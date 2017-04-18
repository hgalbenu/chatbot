from django.views.generic import DetailView
from django.urls import reverse
from django.views.generic.edit import UpdateView
from .forms import UserProfileForm

from .models import UserProfile, ExpertNoteTemplate


class ProfileView(DetailView):
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'user_profile': self.get_object()
        })
        return context


class ProfileEditView(UpdateView):
    template_name = 'profile_edit.html'
    form_class = UserProfileForm

    def get_form_kwargs(self):
        form_kwargs = super(ProfileEditView, self).get_form_kwargs()
        obj = self.get_object()
        form_kwargs['initial'] = {
            'email': obj.email,
            'expert_note_template_name': ExpertNoteTemplate.objects.filter(name=obj.expert_note_template_name).first()
        }
        return form_kwargs

    def get_success_url(self):
        return reverse('profile-edit', kwargs=self.kwargs)

    def get_object(self, queryset=None):
        return UserProfile.objects.get(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        context.update({
            'user_profile': self.get_object()
        })
        return context

    def post(self, request, *args, **kwargs):
        return super(ProfileEditView, self).post(request, *args, **kwargs)
