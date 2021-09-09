# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

"""Telegraph views definitions."""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.seo.mixins import PageDetailsMixin
from .forms import ContactMessageForm
from .tasks import contact_form_submission


class ContactFormView(PageDetailsMixin, FormView):
    """Display and send email form."""

    template_name = 'telegraph/contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('telegraph:contact_form')
    sent = False

    @property
    def title(self):
        """Get the title of the contact form page."""
        return _('Contact Form')

    @property
    def description(self):
        """Get the description of the contact form page."""
        return _('Contact Form')

    def form_valid(self, form):
        """
        If the form is valid, render 'template_name' with a context.

        This method is called when valid form data has been POSTed.
        It will return an HttpResponse.
        """
        super().form_valid(form)
        cd = form.cleaned_data

        subject = cd.get(
            cd['subject'],
            _('Contact form submission')
        )

        contact_form_submission.delay(
                subject=subject,
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
        )

        self.sent = True

        return render(
            self.request,
            self.template_name,
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        """Get object's context data to use in contact page."""
        context = super().get_context_data(**kwargs)
        context['sent'] = self.sent

        return context
