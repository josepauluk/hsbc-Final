from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils import timezone
from re import fullmatch
from django.views.decorators.csrf import csrf_protect

from .tokenizer import findSpecificToken, findUser, checkCreationLimit
# from .models import AccessToken

from mail.models import EmailSender
from mail.mail import sendSingleStaged


emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
hashRegex = r'\b[A-Fa-f0-9]{128}\b'

@csrf_protect
def login(request):
    return redirect('logger_main')

@csrf_protect
def logger(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    return render(request, 'cottonLogger/main.html', {})


# def defaultLogin(request):
#     if request.user.is_authenticated:
#         return redirect('logger_main')
#     if request.method == 'POST':
#         if 'email' in request.POST and 'passw' in request.POST:
#             if fullmatch(emailRegex, request.POST['email']): # 'is email' check
#                 user = auth.authenticate(request,
#                     email=request.POST['email'],
#                     password=request.POST['passw'])
#                 if user is not None:
#                     auth.login(request, user)
#                     return redirect('logger_main')
#     return redirect('logger_defaultError')


# def defaultError(request):
#     if request.user.is_authenticated:
#         return redirect('logger_main')
#     return render(request, 'cottonLogger/defaultError.html', {})

@csrf_protect
def token(request):
    if 'auth' in request.GET:
        thash = request.GET['auth']
        if fullmatch(hashRegex, thash):
            print('Token passes fullmatch')
            user = auth.authenticate(request, fullhash=thash)
            if user is not None:

                # register token from email
                tk = findSpecificToken(thash)
                if tk is not None:
                    try:
                        email = EmailSender.objects.get(baseToken=tk)
                        email.opened = timezone.now()
                        email.save()
                    except:
                        pass
                    
                # login
                auth.login(request, user)
                return redirect('logger_main')
            
            else:
                token = findSpecificToken(thash)
                if token is not None:
                    # if token exists
                    return redirect('logger_tokenExpired')
                # if token does not exists 
        else:
            print('Token not passes fullmatch')
        return redirect('logger_tokenError')
    # if theres not 'auth' in GET
    return redirect('logger_main')

@csrf_protect
def tokenError(request):
    return render(request, 'cottonLogger/tokenError.html', {})

@csrf_protect
def tokenExpired(request):
    return render(request, 'cottonLogger/tokenExpired.html', {})

@csrf_protect
def tokenCreate(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
            if fullmatch(emailRegex, email):
                user = findUser(email)
                if user is not None:
                    if checkCreationLimit(user) and not user.is_superuser:
                        mail = EmailSender(destination=user)
                        mail.save()
                        result = sendSingleStaged(mail)
                        if 'ex' in result:
                            return render(request, 'cottonLogger/tokenEmailError.html', {})
                        return render(request, 'cottonLogger/tokenCreated.html', {})
                    return render(request, 'cottonLogger/tokenCreationLimit.html', {})
                return render(request, 'cottonLogger/tokenEmailError.html', {})
    return redirect('logger_main')

@csrf_protect
def logout(request):
    auth.logout(request)
    return redirect('logger_main')
