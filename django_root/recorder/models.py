from django.db import models
from django.db.models import DO_NOTHING, Sum


class Project(models.Model):
    number = models.IntegerField(verbose_name='Projektnummer')
    description = models.CharField(verbose_name='Bezeichnung', max_length=200)

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekte'

    def __str__(self):
        return str(self.number) + ' - ' + self.description

    def total_costs(self):
        machines = Machine.objects.filter(project_id=self.id)
        total_costs = 0
        for machine in machines:
            total_costs += machine.total_costs()
        return total_costs


class EmployeeGroup(models.Model):
    name = models.CharField(verbose_name='Bezeichnung', max_length=64)

    class Meta:
        verbose_name = 'Mitarbeitergruppe'
        verbose_name_plural = 'Mitarbeitergruppen'

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(verbose_name='Vorname', max_length=64)
    last_name = models.CharField(verbose_name='Nachname', max_length=64)
    cost_rate = models.IntegerField(verbose_name='Kostensatz', default=80)
    group = models.ForeignKey(EmployeeGroup, verbose_name='Gruppe', related_name='employees')

    class Meta:
        verbose_name = 'Mitarbeiter'
        verbose_name_plural = 'Mitarbeiter'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class MachineType(models.Model):
    name = models.CharField(verbose_name='Bezeichnung', max_length=64)

    class Meta:
        verbose_name = 'Maschinentyp'
        verbose_name_plural = 'Maschinentypen'

    def __str__(self):
        return self.name


class Machine(models.Model):
    number = models.IntegerField(verbose_name='Nummer')
    description = models.CharField(verbose_name='Bezeichnung', max_length=64)
    project = models.ForeignKey(Project, verbose_name='Projekt')
    type = models.ForeignKey(MachineType, verbose_name='Typ', blank=True, null=True)
    active = models.BooleanField(verbose_name='Aktiv', default=True)
    assigned_employees = models.ManyToManyField(Employee, related_name='machines', blank=True)

    class Meta:
        verbose_name = 'Kostenträger'
        verbose_name_plural = 'Kostenträger'

    def __str__(self):
        return str(self.number) + ' - ' + str(self.description)

    def material_costs(self):
        total_costs = MaterialCost.objects.filter(machine_id=self.id).aggregate(Sum('amount'))['amount__sum']
        return total_costs if total_costs else 0

    def labour_costs(self):
        total_costs = LabourCost.objects.filter(machine_id=self.id).aggregate(Sum('amount'))['amount__sum']
        return total_costs if total_costs else 0

    def total_costs(self):
        return self.material_costs() + self.labour_costs()


class Comment(models.Model):
    text = models.CharField(verbose_name='Text', max_length=200)

    class Meta:
        verbose_name = 'Kommentar'
        verbose_name_plural = 'Kommentare'

    def __str__(self):
        return self.text


class LabourCost(models.Model):
    employee = models.ForeignKey(Employee, on_delete=DO_NOTHING)
    machine = models.ForeignKey(Machine, verbose_name='Kostenträger', on_delete=DO_NOTHING, null=True)
    date = models.DateField(verbose_name='Datum')
    duration = models.IntegerField(verbose_name='Dauer (Minuten)')
    comment = models.ForeignKey(Comment, verbose_name='Kommentar', blank=True, null=True)
    amount = models.FloatField(verbose_name="Betrag")

    class Meta:
        verbose_name = 'Arbeitsaufwand'
        verbose_name_plural = 'Arbeitsaufwände'

    def __str__(self):
        return str(self.date) + ' - ' + str(self.employee)


class MaterialCost(models.Model):
    machine = models.ForeignKey(Machine, verbose_name='Kostenträger', on_delete=DO_NOTHING)
    description = models.CharField(verbose_name='Bezeichnung', max_length=200)
    amount = models.FloatField(verbose_name="Betrag")

    class Meta:
        verbose_name = 'Materialaufwand'
        verbose_name_plural = 'Materialaufwände'

    def __str__(self):
        return str(self.machine.id) + ' - ' + str(self.description)


class Earning(models.Model):
    type = models.CharField(verbose_name='Typ', default='d', max_length=1,
                            choices=[('a', 'Maschine'), ('b', 'Ersatzteil'), ('c', 'Service'), ('d', 'Sonstiges')])
    project = models.ForeignKey(Project, verbose_name='Projekt')
    description = models.CharField(verbose_name='Bezeichnung', max_length=200)
    amount = models.FloatField(verbose_name="Betrag")

    class Meta:
        verbose_name = 'Erlös'
        verbose_name_plural = 'Erlöse'
