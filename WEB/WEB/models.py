from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class table_User_Data( models.Model ):
	id = models.AutoField(primary_key=True)
	id_user = models.ForeignKey( User , on_delete=models.CASCADE ) 
	folder_session = models.CharField( max_length=200 )
	fecha_creacion = models.DateTimeField( default=datetime.now() )
	fecha_modificacion = models.DateTimeField( default=datetime.now() )

	class Meta:
		db_table='User_Data'


class table_Respuestas_Automaticas( models.Model ):
	id = models.AutoField(primary_key=True)
	id_user_data = models.ForeignKey( table_User_Data , on_delete=models.CASCADE ) 
	name_file = models.CharField( max_length=200 )
	fecha_creacion = models.DateTimeField( default=datetime.now() )

	class Meta:
		db_table='Respuestas_Automaticas'


class table_CronoJobs( models.Model ):
	id = models.AutoField(primary_key=True)
	id_user_data = models.ForeignKey( table_User_Data , on_delete=models.CASCADE ) 
	folder_cronojob = models.CharField( max_length=200 )
	name_file = models.CharField( max_length=200 , blank=True )
	estado = models.CharField( max_length=200 )
	fecha_ejecusion = models.DateTimeField()
	fecha_creacion = models.DateTimeField( default=datetime.now() )

	class Meta:
		db_table='CronoJobs'