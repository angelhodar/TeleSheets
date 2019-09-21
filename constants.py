from emoji import emojize

# Configuration
BOTNAME = 'TeleSpreadSheetsBot'
GRADES_WKS_NAME = 'Notas'
ASISTENCE_WKS_NAME = 'Asistencia'
CALENDAR_WKS_NAME = 'Calendario'

# Verification
SHEET_URL_FORMAT = 'docs.google.com/spreadsheets/d/'

# Warnings
ONLY_ADMIN = emojize('Solo un administrador puede ejecutar este comando :cop:', use_aliases=True)
ONLY_GROUPS = emojize('Este comando solo está disponible en los grupos :family:', use_aliases=True)
URL_ERROR = emojize('El link no es una Google Sheet :x:', use_aliases=True)
INVALID_SHEET = emojize('El link a la hoja de google no es válido :x: Asegurate de copiarlo bien y vuelve a ejecutar el comando de nuevo', use_aliases=True)
BOT_ADMIN = emojize('Debes darme permisos de administrador del grupo para ejecutar este comando :cop:', use_aliases=True)
NO_SHEET = emojize('No has enlazado tu Google Sheet todavia! :x: Usa /config para ver cómo hacerlo :clipboard:', use_aliases=True)

# Confirmations
GROUP_CREATED = emojize('El grupo ha sido configurado con éxito! :white_check_mark:', use_aliases=True)
SHEET_UPDATED = emojize('La hoja ha sido actualizada con éxito! :white_check_mark:', use_aliases=True)
CONFIG_SUCCESSFUL = emojize('Tu grupo está configurado satisfactoriamente! :white_check_mark: Ahora solo necesitas invitar al resto de la gente :)', use_aliases=True)
GRADES_SENT = emojize('Todas las notas han sido enviadas :bell:', use_aliases=True)

# Commands
START_MESSAGE = emojize('¡Hola! :smile: Escribe /config para empezar a enlazar este grupo con tu Google Sheet', use_aliases=True)
# TODO: Añadir emojis aqui y poner lista de tareas en vez de párrafos
CONFIG_MESSAGE = emojize(
    "Para empezar a configurar tu grupo y enlazarlo con tu Google Sheet, primero"
    " debes crearla en tu Google Drive. Una vez lo hayas hecho, ábrela y verás que hay un botón"
    " verde arriba a la derecha que pone 'Compartir'. Antes de compartir tu hoja conmigo, necesitas"
    " mi email. Para ello, primero usa el comando /email y simplemente deberás copiar el"
    " email que obtendrás, es un email un poco extraño pero no te preocupes :)\n\n"
    "Cuando lo tengas copiado, ahora si debes darle al boton de Compartir en tu hoja"
    " , introducir mi email y luego darle a Listo.\n\n"
    "Ya casi hemos terminado! Solo necesitas copiar el link de la hoja (puedes hacerlo desde la barra"
    " del propio navegador o de nuevo si le das al boton de Compartir verás un boton que dice Copiar enlace)."
    " Cuando lo tengas copiado, simplemente pon aqui en el chat el comando /hoja <url>, donde <url> es el link de tu hoja.\n\n"
    " Y con eso ya habrias configurado tu grupo! Puedes usar el comando /comprobar para asegurarte de que no te dejas nada por hacer."
    " Si quieres informacíon sobre todos los comandos que tengo para ofrecerte, usa /comandos"
, use_aliases=True)
COMMANDS_LIST = emojize(
    ":smile: /start - Muestra un mensaje de bienvenida y los primeros pasos para configurar tu grupo.\n"
    ":wrench: /config - Tutorial de como enlazar y configurar el grupo con tu Google Sheet.\n"
    ":clipboard: /comandos - Muestra este mensaje\n"
    ":page_facing_up: /hoja <url> - Enlaza tu hoja de Google Sheet con tu grupo (necesitas darle la url)\n"
    ":mag: /comprobar - Comprueba que todo está configurado correctamente y en caso contrario te avisa de lo que falte por hacer\n"
    ":e-mail: /email - Te envia el email que debes usar para compartir tu Google Sheet\n"
    ":calendar: /calendario - Muestra todos los examenes y tareas pendientes\n"
    ":raising_hand: /asistencia - El miembro del grupo que lo ejecute obtendrá un listado de su asistencia a clase\n"
    ":100: /nota - El miembro del grupo que lo ejecute obtendrá un listado de sus notas\n"
    ":bell: /notas - Envía a todos los miembros del grupo un mensaje privado con el listado de notas actualizado\n"
, use_aliases=True)