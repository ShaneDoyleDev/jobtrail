from allauth.account.forms import SignupForm
from django import forms

# forms.py
from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=100, label="Full Name")
    job_title = forms.CharField(max_length=100, label="Job Title")
    start_date = forms.DateField(required=True, widget=forms.SelectDateWidget(), label="Start Date of Search")
    reason_for_searching = forms.CharField(widget=forms.Textarea, label="Reason for Searching")
    follow_up_no_of_days = forms.IntegerField(label="Desired Time to Follow Up")
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.job_title = self.cleaned_data.get('job_title')
        user.start_date = self.cleaned_data.get('start_date')
        user.reason_for_searching = self.cleaned_data.get('reason_for_searching')
        user.follow_up_no_of_days = self.cleaned_data.get('follow_up_no_of_days')

        user.save()
        return user
