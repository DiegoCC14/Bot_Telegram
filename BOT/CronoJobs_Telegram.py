from telegram import Bot

import sys , os , asyncio
from pathlib import Path


PATH_FOLDER_SESSIONS = Path(__file__).resolve().parent.parent/'SESSIONS'


async def send_msg( bot , chat_id , mensaje ):
    await bot.send_message(chat_id=chat_id, text=mensaje)

async def main( token_bot ):
    bot = Bot( token=token_bot )
    chat_id = '1039891636'
    mensaje = 'Mensaje Iniciado por Bot -->>'

    await send_msg( bot , chat_id , mensaje )
    

if __name__ == "__main__":
    
    Folder_User = sys.argv[1]
    Token_Bot = sys.argv[2]
    Token_Bot = '5974349719:AAH_MzTXkyfwkpiBUEk-48IQgbJPTIlA3Dk'

    if os.path.exists( PATH_FOLDER_SESSIONS/Folder_User ):
        asyncio.run(main( Token_Bot ))
    else:
        print( f'ERROR: Carpeta Usuario "{PATH_FOLDER_SESSIONS/Folder_User}" No Existente' )