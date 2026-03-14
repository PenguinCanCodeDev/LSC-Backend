from django.db import models


class UpdateType(models.TextChoices):
    TRAME_SESSION = 'trame session', 'TRAME SESSION'
    PODCAST = 'podcast', 'PODCAST'
    HOLIDAY_TASK = 'holiday task', 'HOLIDAY TASK'


class UpdateTag(models.TextChoices):
    L300 = 'l300', 'L300'
    LSC = 'lsc', 'LSC'


class Update(models.Model):

    title = models.CharField(
        max_length=200,
        help_text='The title of this update'
    )

    type = models.CharField(
        max_length=15,
        choices=UpdateType.choices,
        help_text='The type of update this is'
    )

    tag = models.CharField(
        max_length=5,
        choices=UpdateTag.choices,
        default=UpdateTag.L300,
        help_text='The audience this update is for (l300 or lsc)'
    )

    happening_when = models.DateTimeField(
        help_text='The date and time this update is happening'
    )

    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='An optional link associated with this update (e.g. meeting link, resource URL)'
    )

    def __str__(self):
        return self.title