from django.contrib import admin
from .models import EncryptionType, EncryptedDisk

admin.site.register(EncryptionType)
admin.site.register(EncryptedDisk)
