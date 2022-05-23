from django import forms

from apps.profile.models import Profile


class ProfileForm(forms.ModelForm):

    user_photo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = (
            "birthday",
            "gender",
            "phone",
            "address",
            "address_number",
            "city",
            "zip",
            "first_name",
            "last_name",
            "state",
            "country",
            "user_photo",
        )
