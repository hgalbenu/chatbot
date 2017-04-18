from django.urls import reverse

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import DebtForm
from .models import Debt
from ..profiles.models import UserProfile


class DebtCreateView(CreateView):
    template_name = 'debt_add_or_edit.html'
    form_class = DebtForm

    def get_success_url(self):
        return reverse('profile-edit', kwargs={'pk': self.kwargs.get('user_id')})

    def get_form_kwargs(self):
        form_kwargs = super(DebtCreateView, self).get_form_kwargs()
        form_kwargs['initial'] = {'user_profile_id': self.kwargs.get('user_id')}
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(DebtCreateView, self).get_context_data(**kwargs)
        context.update({
            'user_profile': UserProfile.objects.get(id=self.kwargs.get('user_id'))
        })
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_profile_id = self.kwargs.get('user_id')
        self.object.save()
        return super(DebtCreateView, self).form_valid(form)


class DebtUpdateView(UpdateView):
    template_name = 'debt_add_or_edit.html'
    form_class = DebtForm

    def get_success_url(self):
        return reverse('profile-edit', kwargs={'pk': self.get_object().user_profile.id})

    def get_context_data(self, **kwargs):
        context = super(DebtUpdateView, self).get_context_data(**kwargs)
        context.update({
            'user_profile': self.get_object().user_profile
        })
        return context

    def get_object(self, queryset=None):
        return Debt.objects.get(id=self.kwargs.get('pk'))


class DebtDeleteView(DeleteView, DebtUpdateView):
    pass
