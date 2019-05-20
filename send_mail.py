import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "train_management.settings")
django.setup()

from django.core.mail import send_mail
from django.db.models import Q, F
from train_management.settings import EMAIL_HOST_USER
from core.models import PreparationClass
from user.models import Employee
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import locale 


try: 
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
except: 
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil') 
    
for employee in Employee.objects.filter(Q(my_preparations_classes__date__gte=datetime.today().date()) | Q(position__my_preparations_classes__association=F('association'))).distinct():
    print(employee.first_name)
    email_content = """   
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>html title</title>        
    <style>
        table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }

        td {        
        text-align: center;
        padding: 8px;
        color: black;
        }

        th {
        color: white;
        background-color: #4CAF50;
        border: 1px solid white ;
        text-align: center;
        padding: 8px;
        }

        tr.even {
        background-color: #D3D3D3;
        }
    </style>
    </head>
    
    <body>
    Olá, <b>"""+ employee.first_name +"""</b>
    <p> Hoje você terá os seguintes treinamentos para assistir</p>
    <table>
    <thead>
        <tr>
            <th>Nome do treinamento</th>                
            <th>Dia</th>
            <th>Hora</th>
            <th>Local</th>
            <th>Unidade</th>
            <th>Instrutor</th>
        </tr>
    </thead>
    <tbody>"""
    cont = 1
    for preparation_class in employee.my_preparations_classes.filter(date__gte=datetime.today().date()) | PreparationClass.objects.filter(positions=employee.position, association=employee.association):
        if cont % 2 == 1:
            email_content += """<tr class="even">
                <td class="cell">"""+preparation_class.title+"""</td>
                <td class="cell">"""+str(preparation_class.date.strftime('%d %B %Y'))+"""</td>
                <td class="cell">"""+str(preparation_class.time)+"""</td>
                <td class="cell">"""+preparation_class.location.name+"""</td>
                <td class="cell">"""+preparation_class.association.name+"""</td>
                <td class="cell">"""+preparation_class.coach.first_name+"""</td>
            </tr>"""
        else:
            email_content += """<tr>
                    <td class="cell">"""+preparation_class.title+"""</td>
                    <td class="cell">"""+str(preparation_class.date.strftime('%d %B %Y'))+"""</td>
                    <td class="cell">"""+str(preparation_class.time)+"""</td>
                    <td class="cell">"""+preparation_class.location.name+"""</td>
                    <td class="cell">"""+preparation_class.association.name+"""</td>
                    <td class="cell">"""+preparation_class.coach.first_name+"""</td>
                </tr>"""
        cont+=1
            
    """
    </tbody>
    </table>    
    </body>     
    </html>            
    """

    HTML_BODY = MIMEText(email_content, 'html')
    
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = "Treinamento para assistir"
    MESSAGE['To'] = employee.email
    MESSAGE['From'] = EMAIL_HOST_USER
    MESSAGE.preamble = """
        Your mail reader does not support the report format.
    Please visit us <a href="http://www.mysite.com">online</a>!
    """

    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(EMAIL_HOST_USER,'99789726')
    server.sendmail(EMAIL_HOST_USER, [employee.email], MESSAGE.as_string())
    
for employee in Employee.objects.filter(my_classes__date__gte=datetime.today().date()):
    print(employee.first_name)
    email_content = """   
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>html title</title>        
    <style>
        table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }

        td {        
        text-align: center;
        padding: 8px;
        color: black;
        }

        th {
        color: white;
        background-color: #4CAF50;
        border: 1px solid white ;
        text-align: center;
        padding: 8px;
        }

        tr.even {
        background-color: #D3D3D3;
        }
    </style>
    </head>
    
    <body>
    Olá, <b>"""+ employee.first_name +"""</b>
    <p> Hoje você terá os seguintes treinamentos para administrar</p>
    <table>
    <thead>
        <tr>
            <th>Nome do treinamento</th>                
            <th>Dia</th>
            <th>Hora</th>
            <th>Local</th>
            <th>Unidade</th>            
        </tr>
    </thead>
    <tbody>"""
    cont = 1
    for preparation_class in employee.my_classes.filter(date__gte=datetime.today().date()):
        if cont % 2 == 1:
            email_content += """<tr class="even">
                <td class="cell">"""+preparation_class.title+"""</td>
                <td class="cell">"""+str(preparation_class.date.strftime('%d %B %Y'))+"""</td>
                <td class="cell">"""+str(preparation_class.time)+"""</td>
                <td class="cell">"""+preparation_class.location.name+"""</td>
                <td class="cell">"""+preparation_class.association.name+"""</td>                
            </tr>"""
        else:
            email_content += """<tr>
                    <td class="cell">"""+preparation_class.title+"""</td>
                    <td class="cell">"""+str(preparation_class.date.strftime('%d %B %Y'))+"""</td>
                    <td class="cell">"""+str(preparation_class.time)+"""</td>
                    <td class="cell">"""+preparation_class.location.name+"""</td>
                    <td class="cell">"""+preparation_class.association.name+"""</td>                    
                </tr>"""
        cont+=1
            
    """
    </tbody>
    </table>    
    </body>     
    </html>            
    """

    HTML_BODY = MIMEText(email_content, 'html')
    
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = "Treinamentos para administrar"
    MESSAGE['To'] = employee.email
    MESSAGE['From'] = EMAIL_HOST_USER
    MESSAGE.preamble = """
        Your mail reader does not support the report format.
    Please visit us <a href="http://www.mysite.com">online</a>!
    """

    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(EMAIL_HOST_USER,'99789726')
    server.sendmail(EMAIL_HOST_USER, [employee.email], MESSAGE.as_string())
    
server.quit()
