from django.shortcuts import render

# Create your views here.
def dashboard(request):

    return render(request, 'job_application/dashboard.html')
