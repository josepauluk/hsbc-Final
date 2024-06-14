from django.shortcuts import render

def error403(request, exception=None):
    return render(request, 'error/403.html', { 'except': exception })

def error404(request, exception=None):
    return render(request, 'error/404.html', { 'except': exception })
