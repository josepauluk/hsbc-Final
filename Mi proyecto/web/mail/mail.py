from django.utils import timezone
from django.shortcuts import render
from django.http import HttpRequest
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import EmailSender
from cottonLogger.models import AccessToken


def sendEmail(subject, template, context, destination) -> dict():
    # html_content = render_to_string(template, context)
    html_content = render(HttpRequest(), template, context).serialize().decode()
    email = EmailMultiAlternatives(
        subject=subject,
        body='CONTENT',
        from_email=settings.EMAIL_HOST_USER,
        to=(destination,)
    )
    email.attach_alternative(html_content, "text/html")
    result = { 'dest': f'{destination}' }
    try:
        email.send(fail_silently=False)
    except Exception as e:
        result['ex'] = f'{e.args}'
    return result


def sendSingleStaged(id: EmailSender) -> dict():
    # create the token
    token = AccessToken(owner=id.destination)
    token.save()
    id.base_token = token
    
    # send mail
    subject = 'INVITACION ENTIDAD FINANCIERA' \
        if id.is_first_email \
        else 'Token de acceso'
        
    template = 'mail/mail_init.html' \
        if id.is_first_email \
        else 'mail/mail_token.html'
            
    result = sendEmail(
        subject=subject,
        template=template,
        context={
            'directory': '127.0.0.1:8000',
            'staticDir': 'http://127.0.0.1:8000',
            'fullhash': id.base_token.getHash(),
            'name': f'{id.destination.last_name}, {id.destination.first_name}',
        },
        destination=id.destination.email
    )
    
    # register
    if 'ex' in result:
        id.base_token.is_active = False
        id.base_token.save()
        id.base_token = None
    else:
        id.sent_on = timezone.now()

    id.save()
    return result


def sendAllStaged(limit: int | None = None) -> list(dict()):
    mails = EmailSender.objects.filter(sent_on=None)
    index = 0
    resultList = []
    for mail in mails:
        
        if limit is not None:
            if index >= limit:
                break
        
        resultList.append(
            sendSingleStaged(mail)
        )
        
        index += 1
        
    return resultList


# OLD CODE:
'''
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_mass_email(subject, template, context, recipient_list):
    html_content = render_to_string(template, context)
    plain_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list
    )
    
    email.attach_alternative(html_content, "text/html")

    # Enviamos el correo electrónico
    email.send()

def mail (request):
    if not request.user.is_authenticated:
        return redirect('error404')
    if request.method == 'POST':
        send_mass_email(
            subject='¡Oferta de primavera!',
            template='mail/mail.html',
            context={
            #    'product_name': 'Zapatillas deportivas',
            #    'discount': '30%',
            #    'expiration_date': '30 de abril de 2023',
                'directory': '127.0.0.1:8000',
                'fullhash': '12341234abcdabcd',
            },
            recipient_list=[
            #    'cristianbufaliniadrian@gmail.com',
            #    'julianmn15@gmail.com',
            #    'soleadhernandez@gmail.com',
            #    'el-eze@hotmail.com',
            ]
        )
    return render(request, 'mail/envio_mail.html', {})
'''
