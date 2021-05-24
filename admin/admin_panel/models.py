import uuid

from django.db import models
from django.template.loader import render_to_string

from admin_panel.misc import EmailSender


class UpdatedCreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Content(UpdatedCreatedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.CharField(max_length=50)
    text = models.TextField()

    class Meta:
        db_table = '"public"."content"'

    def __str__(self):
        return self.text[:50]


class Notification(UpdatedCreatedMixin):
    sender = EmailSender

    STATUS_PENDING = 'pending'
    STATUS_DONE = 'done'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, db_column='content_id')
    recipient = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default=STATUS_PENDING)

    class Meta:
        db_table = '"public"."notification"'

    @property
    def id_as_str(self):
        return str(self.id)

    def do_notify(self, data=None):
        html_data = self._get_html(data=data)
        self.sender.send(html=html_data, subject=self.content_id.event, receiver_email=self.recipient)
        self._notify_done()

    def _notify_done(self):
        self.status = self.STATUS_DONE

    def _get_html(self, data=None):
        ctx = {'content': self.content_id.text}
        if data:
            ctx['data'] = data
        return render_to_string(f'admin_panel/{self.content_id.event}.html', context=ctx)

    def __str__(self):
        return '%s %s' % (self.id_as_str, self.status)


class Compaigne(UpdatedCreatedMixin):
    content_id = models.ForeignKey(Content, on_delete=models.DO_NOTHING, db_column='content_id')

    class Meta:
        db_table = '"public"."compaigne"'

    def __str__(self):
        return f'Compaign #{self.id}, event {self.content_id.event}'
