# members/views.py
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import escape

from core.models import Member
from .forms import MemberForm


class MemberListView(LoginRequiredMixin, ListView):
    """List all members with simple ordering by name."""
    model = Member
    template_name = 'members/list.html'
    context_object_name = 'members'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        return qs.filter(name__icontains=q) if q else qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class MemberDetailView(LoginRequiredMixin, DetailView):
    """Show a single member and allow status toggle via a separate POST view."""
    model = Member
    template_name = 'members/detail.html'
    context_object_name = 'member'


class MemberCreateView(LoginRequiredMixin, FormView):
    """Create a new member using a simple form."""
    template_name = 'members/form.html'
    form_class = MemberForm
    success_url = reverse_lazy('members:list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Member created successfully.')
        return super().form_valid(form)


class MemberToggleView(LoginRequiredMixin, DetailView):
    model = Member

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.toggle_status(save=True)

        if getattr(request, 'htmx', False):
            html = render_to_string(
                'members/_member_status.html', {'member': obj}, request=request)
            resp = HttpResponse(html)
            resp['HX-Trigger'] = 'memberStatusToggled'
            return resp

        return HttpResponseRedirect(reverse('members:detail', kwargs={'pk': obj.pk}))


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing member."""
    model = Member
    form_class = MemberForm
    template_name = 'members/form.html'  # reuse the same template as create

    def get_success_url(self):
        # After successful update, go back to detail
        messages.success(self.request, 'Member updated successfully.')
        return reverse('members:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        # Let the template know this is an edit
        ctx = super().get_context_data(**kwargs)
        ctx['is_update'] = True
        return ctx


def well_known_noop(request):
    return HttpResponse(status=204)
