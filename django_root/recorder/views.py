import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from recorder.models import Employee, LabourCost, Comment, Machine, EmployeeGroup


def emloyee_groups(request):
    groups = EmployeeGroup.objects.all().order_by('name')
    return render(request, 'employee_group_list.html', {'groups': groups})


def employees(request, group_id):
    employees = Employee.objects.filter(group__id=group_id).order_by('first_name')
    return render(request, 'employee_list.html', {'employees': employees})


def machines(request, employee_id):
    machines = Machine.objects.filter(assigned_employees__id=employee_id, active=True).order_by('number')
    employee = Employee.objects.get(id=employee_id)
    return render(request, 'project_list.html', {'machines': machines, 'employee': employee})


@csrf_exempt
def timestamp(request, employee_id, machine_id):
    comments = Comment.objects.all()
    machine = Machine.objects.get(id=machine_id)
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'GET':
        return render(request, 'timestamp.html',
                      {'employee': employee, 'machine': machine, 'comments': comments})

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
