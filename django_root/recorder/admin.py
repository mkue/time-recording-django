from django.apps import apps
from django.contrib import admin

from recorder.models import Employee, Project, Comment, LabourCost, Machine, MachineType, Earning, MaterialCost

# Register your models here.

app = apps.get_app_config('recorder')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    ordering = ('first_name',)


class ProjectMachineInline(admin.TabularInline):
    model = Machine
    fk_name = 'project'
    extra = 0
    can_delete = False
    exclude = ['assigned_employees', 'active']
    readonly_fields = ['labour_costs', 'material_costs', 'total_costs']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('number', 'description')
    search_fields = ('number', 'description')
    ordering = ('-number',)
    readonly_fields = ('total_costs',)

    inlines = [
        ProjectMachineInline,
    ]


@admin.register(LabourCost)
class LabourCostAdmin(admin.ModelAdmin):
    list_display = ('date', 'employee', 'duration', 'machine', 'comment')
    ordering = ('-date',)
    list_filter = ('comment',)


class MachineLabourCostInline(admin.TabularInline):
    model = LabourCost
    fk_name = 'machine'
    extra = 0


class MachineMaterialCostInline(admin.TabularInline):
    model = MaterialCost
    fk_name = 'machine'
    extra = 0


@admin.register(MaterialCost)
class MaterialCostAdmin(admin.ModelAdmin):
    list_display = ('machine', 'description', 'amount')
    ordering = ('-machine',)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'active')
    ordering = ('-number',)
    list_filter = ('type', 'active')
    list_editable = ('active',)
    search_fields = ('number',)

    readonly_fields = ('material_costs', 'labour_costs', 'total_costs')

    inlines = [
        MachineLabourCostInline,
        MachineMaterialCostInline
    ]


@admin.register(MachineType)
class MachineTypeAdmin(admin.ModelAdmin):
    ordering = ('name',)


admin.site.register(Comment)
admin.site.register(Earning)
