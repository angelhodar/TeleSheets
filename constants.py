ONLY_ADMIN = 'Solo un administrador puede ejecutar este comando'
ONLY_GROUPS = 'Este comando solo está disponible en los grupos'
INVALID_SHEET = 'El link a la hoja de google no es válido. Asegurate de copiarlo bien y vuelve a ejecutar el comando de nuevo'
BOT_ADMIN = 'El bot debe ser administrador para ejecutar este comando'
NO_DB_GROUP = 'No has enlazado tu Google Sheet todavia!. Usa /config para ver cómo hacerlo'
GROUP_CREATED = 'El grupo ha sido configurado con éxito!'
SHEET_UPDATED = 'La hoja ha sido actualizada con éxito!'
CONFIG_SUCCESSFUL = 'Tu grupo está configurado satisfactoriamente! Ahora solo necesitas invitar al resto de la gente :)'

CONFIG_MESSAGE = message = (
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
    " Y con eso ya habrias configurado tu grupo! Si quieres informacíon sobre todos los comandos que tengo para ofrecerte,"
    " usa /ayuda"
)