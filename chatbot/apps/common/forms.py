from django import forms


class MotionAIWebHookForm(forms.Form):
    message_from = forms.CharField()
    message_to = forms.CharField()
    bot_reply = forms.CharField()
    reply_data = forms.CharField()

    module_id = forms.IntegerField()
    session = forms.CharField()
    direction = forms.CharField()
    attached_media = forms.CharField
