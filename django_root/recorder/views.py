import datetime

from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from recorder.models import Employee, LabourCost, Comment, Machine


def employees(request):
    employees = Employee.objects.all().order_by('first_name')
    return render(request, 'employee_list.html', {'employees': employees})


def machines(request, employee_id):
    machines = Machine.objects.filter(assigned_employees__id=employee_id, active=True).order_by('number')

    return render(request, 'project_list.html', {'machines': machines, 'employee_id': employee_id})


@csrf_exempt
def timestamp(request, employee_id, machine_id):
    comments = Comment.objects.all()
    try:
        machine = Machine.objects.get(id=machine_id)
    except:
        machine = "Sonstiges"
    if request.method == 'GET':
        return render(request, 'timestamp.html',
                      {'employee_id': employee_id, 'machine': machine, 'comments': comments})

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Employee.objects.get(id=employee_id)
        machine_id = request.POST.get('machine_id')
        date = request.POST.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        duration = int(request.POST.get('duration'))
        comment_id = request.POST.get('comment_id')
        amount = (employee.cost_rate / 60) * duration

        recording = LabourCost(employee_id=employee_id, machine_id=machine_id, comment_id=comment_id, date=date,
                               duration=duration, amount=amount)
        recording.save()
        return HttpResponse(status=200)
