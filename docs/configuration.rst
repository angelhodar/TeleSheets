Configuration
=============

Getting the project
-------------------

The first thing you need to do to start configuring the project is cloning it from GitHub using
the following commands:

.. code-block:: bash

    $ git clone https://github.com/angelhodar/TeleSheets
    $ cd TeleSheets

Once you have done it, then you need to install all the dependencies for this project. If you use **pipenv** (which you should)
you can just use this command to create a virtual environment and install all the dependencies:

.. code-block:: bash

    $ pipenv install

If you dont use pipenv i have also provided a ``requirements.txt`` so using pip is just like this:

.. code-block:: bash

    $ pip install -r requirements.txt

Environment Vars
----------------

Now that you have your project ready, you need to setup some environment vars listed below.
It is always a good practice to keep sensitive data out of the code, thats why we are using them.
For that, you need to create a ``.env`` file inside the ``telesheets/config`` directory. The vars will
be loaded into python using the python-dotenv module in the ``__init__.py`` of that directory, so you can
just use:

.. code-block:: python

    from telegram.config import <VAR_NAME>

The ``.env`` file should contain the following variables:

Telegram
""""""""

* ``TELEGRAM_BOT_TOKEN``: The token you get when creating your bot talking to **@BotFather** on telegram.
* ``TELEGRAM_API_ID``: The API ID you obtain when creating your own telegram app.
* ``TELEGRAM_API_HASH``: The API Hash you obtain when creating your own telegram app.

To create your telegram app just follow this `link <https://my.telegram.org/>`_. The process is very straightforward, just
remember to save the ``api_id`` and ``api_hash``.

Google Cloud
""""""""""""

* ``CREDENTIALS_PATH`` : The path of your credentials **json** file you get when creating your Google Service Account.

To create your service and get the credentials file you can see `this video <https://www.youtube.com/watch?v=cnPlKLEGR7E/>`_
that shows all the process (just until minute 3:00) 

Database
""""""""

* ``DB_USER`` : The user of your db.
* ``DB_PASSWORD`` : The password for that particular user.
* ``DB_NAME`` : The name you want to give to the database when everything is going to be saved.
* ``DB_HOST`` : URI-style host of your db. For example if using mongodb and localhost
  it would be *mongodb://localhost/db_name*. If that URI contains **user**, **password** or the **db_name** keywords,
  they will be parsed with your ``DB_USER``, ``DB_PASSWORD`` and ``DB_NAME`` values.

Before reading the following paragraphs, you should know that every database relation within the bot is collapsed in the ``db.py``
module, so the way you handle the functions there to interact with the database is completely up to you, so you could simply use the
`TinyDB <https://tinydb.readthedocs.io/en/latest/intro.html>`_ python module, but i would recommend to only use it for playing with the
system as it doesnt support important database properties. I also wanted to learn NoSQL so you would probably see that the modules used
are too much for the simple use i have done with them. With that said, you can continue reading :)

The database system used in this project is `MongoDB <https://www.mongodb.com/es>`_ using `mongoengine <http://mongoengine.org/>`_ as ORM.
In order to use mongo, you need to install it to run in your localhost with the following command:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install -y mongod
    $ sudo systemctl status mongodb

MongoDB also has a nice GUI client which i recommend you to install to have a nice view of your db:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install -y mongod

You can check if its running with the following command:

.. code-block:: bash

    $ sudo systemctl status mongodb

There is another option if you want to avoid installing anything on your computer, which is signing up on the cloud service
`MongoDB Atlas <https://www.mongodb.com/cloud/atlas>`_, which gives you a 512MB free cluster! (its something).
