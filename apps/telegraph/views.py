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

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .forms import ContactMessageForm


def contact_form(request):
    """Contact form handler."""
    sent = False
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd.get(cd['subject'], _('Contact form submission'))

            try:
                sent_messages = send_mail(
                    subject=subject,
                    message=cd['message'],
                    from_email=f"{cd['name']} <{cd['email']}>",
                    recipient_list=['egrep@protonmail.ch'],
                )
                sent = sent_messages > 0
            except BadHeaderError:
                return HttpResponse(_('Invalid header found'))
    else:
        form = ContactMessageForm()

    context = {
        'form': form,
        'sent': sent,
        'page_description': _('Contact Form'),
        'page_title': _('Contact Form'),
    }

    return render(request, 'telegraph/contact.html', context)
