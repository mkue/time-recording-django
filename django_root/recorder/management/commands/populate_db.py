import csv
import os
from datetime import datetime

import sys
from django.core.management import BaseCommand

from recorder.models import Comment, Machine, MachineType, Project, Employee, LabourCost


def get_name(fullname):
    namelist = fullname.split()
    return namelist[0], namelist[1]


def get_number_from_string(machine_string):
    if not machine_string[0].isdigit():
        return -1
    i = 0
    machine_nr = ''
    while i < len(machine_string) and machine_string[i].isdigit():
        machine_nr += machine_string[i]
        i += 1
    return int(machine_nr)


def parse_project_name(project_name):
    print(project_name)
    splitted_name = project_name.split('_')
    number_of_underscores = len(splitted_name) - 1

    if number_of_underscores == 1:
        description = splitted_name[0] + ' ' + splitted_name[1]
        return None, description, None, None

    elif number_of_underscores == 2:
        try:
            description = splitted_name[1]
            project_number = int(splitted_name[0])
        except ValueError:
            description = splitted_name[0]
            project_number = int(splitted_name[1])

        description += ' ' + splitted_name[2]
        return project_number, description, None, None

    elif number_of_underscores == 3 or number_of_underscores == 4:
        project_number = get_number_from_string(splitted_name[1])
        machine_nr = get_number_from_string(splitted_name[0])
        description = splitted_name[3]
        if number_of_underscores == 4:
            description += ' ' + splitted_name[4]
        machine_type, _ = MachineType.objects.get_or_create(name=splitted_name[2])
        return project_number, description, machine_nr, machine_type


def add_projects_to_employees():
    employees = Employee.objects.all()
    machines = Machine.objects.all()
    for machine in machines:
        machine.assigned_employees.add(*employees)


class Command(BaseCommand):
    help = 'Populate the database from a .csv file (export from current Access database).'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Full path to .csv file')

    def handle(self, *args, **options):
        timestamps_file = open(options['path'], 'r', encoding='utf-8')
        csv_reader = csv.DictReader(timestamps_file, delimiter=';')

        for row in csv_reader:
            last_name, first_name = get_name(row['Mitarbeiter'])
            employee, _ = Employee.objects.get_or_create(first_name=first_name, last_name=last_name)

            comment_text = row['Kommentar']
            comment, _ = Comment.objects.get_or_create(text=comment_text) if len(comment_text) > 0 else (None, None)

            project_nr, project_desc, machine_nr, machine_type = parse_project_name(row['Projektname'])
            if project_nr:
                project, _ = Project.objects.get_or_create(number=project_nr, description=project_desc)
            if machine_nr:
                machine, _ = Machine.objects.get_or_create(number=machine_nr, type=machine_type, project=project)
            date = datetime.strptime(row['Datum'], '%d.%m.%Y').date()
            duration = int(row['Dauer(min)'])
            amount = (employee.cost_rate / 60) * duration
            LabourCost.objects.get_or_create(employee=employee, machine=machine, comment=comment, duration=duration,
                                             date=date, amount=amount)

        add_projects_to_employees()
