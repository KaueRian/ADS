from django.contrib import admin
from .models import New, Comentario


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
    exclude = ['']

    def _autor(self, instance):
        if instance.autor is not None:
            return instance.autor.get_full_name()
        return 'Sem autor'

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

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('new', '_autor', 'criado', 'ativado')
    list_filter = ('new', 'ativado')
    ordering = ('new', 'ativado')
    list_editable = ['ativado']

    def _autor(self, instance):
        return instance.usuario.get_full_name()
