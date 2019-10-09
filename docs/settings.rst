Custom Settings
===============

Once you have configured the most important and sensible data of your app, now the last thing is to
adjust the rest of the app settings to your needs. All the settings are stored in the ``constants.py``
located in the ``telesheets\config`` directory. These variables are grouped by usability so lets explain
each group and its variables:

Commands
--------

The values of this variables will define the text that the user needs to put in telegram with the / character to
invoke each command (for example */start* or */commands*). These are:

* ``START``: Shows simple start message.
* ``CONFIG``: Tells the administrator how to connect and configure the group with Google Sheets.
* ``COMMANDS``: Shows a message with all the available commands.
* ``SHEET``: Configures the sheet url passed by parameter for the group where it is invoked.
* ``CHECK``: Tells the administrator if there is any extra configuration needed.
* ``EMAIL``: Shows the bot email used to share the group admin's Google Sheet.
* ``CALENDAR``: Shows the calendar of nearby events.
* ``ATTENDANCE``: Sends the attendance to the student.
* ``GRADES``: Sends the grades to the student.

.. Note:: In the case of ``ATTENDANCE`` and ``GRADES`` the info is sent by private message to the student instead
    of showing the data in a group message. The way the commands send the data varies depending on who invoked the command:

    * If invoked by the **group admin**, each student will receive a private message with their grades.
    * If invoked by a **student**, only that particular student will receive the grades.

Sheet
-----

When working with your Google Sheet, the app needs to know some data about your worksheets:

* ``GRADES_WKS_NAME``: The name of your grades worksheet.
* ``ATTENDANCE_WKS_NAME``: The name of your attendance worksheet.
* ``CALENDAR_WKS_NAME``: The name of your calendar worksheet.
* ``IGNORE_HEADERS``: A dict containing a list of header names that will be ignored when sending data to students. For example,
  you need a header called ``Telegram`` in your grades and attendance worksheet for the bot to identify each student, but you dont need to send
  that info to the students.


Messages
--------

There are some messages that will be sent to the group while configuring it or invoking some commands that always shows
the same message (like the commands list for example).

Errors
******

* ``COMMAND_ONLY_ADMINS``: Showed if a non-admin group member executes a command that requires admin privilege.
* ``URL_ERROR``: If the passed sheet url to the ``SHEET`` command is not a Google Sheet.
* ``INVALID_SHEET``: The url passed has the Google Sheet url format but the sheet is not valid.
* ``NO_BOT_ADMIN``: Showed when invoking a command and the bot doesnt have admin privileges in the group.
* ``NO_SHEET``: If the group doesnt have a sheet configured.

Confirmations
*************

* ``SHEET_UPDATED``: Showed when using the ``SHEET`` command succesfully.
* ``CONFIG_SUCCESSFUL``: Showed when everything is well configured and there is nothing more to do.
* ``GRADES_SENT``: Showed when an admin invokes the ``GRADES`` command.

Commands
********

* ``START_PRIVATE``: Shoed when invoking ``START`` in a private conversation.
* ``START_GROUP``: Showed when invoking ``START`` in a group.
* ``COMMANDS_LIST``: Showed when invoking ``COMMANDS``.
* ``CONFIG_MESSAGE``: Showed when invoking ``CONFIG``.
