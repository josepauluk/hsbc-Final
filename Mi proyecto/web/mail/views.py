from django.shortcuts import render, redirect
from django.http import HttpResponse
from .mail import sendAllStaged


def mail(request):
    if not request.user.is_superuser:
        return redirect('error404')
    return render(request, 'sender/sender.html', {})


def sendAll(request):
    if not request.user.is_superuser:
        return redirect('error404')
    
    if request.method == 'POST':
        try:
            limit = int(request.POST['limit'])
        except:
            limit = None
        result = sendAllStaged(limit)
        return render( request, 'sender/resultList.html', { 'rlist': result } )
    #if request.method == 'POST':
    #    result = [
    #        { 'dest': 'juanito@fulanomail.com' },
    #        { 'dest': 'pepito@menganomail.com' },
    #        { 'dest': 'rroberrto@xd.com', 'ex': '(505: error mail bla bla bla EXCEPTION nosecuanto bla bla)' },
    #        { 'dest': 'carlos@truchicorp.com' },
    #    ]
    #    return render( request, 'sender/resultList.html', { 'rlist': result } )
    
    return redirect('emailSend')
