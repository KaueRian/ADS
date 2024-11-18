from lib2to3.btm_utils import reduce_tree

from django.contrib import admin
from .models import New


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'slug', '_autor', 'criado', 'status']
    prepopulated_fields = {'slug': ('titulo',)}
    list_filter = ['autor', 'status', 'criado']
    list_editable = ['status']
    search_fields = ['titulo', 'texto']
    raw_id_fields = ('autor',)
    date_hierarchy = 'publicado'
    ordering = ['status', '-publicado']
    exclude = ['autor']

    def _autor(self, instance):
         if instance.autor is not None:
              return instance.autor.get_full_name()
         return 'Sem Autor.'


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            self.exclude = ['autor']
            return queryset.filter(autor=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.autor = request.user
        super().save_model(request, obj, form, change)
