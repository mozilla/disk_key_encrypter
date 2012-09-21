from django import forms
import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from apps.site.gpg import encrypt
from settings import GPG_KEY_IDS

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class UploadFormUser(forms.ModelForm):
    binary_blob = forms.FileField(label="Binary Key (Optional, if you don't know what this is, skip it)", required=False)
    def clean_recovery_key(self):
        data = self.cleaned_data['recovery_key']
        """
            We don't want to allow files to huge
            Going to start with 10MB and see where
            that gets us
        """

        if data._size > 10*1024*1024:
            raise forms.ValidationError("Image file too large ( > 10mb )")


        if len(data) > 0:
            data = encrypt(data, GPG_KEY_IDS)
        return data
    def clean_binary_blob(self):
        data = self.cleaned_data['binary_blob']
        try:
            tmp = data.file.read()
            encrypted = encrypt(tmp, GPG_KEY_IDS)
            data.file.truncate(0)
            data.file.seek(0)
            data.file.write(encrypted)
            data.file.seek(0)
            return data;
        except Exception, e:
            print e
            pass

    class Meta:
        model = models.EncryptedDisk
        exclude=(
                'user',
                'email_address',
                'created_on',
                'updated_on',
                )

class UploadFormDesktop(UploadFormUser):

    def get_binary_blob(self):
        print 'called'
        return 'asdf'

    class Meta:
        model = models.EncryptedDisk
        exclude = ()

class UploadFormDesktopUpload(UploadFormUser):

    class Meta:
        model = models.EncryptedDisk
        exclude = ('created_on', 'updated_on')
