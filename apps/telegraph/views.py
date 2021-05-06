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

import logging

from django.conf import settings
from django.core.mail import (
    BadHeaderError,
    EmailMultiAlternatives,
    get_connection,
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.seo.mixins import PageDetailsMixin
from .forms import ContactMessageForm


class ContactFormView(PageDetailsMixin, FormView):
    """Display and send email form."""

    template_name = 'telegraph/contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('telegraph:contact_form')
    sent = False

    @property
    def title(self):
        return _('Contact Form')

    @property
    def description(self):
        return _('Contact Form')

    def form_valid(self, form):
        """If the form is valid, render 'template_name' with a context."""
        super().form_valid(form)
        cd = form.cleaned_data

        subject = cd.get(
            cd['subject'],
            _('Contact form submission')
        )

        try:
            mail = EmailMultiAlternatives(
                subject=subject,
                body=cd['message'],
                from_email=settings.SERVER_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[f"{cd['name']} <{cd['email']}>"],
                connection=get_connection(),
            )

            self.sent = mail.send() > 0

        except BadHeaderError as exc:
            # TODO: Handle this better
            logging.exception(exc)

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
