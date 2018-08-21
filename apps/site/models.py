from django.db import models
from django.contrib.auth.models import User
import datetime
from vendor.database_storage import DatabaseStorage
from settings import DBS_OPTIONS


class EncryptionType(models.Model):
    encryption_type = models.CharField(max_length=128)

    def __unicode__(self):
        return self.encryption_type


class EncryptedDisk(models.Model):
    email_address = models.CharField(max_length=256, blank=False, null=False)
    user = models.ForeignKey(User, blank=True, null=True)
    asset_tag = models.CharField(max_length=32, blank=False, null=False)
    encryption_type = models.ForeignKey(
            'EncryptionType', verbose_name='System Type'
            )
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    recovery_key = models.TextField(blank=False, null=False)
    binary_blob = models.FileField(
            upload_to='gpg',
            storage=DatabaseStorage(DBS_OPTIONS),
            blank=True,
            null=True,
            default=None
            )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.datetime.today()
        self.updated_on = datetime.datetime.today()

        return super(EncryptedDisk, self).save(*args, **kwargs)

    def __unicode__(self):
        try:
            return "%s - %s" % (self.user.username, str(self.asset_tag))
        except:
            return "%s - %s" % (self.email_address, str(self.asset_tag))

    search_fields = (
                'email_address',
                'asset_tag',
                )
