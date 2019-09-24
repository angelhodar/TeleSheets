from emoji import emojize

# The text needed to execute each command
START = 'start'
CONFIG = 'config'
COMMANDS = 'comandos'
SHEET = 'hoja'
CHECK = 'comprobar'
EMAIL = 'email'
CALENDAR = 'calendario'
ATTENDANCE = 'asistencia'
GRADE = 'nota'
GRADES = 'notas'

# The names you are going to give to your worksheets
GRADES_WKS_NAME = 'Notas'
ATTENDANCE_WKS_NAME = 'Asistencia'
CALENDAR_WKS_NAME = 'Calendario'

# Headers that will be ignored when parsing the corresponding worksheet
GRADES_IGNORED_HEADERS = ['Telegram']
ATTENDANCE_IGNORED_HEADERS = ['Telegram']
CALENDAR_IGNORED_HEADERS = []

# Errors
COMMAND_ONLY_ADMINS = emojize('Solo un administrador puede ejecutar este comando :cop:', use_aliases=True)
URL_ERROR = emojize('El link no es una Google Sheet :x:', use_aliases=True)
INVALID_SHEET = emojize('El link a la hoja de google no es válido :x: Asegurate de copiarlo bien y vuelve a ejecutar el comando de nuevo', use_aliases=True)
NO_BOT_ADMIN = emojize('Debes darme permisos de administrador del grupo para ejecutar este comando :cop:', use_aliases=True)
NO_SHEET = emojize('No has enlazado tu Google Sheet todavia! :x: Usa /config para ver cómo hacerlo :clipboard:', use_aliases=True)

# Confirmations
SHEET_UPDATED = emojize('La hoja ha sido actualizada con éxito! :white_check_mark:', use_aliases=True)
CONFIG_SUCCESSFUL = emojize('Tu grupo está configurado satisfactoriamente! :white_check_mark: Ahora solo necesitas invitar al resto de la gente :)', use_aliases=True)
GRADES_SENT = emojize(':bell: Todas las notas han sido enviadas :bell:', use_aliases=True)

# Static messages for some commands
START_PRIVATE = emojize('¡Hola! :smile: Ahora te mandaré tus notas y asistencia por aqui cuando tu o tu profesor lo soliciteis :loudspeaker:', use_aliases=True)
START_GROUP = emojize(
    "¡Hola! :smile: Antes de nada, asegúrate de darme permisos de administrador! Cuando lo hayas hecho "
    "escribe /config para empezar a enlazar este grupo con tu Google Sheet", use_aliases=True)
COMMANDS_LIST = emojize(
    ":smile: /start - Muestra un mensaje de bienvenida y los primeros pasos para configurar tu grupo.\n"
    ":wrench: /config - Tutorial de como enlazar y configurar el grupo con tu Google Sheet.\n"
    ":clipboard: /comandos - Muestra este mensaje\n"
    ":page_facing_up: /hoja <url> - Enlaza tu Google Sheet con tu grupo (necesitas darle la url)\n"
    ":mag: /comprobar - Comprueba que todo está configurado correctamente y en caso contrario te avisa de lo que falte por hacer\n"
    ":e-mail: /email - Te envia el email que debes usar para compartir tu Google Sheet\n"
    ":calendar: /calendario - Muestra todos los examenes y tareas pendientes\n"
    ":raising_hand: /asistencia - El miembro del grupo que lo ejecute obtendrá un listado de su asistencia a clase\n"
    ":100: /nota - El miembro del grupo que lo ejecute obtendrá un listado de sus notas\n"
    ":bell: /notas - Envía a todos los miembros del grupo un mensaje privado con el listado de notas actualizado\n"
, use_aliases=True)
CONFIG_MESSAGE = emojize(
    "Para configurar tu grupo y enlazarlo con tu Google Sheet tan solo debes seguir estos pasos :clipboard:\n"
    "1. Usa el comando /email y copia el el email que obtendrás, lo usarás luego para compartir tu Google Sheet conmigo.\n"
    "2. Ve a tu Google Drive, crea tu hoja y ábrela.\n" 
    "3. Ahora debes compartir la hoja conmigo usando el email que has copiado antes. Si estás haciendo esto desde el navegador, "
    "verás un botón verde arriba a la derecha que pone 'Compartir, simplemente haz click, introduce mi email en la caja que aparece y "
    "asegúrate de darme solo el permiso 'Puede ver' para que tu hoja solo la puedas modificar tu (para que te fies de mi :smile:).\n"
    "4. Dale al boon 'Listo' y ya has terminado de configurar tu Google Sheet!\n"
    "5. Ahora copia la url de la hoja (puedes hacerlo desde la propia barra del navegador o si vuelves a pulsar el botón 'Compartir' "
    "también aparecerá ahi junto con un botón para copiar la url\n"
    "6. Cuando lo tengas copiado, simplemente pon aqui en el chat el comando /hoja <url>, sustituyendo <url> con el link de tu hoja.\n\n"
    "Y con eso ya habrias configurado tu grupo! :white_check_mark: Puedes usar el comando /comprobar para asegurarte de que no te dejas "
    "nada por hacer :mag: Si quieres informacíon sobre todos los comandos que tengo para ofrecerte, usa /comandos :clipboard:"
, use_aliases=True)