from django.contrib import admin
from .models import table_User_Data , table_Respuestas_Automaticas , table_CronoJobs


class Admin_User_Data(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'folder_session','fecha_creacion','fecha_modificacion')
    search_fields = ('folder_session',)
admin.site.register( table_User_Data , Admin_User_Data)


class Admin_Respuestas_Automaticas(admin.ModelAdmin):
    list_display = ('id', 'id_user_data', 'name_file','fecha_creacion')
    search_fields = ('name_file',)
admin.site.register( table_Respuestas_Automaticas , Admin_Respuestas_Automaticas)


class Admin_table_CronoJobs(admin.ModelAdmin):
    list_display = ('id', 'id_user_data', 'folder_cronojob','name_file','estado','fecha_ejecusion','fecha_creacion')
    search_fields = ('folder_cronojob','estado')
admin.site.register( table_CronoJobs , Admin_table_CronoJobs)