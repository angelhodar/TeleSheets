Configuration
=============

In this section i will show you how to configure your own bot and the Google Cloud service.

Environment Vars
----------------

The first thing to configure is your environment vars to keep your secret credentials out of the code.
For that, you need to create a ``.env`` file inside the ``telesheets/config`` directory. The vars will
be loaded into python using the python-dotenv module in the __init__.py of that directory, so you can
just use:

.. code-block:: python

    from telegram.config import <VAR_NAME>

The ``.env`` file should contain the following variables:

Telegram
""""""""

* ``TELEGRAM_BOT_TOKEN``: The token you get when creating your bot talking to **@BotFather**.
* ``TELEGRAM_API_ID``: The API ID you obtain when creating your own telegram app.
* ``TELEGRAM_API_HASH``: The API Hash you obtain when creating your own telegram app.

To create your telegram app just follow this `link <https://my.telegram.org/>`_

Google Cloud
""""""""""""

* ``CREDENTIALS_PATH`` : The path of your credentials **.json** file you get when creating your Google Service Account.

To create your service follow this `link <https://console.developers.google.com/>`_

Database
""""""""

* ``DB_USER`` : The user of your db.
* ``DB_PASSWORD`` : The password for that particular user.
* ``DB_NAME`` : The name you want to give to the database when everything is going to be saved.
* ``DB_HOST`` : URI-style host of your db. For example if using mongodb and localhost
  it would be *mongodb://localhost/db_name*. If that URI contains **user**, **password** or the **db_name** keywords,
  they will be parsed with your ``DB_USER``, ``DB_PASSWORD`` and ``DB_NAME`` values.