from django.shortcuts import render

def home(request):
    return render(request, 'staticpages/index.html')

def test_404(request):
    return render(request, 'staticpages/404.html')

def test_500(request):
    return render(request, 'staticpages/500.html')