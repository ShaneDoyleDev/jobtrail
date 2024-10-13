from django import forms
from profiles.models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['job_title', 'start_date', 'reason_for_searching', 'follow_up_no_of_days']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'job_title': 'Job your looking for',
            'start_date': 'Date you started looking',
            # TODO: Astrix saying we will remind of this regularly
            'reason_for_searching': 'Why are you looking for a new role?',
            # TODO: Add in an info hover thing where it explains what this is
            'follow_up_no_of_days': 'How soon do you want to follow up?',
        }

        for field in self.fields:
            placeholder = f'{placeholders.get(field, "")}'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

            
