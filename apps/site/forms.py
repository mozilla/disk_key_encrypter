from django import forms
from . import models
from apps.site.gpg import encrypt
from settings import GPG_KEY_IDS, HOMEDIR


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class UploadFormUser(forms.ModelForm):
    binary_blob = forms.FileField(label="Binary Key (Optional, if you don't know what this is, skip it)", required=False)  # noqa

    def clean_recovery_key(self):
        data = self.cleaned_data['recovery_key']
        """
            We don't want to allow files to huge
            Going to start with 10MB and see where
            that gets us
        """

        data = bytes(data, 'utf8')
        if len(data) > 0:
            data = encrypt(data, GPG_KEY_IDS, HOMEDIR)
        return data

    def clean_binary_blob(self):
        data = self.cleaned_data['binary_blob']
        try:
            if data.file._size > 10*1024*1024:
                raise forms.ValidationError("Image file too large ( > 10mb )")
        except:
            pass
        try:
            tmp = data.file.read()
            encrypted = encrypt(tmp, GPG_KEY_IDS, HOMEDIR)
            data.file.truncate(0)
            data.file.seek(0)
            data.file.write(encrypted)
            data.file.seek(0)
            return data
        except Exception as e:
            print(e)
            pass

    class Meta:
        model = models.EncryptedDisk
        exclude = (
                'user',
                'email_address',
                'created_on',
                'updated_on',
                )


class UploadFormDesktop(UploadFormUser):

    def get_binary_blob(self):
        print('called')
        return 'asdf'

    class Meta:
        model = models.EncryptedDisk
        exclude = [
            'legacy_binary_blob_data',
            'legacy_binary_blob',
            'legacy_file_size',

        ]


class UploadFormDesktopUpload(UploadFormUser):

    class Meta:
        model = models.EncryptedDisk
        exclude = ('created_on', 'updated_on')
