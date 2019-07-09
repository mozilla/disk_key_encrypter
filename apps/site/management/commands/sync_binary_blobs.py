from django.core.management.base import BaseCommand, CommandError
from apps.site.models import EncryptedDisk
import base64
from django.db import connection

def my_custom_sql(filename):
    cursor = connection.cursor()
    cursor.execute("SELECT size,data FROM binary_blob where filename=%s",[filename])
    row = cursor.fetchall()
    return row

class Command(BaseCommand):
    help = 'Syncs from binary_blob to site_encrypteddisk.binary_blob_data'

    def handle(self, *args, **options):
        for disk in EncryptedDisk.objects.all():
            if not disk.legacy_binary_blob:
                continue
            binary_data = my_custom_sql(disk.legacy_binary_blob)
            try:
                file_size = binary_data[0][0]
            except:
                continue
            base64_encoded_file_data = binary_data[0][1]
            disk.file_name = disk.legacy_binary_blob
            decoded_file_data = base64.b64decode(base64_encoded_file_data + "====")
            disk.legacy_binary_blob = decoded_file_data
            disk.legacy_file_size = file_size
            disk.save()
        print("All Entries Syncd")
        """
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)
kkkkkkkkkk
            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
        """