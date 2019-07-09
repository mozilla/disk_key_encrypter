from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import EncryptionType, EncryptedDisk


@admin.register(EncryptedDisk)
class EncryptedDiskAdmin(VersionAdmin):

    pass

admin.site.register(EncryptionType)