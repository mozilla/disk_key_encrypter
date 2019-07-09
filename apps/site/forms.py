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
        try:
            data = self.files['binary_blob'].file
        except KeyError:
            return
        try:
            if len(data.read()) > 10*1024*1024:
                raise forms.ValidationError("Image file too large ( > 10mb )")
            data.seek(0)
        except AttributeError:
            return
        try:
            data.seek(0)
            data.truncate(0)
            tmp = data.read()
            encrypted = encrypt(tmp, GPG_KEY_IDS, HOMEDIR)
            return encrypted
        except Exception as e:
            print(e)
            pass
        return 

    class Meta:
        model = models.EncryptedDisk
        exclude = (
                'user',
                'email_address',
                'created_on',
                'updated_on',
                'legacy_binary_blob',
                'legacy_file_size',
                'file_size',
                'file_data',
                'legacy_binary_blob_data',
                'file_name',
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
