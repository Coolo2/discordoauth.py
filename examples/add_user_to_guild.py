
"""
Basic Quart example for using Discord Oauth2
"""

import quart
import discordoauth 

app = quart.Quart(__name__)

# Everything here is described in the quart example.
app_id = 999999999999999999
app_secret = "app_secret_here"
client = discordoauth.Client(app_id, app_secret)
scopes = discordoauth.Scopes(identify=True, guilds_join=True)
address = "localhost:5000"

@app.route("/join", ["GET"])
def _join():
    return quart.redirect(
        client.get_oauth_url(scopes, rediret_uri= address+"/return")
    )

# The bot token to add the user with. Must be of the same application as the app_id and app_secret
token = "bot_token_here"

@app.route("/return", ["GET"])
async def _discord_return():

    guild_id_to_join = 999999999999999999

    # Get the code discord responds with from URI arguments
    code = quart.request.args.get("code")

    # Start a session
    session = client.new_session(code, scopes, address+"/return")

    # Use scope identify to fetch user information. Automatically converts code to access token
    member = await session.join_guild(
        token, 
        guild_id_to_join,
        roles=[999999999999999999], # Optional - Roles to add to the user
        nick= "Automatically added user", # Optional - Nickname for the user once added
        mute=True, # Optional - Mute the user once added
        deaf=True # Optional - Deafen the user once added
    )

    return f"""
Added to guild!

Nickname: {member.nick} <br>
    """

# Run the app locally on port 5000
app.run("0.0.0.0", 5000)
