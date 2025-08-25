# members/views.py
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import escape

from core.models import Member


class MemberForm(forms.ModelForm):
    """Minimal form for creating a new member."""
    class Meta:
        model = Member
        fields = ['name', 'email']  # status defaults to CURRENT


class MemberListView(LoginRequiredMixin, ListView):
    """List all members with simple ordering by name."""
    model = Member
    template_name = 'members/list.html'
    context_object_name = 'members'
    paginate_by = 10  # demo-friendly pagination


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
    """HTMX-aware toggle: returns a fragment on HTMX requests; redirects otherwise."""
    model = Member

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.toggle_status(save=True)

        if getattr(request, 'htmx', False):
            # Return small HTML fragment + trigger a client-side event
            html = (
                '<p>Status: <strong>{status}</strong></p>'
                '<form '
                '  hx-post="{url}" '
                '  hx-target="#member-status" '
                '  hx-swap="outerHTML">'
                "{csrf}<button type='submit'>Toggle status</button>"
                '</form>'
            ).format(
                status=escape(obj.get_status_display()),
                url=escape(reverse('members:toggle', kwargs={'pk': obj.pk})),
                csrf=self._csrf_token_input(request),
            )
            resp = HttpResponse(html)
            # Optional: trigger a toast on client (we’ll listen later in base.html)
            resp['HX-Trigger'] = 'memberStatusToggled'
            return resp

        # Non-HTMX fallback: classic redirect
        return HttpResponseRedirect(reverse('members:detail', kwargs={'pk': obj.pk}))

    def _csrf_token_input(self, request):
        from django.middleware.csrf import get_token
        token = get_token(request)
        return f"<input type='hidden' name='csrfmiddlewaretoken' value='{token}'>"
