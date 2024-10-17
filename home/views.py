from django.shortcuts import render

def home(request):
    return render(request, 'staticpages/index.html')

def test_404(request):
    return render(request, 'staticpages/test-404.html')