from django.contrib import admin
from app01.models import PedigreeMPTT, PedigreeTree, Sire, Dam, PlantTree, Plantation
from mptt.admin import MPTTModelAdmin
# Register your models here.
# app01/admin.py
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import germplasm, pedigree
from import_export.admin import ImportExportModelAdmin


class GermResource(resources.ModelResource):
    class Meta:
        model = germplasm


class GermAdmin(ImportExportModelAdmin):
    resource_classes = [GermResource]


class PedigreeResource(resources.ModelResource):
    class Meta:
        model = pedigree


class PedigreeAdmin(ImportExportModelAdmin):
    resource_classes = [PedigreeResource]


class TreeResource(resources.ModelResource):
    sire = fields.Field(
        column_name='Sire',
        attribute='Sire',
        widget=ForeignKeyWidget(Sire, 'Sire'))
    dam = fields.Field(
        column_name='Dam',
        attribute='Dam',
        widget=ForeignKeyWidget(Dam, 'Dam'))

    class Meta:
        model = PedigreeTree
        fields = ('id', 'germ_id', 'sire', 'dam',)


class TreeAdmin(ImportExportModelAdmin):
    resource_classes = [TreeResource]


class SireResource(resources.ModelResource):
    class Meta:
        model = Sire


class SireAdmin(ImportExportModelAdmin):
    resource_classes = [SireResource]


class DamResource(resources.ModelResource):
    class Meta:
        model = Dam


class DamAdmin(ImportExportModelAdmin):
    resource_classes = [DamResource]


class PlantTestResource(resources.ModelResource):
    p_id = fields.Field(
        column_name='p_id',
        attribute='p_id',
        widget=ForeignKeyWidget(Plantation, 'p_id'))

    class Meta:
        model = PlantTree
        fields = ('id', 'p_id', 'year', 'Height', 'dbh', 'volume_of_wood')


class PlantTestAdmin(ImportExportModelAdmin):
    resource_classes = [PlantTestResource]


class PlantationResource(resources.ModelResource):
    class Meta:
        model = Plantation


class PlantationAdmin(ImportExportModelAdmin):
    resource_classes = [PlantationResource]


admin.site.register(germplasm, GermAdmin)
admin.site.register(PedigreeTree, TreeAdmin)
admin.site.register(pedigree, PedigreeAdmin)
admin.site.register(PedigreeMPTT, MPTTModelAdmin)
admin.site.register(Sire, SireAdmin)
admin.site.register(Dam, DamAdmin)
admin.site.register(Plantation, PlantationAdmin)
admin.site.register(PlantTree, PlantTestAdmin)
