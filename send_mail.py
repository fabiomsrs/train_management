import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "train_management.settings")
django.setup()

from django.core.mail import send_mail
from train_management.settings import EMAIL_HOST_USER
from core.models import PreparationClass
from user.models import Employee
from datetime import datetime
import locale 

message_employees = []

try: 
    locale.setlocale(locale.LC_ALL, 'pt_BR') 
except: 
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil') 
    
for preparation_class in PreparationClass.objects.filter(date__gte=datetime.today().date()):
    for employee in preparation_class.employees.all():
        message_employees.append(employee)
    for position in preparation_class.positions.all():
        for employee in Employee.objects.filter(position=position, association=preparation_class.association):
            if employee not in message_employees:
                message_employees.append(employee)
    for employee in message_employees:
        print("sending email to " + employee.first_name + " email: " + employee.email)                
        send_mail(
            'Treinamento para assistir',
            'Olá ' + employee.first_name + ", você tem um treinamento para assistir em " + str(preparation_class.date.strftime('%d %B %Y')) + " às " + str(preparation_class.time) +" administrado pelo instrutor " + preparation_class.coach.first_name + "." ,
            EMAIL_HOST_USER,
            [employee.email],
            fail_silently=False,
        )
    coach = preparation_class.coach
    send_mail(
        'Treinamento para administrar',
        'Olá ' + coach.first_name + ", você tem um treinamento para administrar em " + str(preparation_class.date.strftime('%d %B %Y')) + " às " + str(preparation_class.time) + "." ,
        EMAIL_HOST_USER,
        [coach.email],
        fail_silently=False,
        )
    message_employees = []