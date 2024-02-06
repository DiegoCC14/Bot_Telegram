from telegram.ext import Updater, CommandHandler
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from pathlib import Path
from PIL import Image
import json , os , sys


PATH_FOLDER_SESSIONS = Path(__file__).resolve().parent.parent/'SESSIONS'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    user = update.effective_user
    user_id = update.message.from_user.id
    print( f'User ID: {user_id}' )
    await update.message.reply_html( rf"Hi {user.mention_html()}!", reply_markup=ForceReply(selective=True), )

async def send_document( update , context , path_document , text_msg ):
    await update.message.reply_document( open( path_document , 'rb') , caption=text_msg)

async def send_image( update, context , path_image , text_msg ):
    await update.message.reply_photo( open(path_image, 'rb') , caption=text_msg)

async def send_text( update, context , text_msg ):
    await update.message.reply_text( text_msg )

def obtener_tipo_archivo( path_file ):
    try:
        Image.open( path_file )
        return 'Imagen'
    except:
        return 'Documento'

async def respuesta_a_mensje( update, context , dicc_respuestas_total , dicc_respuesta , iteracion_num ):

    msg_respuesta = str( dicc_respuesta['mensaje_respuesta'] )
    
    if 'archivo_mensaje' in dicc_respuesta.keys():
        #Enviamos archivo con texto, debemos saber si es imagen o documento
        file = dicc_respuesta['archivo_mensaje']
        path_file = PATH_FOLDER_SESSIONS/Folder_User/'MEDIA_FILES'/file

        if os.path.exists( path_file ):

            tipo_archivo = obtener_tipo_archivo( path_file )
            
            if tipo_archivo == 'Imagen':
                await send_image( update, context , path_file , msg_respuesta )

            elif tipo_archivo == 'Documento':
                await send_document( update , context , path_file , msg_respuesta )
        else:
            msg_respuesta = f'-- Archivo No Encontrado--\n{msg_respuesta}'
            await send_text( update, context , msg_respuesta )

    else:
        #Solo enviamos texto
        await send_text( update, context , msg_respuesta )
    
    if 'redireccionar_a_codigo' in dicc_respuesta.keys() and iteracion_num<3:
        dicc_respuesta = dicc_respuestas_total[ dicc_respuesta['redireccionar_a_codigo'] ]
        await respuesta_a_mensje( update, context , dicc_respuestas_total , dicc_respuesta , iteracion_num+1 )

async def respuesta_automatica( update, context ):

    json_data = json.loads( open( PATH_FOLDER_SESSIONS/Folder_User/'Respuestas_Automaticas.json' , 'rb' ).read() )

    text_msg = update.message.text
    
    if text_msg in json_data.keys():
        await respuesta_a_mensje( update, context , json_data , json_data[text_msg] , 0 )

    elif 'Bienvenida' in json_data.keys():
        await respuesta_a_mensje( update, context , json_data , json_data['Bienvenida'] , 0 )

    else:
        await send_text( update, context , '-- Mensaje sin Coincidencia con algun Codigo --' )

def main( token_bot ):

    application = Application.builder().token( token_bot ).build()
    
    application.add_handler( CommandHandler("start", start) )
    
    application.add_handler( MessageHandler( filters.TEXT & ~filters.COMMAND , respuesta_automatica) )
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    
    Folder_User = sys.argv[1]
    Token_Bot = sys.argv[2]
    Token_Bot = '5974349719:AAH_MzTXkyfwkpiBUEk-48IQgbJPTIlA3Dk'

    if os.path.exists( PATH_FOLDER_SESSIONS/Folder_User ):
        main( Token_Bot )
    else:
        print( f'ERROR: Carpeta Usuario "{PATH_FOLDER_SESSIONS/Folder_User}" No Existente' )