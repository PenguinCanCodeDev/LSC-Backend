from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings

class EventType(models.TextChoices):
    TRAME_SESSION = 'trame_session', 'TRAME SESSION'
    HOLIDAY_TASK = 'holiday_task', 'HOLIDAY TASK'

class Tag(models.TextChoices):
    LSC = 'lsc', 'LSC'
    L300 = 'l300', 'L300'

class Level(models.TextChoices):
    HUNDRED_TO_FOUR_HUNDRED = '100-400L', '100 - 400L'
    FOUR_HUNDRED_TO_SIX_HUNDRED = '400-600L', '400 - 600L'

class Event(models.Model):

    title = models.CharField(
        max_length=200,
        help_text='The title of this event'
    )

    happening_when = models.DateTimeField(help_text='The date and time this event occurs')

    thumbnail = CloudinaryField(
        folder=f'{settings.CLOUDINARY_MEDIA_PREFIX_URL}/event_images/',
        help_text='The image associated to this event',
        blank=True,
        null=True
    )

    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='An optional link associated with this event (e.g. meeting link, resource URL)'
    )

    event_type = models.CharField(
        max_length=15,
        choices=EventType.choices,
        default=EventType.TRAME_SESSION,
        help_text='The type of event this is (trame session or holiday task)'
    )
    tag = models.CharField(
        max_length=15,
        choices=Tag.choices,
        default=Tag.L300,
        help_text='The tag associated to this event (lsc or l300)'
    )
    level = models.CharField(
        max_length=15,
        choices=Level.choices,
        default=Level.HUNDRED_TO_FOUR_HUNDRED,
        help_text='The students level associated to this event (100-400L or 400-500L)'
    )
    created_when = models.DateTimeField(
        auto_now_add=True,
        help_text='The date and time this event was created'
    )

    def __str__(self):
        return self.title