# Create your views here.
from urllib import parse
from datetime import datetime

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.conf import settings

from .models import MotionAI

from ..profiles.forms import USER_STATUS_MAPPING
from ..profiles.models import UserProfile
from ..debts.models import Debt
from ..jobs.models import Job


class MotionAIWebHookView(View):
    def post(self, request):
        data = request.POST.dict()

        # store the raw data
        MotionAI.save_data(data)

        # we only care about messages sent to the bot, discard bot -> user messages
        if data['to'] != data['botID']:
            return HttpResponse(status=204, data='')

        # make sure this is our bot
        if data['secret'] != settings.MOTION_AI_WEBHOOK_SECRET:
            raise PermissionDenied

        bot_id = int(data['botID'])
        bot_mappings = settings.MOTION_AI_MODULE_MAPPING.get(bot_id)
        if not bot_mappings:
            raise PermissionDenied

        # we need a session
        if not data['session']:
            raise PermissionDenied

        # get module, abort if not found
        module_id = int(data['moduleID'])

        is_user = module_id in bot_mappings.get('User', {}).keys()
        is_debt = module_id in bot_mappings.get('Debt', {}).keys()
        is_job = module_id in bot_mappings.get('Job', {}).keys()

        user_profile = None
        # TODO - refactor this
        if is_user:
            field_name = bot_mappings.get('User').get(module_id)
            user_data = {
                'botId': bot_id,
                field_name: parse.unquote(data['reply'])
            }
            user_profile = UserProfile.objects.get_or_create(session_id=data['session'], defaults=user_data)[0]
            user_profile.save()

            if field_name == 'email' and user_profile.user_status == 'None':
                # If the user has no user_status set yet, change it to '1 - Waiting data review'
                index_of_status = list(USER_STATUS_MAPPING.values()).index('waiting_data_review_at')
                status_name = list(USER_STATUS_MAPPING.keys())[index_of_status]
                user_profile.user_status = status_name
                user_profile.waiting_data_review_at = datetime.now()
                user_profile.save()

        elif is_debt:
            field_name = bot_mappings.get('Debt').get(module_id)
            user_profile = UserProfile.objects.filter(session_id=data['session']).first()
            if not user_profile:
                raise Http404
            is_new_debt = settings.MOTION_AI_DEBT_NEW == module_id
            if is_new_debt:
                debt = Debt(user_profile_id=user_profile.id)
                user_profile.current_debt = debt
                user_profile.save()
            elif user_profile.current_debt:
                debt = user_profile.current_debt
            else:
                raise Exception  # something went wrong
            setattr(debt, field_name, parse.unquote(data['reply']))
            debt.save()

        elif is_job:
            field_name = bot_mappings.get('Job').get(module_id)
            user_profile = UserProfile.objects.filter(session_id=data['session']).first()
            if not user_profile:
                raise Http404
            is_new_job = settings.MOTION_AI_JOB_NEW == module_id
            if is_new_job:
                job = Job(user_profile_id=user_profile.id)
                user_profile.current_job = job
                user_profile.save()
            elif user_profile.current_job:
                job = user_profile.current_job
            else:
                raise Exception  # something went wrong
            setattr(job, field_name, parse.unquote(data['reply']))
            job.save()

        else:
            raise PermissionDenied

        resp = {'action': user_profile.action} if user_profile else {}
        print('MotionAI', data, resp)
        return JsonResponse(resp)
