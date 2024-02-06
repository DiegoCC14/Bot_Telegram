from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views import View
from django.urls import reverse
from django.utils import timezone

from .models import table_User_Data , table_Respuestas_Automaticas , table_CronoJobs

from Config.settings import BASE_DIR , PATH_FOLDER_SESSIONS
from .services.ETL_Data import Genera_JSON_Excel_Valido , Genera_JSON_Excel_CronoJobs_Valido

import shutil , os , string , secrets , json , zipfile , random , string
from datetime import datetime
from pathlib import Path


class Home_Bot_Telegram( View ):
    def get( self , request ):
        return render( request , 'home.html' )


class Files( View ):
    
    def get(  self , request  ):
        try:
            
            obj_Data_User = table_User_Data.objects.filter( id_user=request.user ).first()
            
            Folder_User = obj_Data_User.folder_session
            PATH_FOLDER_USER = PATH_FOLDER_SESSIONS/Folder_User

            path_files_json = PATH_FOLDER_USER/'MEDIA_FILES.json'
            response = HttpResponse( open( path_files_json, 'rb' ) , content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="Archivos_Subidos.json"'
            
            return response
        except:
            return JsonResponse( {'Mensaje': 'Error al Descargar Carpeta.'} , status=400 )

    def post( self , request ):
        try:

            files = request.FILES.getlist('archivos')
            
            if len( files ) > 0:
                
                obj_Data_User = table_User_Data.objects.filter( id_user=request.user ).first()
                
                Folder_User = obj_Data_User.folder_session
                PATH_FOLDER_USER = PATH_FOLDER_SESSIONS/Folder_User
                PATH_MEDIA_FILES = PATH_FOLDER_SESSIONS/Folder_User/'MEDIA_FILES'
                
                # Cargamos los archivos en la carpeta MEDIA_FILES ----->>>>>>>>>>>>
                for file in files:
                    try:
                        with open( PATH_MEDIA_FILES/str(file) , 'wb') as PATH_FILE:
                            for trozo in file.chunks():
                                PATH_FILE.write(trozo)
                    except:
                        pass
                # ----------------------------------------------------->>>>>>>>>>>>
                
                # Actualizamos los archivos de carpeta MEDIA_FILES ---->>>>>>>>>>>>
                files_MEDIA_FILES = os.listdir( PATH_MEDIA_FILES )
                with open( PATH_FOLDER_USER/'MEDIA_FILES.json' , 'w' ) as FileJSON:
                    json.dump( { 'archivos' : files_MEDIA_FILES } , FileJSON )
                # ----------------------------------------------------->>>>>>>>>>>>

            return redirect( 'home' )
        except :
            return JsonResponse( {'Mensaje': 'Error al Subir Archivos.'} , status=400 )


class Respuesta_Automatica( View ):
    
    def get( self , request ):
        try:
            obj_Data_User = table_User_Data.objects.filter( id_user=request.user ).first()
            dicc_registro_resp_automaticas = {}
            if table_Respuestas_Automaticas.objects.filter( id_user_data=obj_Data_User ).exists():
                dicc_registro_resp_automaticas = list( table_Respuestas_Automaticas.objects.filter( id_user_data=obj_Data_User ).values() )[0]
                dicc_registro_resp_automaticas['fecha_creacion'] = str( dicc_registro_resp_automaticas['fecha_creacion'] )

            return JsonResponse( {'respuesta': [dicc_registro_resp_automaticas] } , status=200 )
        except:
            return JsonResponse( {'Mensaje': 'Error Obteniendo Regitros Respuestas Automaticas.'} , status=400 )
    
    def post( self , request ):
        try:
            
            file = request.FILES.get('Excel_Respuesta_Automatica')

            if file != None and str(file).split(".")[-1].lower() == "xlsx":
                
                obj_Data_User = table_User_Data.objects.filter( id_user=request.user ).first()

                Folder_User = obj_Data_User.folder_session
                PATH_FOLDER_USER = PATH_FOLDER_SESSIONS/Folder_User
                
                # Cargamos los archivos en la carpeta MEDIA_FILES ----->>>>>>>>>>>>
                with open( PATH_FOLDER_USER/str(file)  , 'wb') as PATH_FILE_XLSX:
                    for trozo in file.chunks():
                        PATH_FILE_XLSX.write(trozo)
                # ----------------------------------------------------->>>>>>>>>>>>
                
                # Analizamos y Generamos JSON con los datos ----------->>>>>>>>>>>>
                Path_Excel = PATH_FOLDER_USER/str(file)
                fila_inicial = 2
                Path_Excel_Salida = PATH_FOLDER_USER/'Respuestas_Automaticas.xlsx' 
                Path_JSON_Salida = PATH_FOLDER_USER/'Respuestas_Automaticas.json'
                Lista_Archivos_Disponibles = []
                if Path( PATH_FOLDER_USER/'MEDIA_FILES.json' ).exists():
                    with open( PATH_FOLDER_USER/'MEDIA_FILES.json' , 'r') as archivo_json:
                        Lista_Archivos_Disponibles = json.load(archivo_json)['archivos']
                Genera_JSON_Excel_Valido( Path_Excel , fila_inicial , Path_Excel_Salida , Path_JSON_Salida , Lista_Archivos_Disponibles )
                # ----------------------------------------------------->>>>>>>>>>>>

                # Actualizamos la DB con el nuevo registro ------------>>>>>>>>>>>>
                if table_Respuestas_Automaticas.objects.filter( id_user_data=obj_Data_User ).exists():
                    obj_Respuesta_Automatica = table_Respuestas_Automaticas.objects.filter( id_user_data=obj_Data_User ).first()
                    obj_Respuesta_Automatica.name_file=str(file)
                    obj_Respuesta_Automatica.fecha_creacion = datetime.now()
                    obj_Respuesta_Automatica.save()
                else:
                    table_Respuestas_Automaticas( id_user_data=obj_Data_User , name_file=str(file) , fecha_creacion=datetime.now() ).save()
                # ----------------------------------------------------->>>>>>>>>>>>
            return redirect( 'home' )
        except :
            return JsonResponse( {'Mensaje': 'Error al Subir Excel Repuesta Automatica.'} , status=400 )


class Respuesta_Automatica_Files( View ):

    def get( self , request ):
        try:
            obj_Data_User = table_User_Data.objects.filter( id_user=request.user ).first()
            
            Folder_User = obj_Data_User.folder_session
            PATH_FOLDER_USER = PATH_FOLDER_SESSIONS/Folder_User
            
            obj_Respuesta_Automatica = table_Respuestas_Automaticas.objects.filter( id_user_data=obj_Data_User ).first()
            
            Lista_Archivos = []
            for archivo in ['Respuestas_Automaticas.xlsx',obj_Respuesta_Automatica.name_file]:
                if Path( PATH_FOLDER_USER/archivo ).exists():
                    Lista_Archivos.append( PATH_FOLDER_USER/archivo )

            if os.path.exists( PATH_FOLDER_USER/'Comprimidos' ):
                shutil.rmtree( PATH_FOLDER_USER/'Comprimidos' )
            os.mkdir( PATH_FOLDER_USER/'Comprimidos' )
            for archivo in Lista_Archivos:
                shutil.copy( archivo , PATH_FOLDER_USER/'Comprimidos' )
            
            shutil.make_archive( str( PATH_FOLDER_USER/'Comprimidos' ) , 'zip', str( PATH_FOLDER_USER/'Comprimidos' ) )

            response = HttpResponse( open( PATH_FOLDER_USER/'Comprimidos.zip' , 'rb' ), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="Files_Respuesta.zip"'
            
            # Borramos los comprimidos generados ---->>>>>>>>>
            os.remove( PATH_FOLDER_USER/'Comprimidos.zip' )
            shutil.rmtree( PATH_FOLDER_USER/'Comprimidos' )
            # --------------------------------------->>>>>>>>>
            
            return response

        except Exception as error:
            print( error )
        
        return JsonResponse( {'Mensaje': 'Error al Descargar Carpeta.'} , status=400 )


class CronoJobs( View ):
    
    def post( self , request ):
        
        try:
            
            file = request.FILES.get('Excel_CronoJobs')

            if file != None and str(file).split(".")[-1].lower() == "xlsx":
                
                obj_Data_User = table_User_Data.objects.filter( id_user=request.user ).first()

                Folder_User = obj_Data_User.folder_session
                PATH_FOLDER_USER = PATH_FOLDER_SESSIONS/Folder_User

                # Obtenemos las Fechas ------------------------------->>>>>>>>>>>>
                
                date = request.POST.get('date')
                time = request.POST.get('time')
                fecha_ejecusion = datetime.strptime( f'{date} T{time}' , "%Y-%m-%d T%H:%M" )
                # ----------------------------------------------------->>>>>>>>>>>>

                Carpeta_Cronojobs = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                os.mkdir( PATH_FOLDER_USER/'CRONOJOBS'/Carpeta_Cronojobs )

                # Cargamos los archivos en la carpeta MEDIA_FILES ----->>>>>>>>>>>>
                with open( PATH_FOLDER_USER/'CRONOJOBS'/Carpeta_Cronojobs/str(file)  , 'wb') as PATH_FILE_XLSX:
                    for trozo in file.chunks():
                        PATH_FILE_XLSX.write(trozo)
                # ----------------------------------------------------->>>>>>>>>>>>
                
                # Analizamos y Generamos JSON con los datos ----------->>>>>>>>>>>>
                Path_Excel = PATH_FOLDER_USER/'CRONOJOBS'/Carpeta_Cronojobs/str(file)
                fila_inicial = 2
                Path_Excel_Salida = PATH_FOLDER_USER/'CRONOJOBS'/Carpeta_Cronojobs/'Cronojobs_Validado.xlsx'
                Path_JSON_Salida = PATH_FOLDER_USER/'CRONOJOBS'/Carpeta_Cronojobs/'Cronojobs_Validado.json'
                Lista_Archivos_Disponibles = []
                if Path( PATH_FOLDER_USER/'MEDIA_FILES.json' ).exists():
                    with open( PATH_FOLDER_USER/'MEDIA_FILES.json' , 'r') as archivo_json:
                        Lista_Archivos_Disponibles = json.load(archivo_json)['archivos']
                Genera_JSON_Excel_CronoJobs_Valido( Path_Excel , fila_inicial , Path_Excel_Salida , Path_JSON_Salida , Lista_Archivos_Disponibles )
                # ----------------------------------------------------->>>>>>>>>>>>
                
                # Actualizamos la DB con el nuevo registro ------------>>>>>>>>>>>>
                table_CronoJobs( 
                    id_user_data = obj_Data_User ,
                    folder_cronojob = Carpeta_Cronojobs ,
                    name_file = str(file) ,
                    estado ='en_cola' ,
                    fecha_ejecusion = fecha_ejecusion ).save()
                # ----------------------------------------------------->>>>>>>>>>>>
                
            return redirect( 'home' )
        except :
            return JsonResponse( {'Mensaje': 'Error al Subir Excel Repuesta Automatica.'} , status=400 )

    def get( self , request ):
        try:
            obj_Data_User = table_User_Data.objects.filter( id_user=request.user ).first()
            list_CronoJobs = []
            list_obj_CronoJobs = table_CronoJobs.objects.filter( id_user_data=obj_Data_User )
            for obj_CronoJob in list_obj_CronoJobs:
                list_CronoJobs.append( { 'id':obj_CronoJob.id , 'name_file':obj_CronoJob.name_file,
                        'fecha_ejecusion':str(obj_CronoJob.fecha_ejecusion) , 'fecha_creacion':str(obj_CronoJob.fecha_creacion),
                        'estado':obj_CronoJob.estado} )
                
            return JsonResponse( {'respuesta': list_CronoJobs } , status=200 )
        except:
            return JsonResponse( {'Mensaje': 'Error Obteniendo Regitros Respuestas Automaticas.'} , status=400 )