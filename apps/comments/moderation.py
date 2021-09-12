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

"""Comment-moderation module."""

from django.contrib.sites.shortcuts import get_current_site
from django_comments.moderation import CommentModerator

from apps.comments.tasks import notification_send


class PostCommentModerator(CommentModerator):
    """Encapsulates comment-moderation options for Post model."""

    # If True, any new comment on an object of this model which survives
    # moderation (i.e., is not deleted) will generate an email to site staff.
    email_notification = True

    # If this is set to the name of a BooleanField on the model for which
    # comments are being moderated, new comments on objects of that model
    # will be disallowed (immediately deleted) whenever the value of that
    # field is False on the object the comment would be attached to.
    enable_field = 'allow_comments'

    # Like auto_close_field, but instead of outright deleting new comments
    # when the requisite number of days have elapsed, it will simply set the
    # is_public field of new comments to False before saving them. Must be
    # used in conjunction with moderate_after, which specifies the number of
    # days past which comments should be moderated.
    auto_moderate_field = 'created_at'

    # If auto_moderate_field is used, this must specify the number of days past
    # the value of the field specified by auto_moderate_field after which new
    # comments for an object should be marked non-public. Allowed values are
    # None, 0 (which moderates comments immediately), or any positive integer.
    moderate_after = 0

    def moderate(self, comment, content_object, request):
        """
        Moderate a given comment comment.

        Determine whether a given comment on a given object should be
        allowed to show up immediately, or should be marked non-public
        and await approval.

        Return ``True`` if the comment should be moderated (marked
        non-public), ``False`` otherwise.
        """
        # If the user who commented is a staff member, don't moderate
        if comment.user and comment.user.is_staff:
            return False
        return super().moderate(comment, content_object, request)

    def email(self, comment, content_object, request):
        """Send email notification of a new comment to site staff."""
        # Do not sent notification for site staff
        if comment.user and comment.user.is_staff:
            return

        # Do not sent notification if email notification is disabled
        if not self.email_notification:
            return

        user_id = None
        if comment.user:
            user_id = comment.user.pk

        site = get_current_site(request)
        notification_send.delay(
            comment_pk=comment.pk,
            site_name=site.name,
            site_url=f'{request.scheme}://{site.domain}',
            user_id=user_id,
        )
