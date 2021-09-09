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

"""Telegraph Celery tasks."""

from smtplib import SMTPConnectError

from django.conf import settings
from django.core.mail import (
    BadHeaderError,
    EmailMultiAlternatives,
    get_connection,
)

from branch import celery_app
from branch.celery import log



@celery_app.task(
    rate_limit='1/s',
    retry_kwargs={'max_retries': 5},
    retry_backoff=True,
    autoretry_for=(SMTPConnectError,),
    name='apps.telegraph.tasks.contact_form_submission',
)
def contact_form_submission(subject, message, sender_name, sender_email):
    """Contact form submission task."""
    reply_to = f'{sender_name} <{sender_email}>'

    try:
        mail = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.SERVER_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[reply_to],
            connection=get_connection(),
        )

        if mail.send() == 0:
            log.error('Unable to sent contact form')
    except BadHeaderError as exc:
        log.exception(exc)
