from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import pytz
from settings import DBS_OPTIONS


class EncryptionType(models.Model):
    encryption_type = models.CharField(max_length=128)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.encryption_type

# update site_encrypteddisk, binary_blob set site_encrypteddisk.legacy_binary_blob_data = binary_blob.data where site_encrypteddisk.legacy_binary_blob = binary_blob.filename;
class EncryptedDisk(models.Model):
    email_address = models.CharField(max_length=256, blank=False, null=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    asset_tag = models.CharField(max_length=32, blank=False, null=False)
    encryption_type = models.ForeignKey(
            'EncryptionType', verbose_name='System Type', on_delete=models.CASCADE
            )
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True, auto_now=True)
    recovery_key = models.TextField(blank=False, null=False)
    file_data = models.TextField(null=True, blank=True)
    file_name = models.CharField(max_length=256, blank=True, null=True)
    legacy_binary_blob = models.TextField(null=True, blank=True)
    legacy_binary_blob_data = models.TextField(null=True, blank=True)
    legacy_file_size = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        return super(EncryptedDisk, self).save(*args, **kwargs)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        try:
            return "%s - %s" % (self.user.username, str(self.asset_tag))
        except:
            return "%s - %s" % (self.email_address, str(self.asset_tag))

    search_fields = (
                'email_address',
                'asset_tag',
                )
