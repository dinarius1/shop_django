from django.core.mail import send_mail
from decouple import config
from celery import shared_task #позволяет его видеть вне джанго. ассинхронно

# def send_activation_code(email: str,code: str):
#     message = ''
#     html = f'''
#     <h1>для активации аккаунта нажмите на кнопку</h1>
#     <a href='{config("LINK")}api/v1/account/activate/{code}'>
#     <button>Activate</button>
#     </a>
#     '''
#     send_mail(
#         subject='Активация аккаунта',
#         message = message,
#         from_email= 'a@gmail.com',
#         recipient_list=[email], #recipient_list - куда или кому отпарвивть. на данную почту отправляем активационный код
#         html_message=html
#     )

@shared_task
def send_activation_code(email: str,code: str):
    message = ''
    html = f'''
    <h1>для активации аккаунта нажмите на кнопку</h1>
    <a href='http://127.0.0.1:8000/api/v1/account/activate/{code}'>
    <button>Activate</button>
    </a>
    '''
    send_mail(
        subject='Активация аккаунта',
        message = message,
        from_email= 'a@gmail.com',
        recipient_list=[email], #recipient_list - куда или кому отпарвивть. на данную почту отправляем активационный код
        html_message=html
    )