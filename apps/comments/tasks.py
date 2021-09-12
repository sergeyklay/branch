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

"""Comments Celery tasks."""

from smtplib import SMTPConnectError

import structlog
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django_comments import get_model
from django_comments.models import Comment

from branch import celery_app

logger = structlog.get_logger(__name__)


@celery_app.task(
    rate_limit='1/s',
    retry_kwargs={'max_retries': 5},
    retry_backoff=True,
    autoretry_for=(SMTPConnectError,),
    name='apps.comments.tasks.notification_send',
)
def notification_send(comment_pk, site_name, site_url, user_id=None):
    """Send email notification of a new comment to site staff."""
    logger.bind(comment_pk=comment_pk, user_id=user_id)
    logger.debug('notification_send_started', status='START')

    managers = getattr(settings, 'MANAGERS', None)
    if not managers or len(managers) == 0:
        logger.error('improperly_configured',
                     message='settings.MANAGERS is empty')
        return 0

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    if not from_email:
        logger.error('improperly_configured', message='server email is missed')
        return 0

    recipient_list = [manager[1] for manager in managers]
    t = loader.get_template('comments/comment_notification_email.txt')

    comment_model = get_model()
    comment = comment_model.objects.get(pk=comment_pk)  # type: Comment

    c = {
        'admin_site_url': settings.ADMIN_SITE_URL,
        'comment': comment,
        'content_object': comment.content_object,
        'site_url': site_url,
        'user_name': comment.name,
        'user_email': comment.email,
    }

    subject = _('[%(site)s] New comment posted on "%(object)s"') % {
        'site': site_name,
        'object': comment.content_object,
    }

    message = t.render(c)
    mail = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
        reply_to=[from_email],
        connection=get_connection(),
    )

    result = mail.send()
    if result > 0:
        logger.info('notification_send_finished', status='OK')
    else:
        logger.warn('notification_send_finished', status='KO')

    return result
