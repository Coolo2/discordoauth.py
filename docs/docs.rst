
discordoauth.py
===================

Setup
-------------------

discordoauth.py is a PyPi package and can be installed using the following:

``pip install discordoauth.py``

Getting started
-------------------

It is reccomended to create a client at initialisation of the webserver since the application id and secret will not need to be changed.

.. code-block:: python

    import discordoauth 

    client = discordoauth.Client(application_id, "application_secret")


Scopes
~~~~~~~~

Scopes are sent to discord so that the user knows what will be accessed.

It is reccomended to choose your scopes outside of your webserver routes so that they can be used for URL generation.

Supported Scopes 
*********************

bot=True - Adding a bot to a server. Does not affect the library 

identify=True - Identifying the user who authorises. Used with Session.fetch_user()

guilds=True - Fetches all guilds the user is in. Used with Session.fetch_guilds()

connections=True - Fetches all third party connections for the user. Used with Session.fetch_connections()

email=True - Additionally provides an e-mail with Session.fetch_user()

guilds_join=True - Allows the user to be added to a guild that the bot is in. Used with Session.join_guild(bot_token, guild_id)

guilds_members_read=True - Gets guild member information (roles, nick, etc) in a guild. Used with Guild.fetch_member()

applications_commands=True - Allows the bot to add slash commands to a server. Has no library methods.

Scopes Example 
*********************

This Example was taken from examples/quart.py

.. code-block:: python 
    
    import quart
    import discordoauth 

    app = quart.Quart(__name__)
    
    # Initialise client and choose scopes.
    client = discordoauth.Client(app_id, "app_secret_here")
    scopes = discordoauth.Scopes(identify=True)

    # The address that flask is currently running on
    address = "localhost:5000"

    @app.route("/login", ["GET"])
    def _login():

        # Generate an oauth URL and redirect the user to it
        return quart.redirect(
            client.get_oauth_url(scopes, rediret_uri= address+"/return")
        )

Sessions
~~~~~~~~~

Sessions are used to retrieve data from a response code.

When a redirect URI is provided to an Oauth URL, Discord redirects the user to that URI with a code as a URL parameter.

The code can be passed into a `discordoauth.Session()` to retrieve data from scopes 

Session Example 
*********************

This Example was taken from examples/quart.py

.. code-block:: python 
    
    import quart
    import discordoauth 

    client = discordoauth.Client(app_id, app_secret)
    scopes = discordoauth.Scopes(identify=True)

    @app.route("/return", ["GET"])
    async def _discord_return():

        # Get the code discord responds with from URI arguments
        code = quart.request.args.get("code")

        # Start a session
        session = client.new_session(code, scopes, address+"/return")

        # Use scope identify to fetch user information. Automatically converts code to access token
        user = await session.fetch_user()

        return f"""
    Username: {user.name} <br>
    User ID: {user.id}
        """

Session Methods
~~~~~~~~~~~~~~~~

await Session.fetch_user()
******************************************

Requires the `identify` scope.

Identify the Oauth user and get user information.

.. code-block:: python 

    import quart
    import discordoauth 

    client = discordoauth.Client(app_id, app_secret)
    scopes = discordoauth.Scopes(identify=True)

    @app.route("/return", ["GET"])
    async def _discord_return():

        code = quart.request.args.get("code")
        session = client.new_session(code, scopes, address+"/return")

        user = await session.fetch_user()

        print(user.name)
        print(user.id)
        print(user.avatar_url)

await Session.fetch_guilds()
******************************************

Requires the `guilds` scope.

Fetch the guilds the Oauth user is in.

.. code-block:: python 

    import quart
    import discordoauth 

    client = discordoauth.Client(app_id, app_secret)
    scopes = discordoauth.Scopes(guilds=True)

    @app.route("/return", ["GET"])
    async def _discord_return():

        code = quart.request.args.get("code")
        session = client.new_session(code, scopes, address+"/return")

        guilds = await session.fetch_guilds()

        for guild in guilds:
            print(guild.name)
            print(guild.id)
            print(guild.avatar_url)

await Session.fetch_connections()
******************************************

Requires the `connections` scope.

Fetch all third party connections on the User's profile.

.. code-block:: python 

    import quart
    import discordoauth 

    client = discordoauth.Client(app_id, app_secret)
    scopes = discordoauth.Scopes(connections=True)

    @app.route("/return", ["GET"])
    async def _discord_return():

        code = quart.request.args.get("code")
        session = client.new_session(code, scopes, address+"/return")

        connections = await session.fetch_connections()

        for connection in connections:
            print(connection.name)
            print(connection.is_visible)
            print(connection.is_verified)


|subst|
******************************************

.. |subst| replace:: await Session.join_guild(
    bot_token : str,
    guild_id : int,
    nick : str = None,
    roles : List[int, Object] = [],
    mute : bool = False,
    deaf : bool = False,
    user_id : int = None
    )

Requires the `guilds_join` scope and the `identify` scope if user_id is not passed.

Joins a guild as the user.

.. code-block:: python 

    import quart
    import discordoauth 

    client = discordoauth.Client(app_id, app_secret)
    scopes = discordoauth.Scopes(guilds_join=True)

    bot_token = "bot_token_here"

    @app.route("/return", ["GET"])
    async def _discord_return():

        code = quart.request.args.get("code")
        session = client.new_session(code, scopes, address+"/return")

        member = await session.join_guild(bot_token, guild_id, user_id=user_id)
        print(member.nick)

Versions
-------------------

v0.1.3
~~~~~~~~~

* Remove prints

v0.1.2
~~~~~~~~~

* Added casting functions to objects 
* Fixed scopes docstring
* Renamed scopes in __init__

v0.1.1
~~~~~~~~~

* Added applicationds_commands scope so that bot invites can be used

v0.1.0
~~~~~~~~~

* Initial version