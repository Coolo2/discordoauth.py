
"""
Basic Quart example for using Discord Oauth2
"""

import quart
import discordoauth 

app = quart.Quart(__name__)

# The application ID and secret to use for Oauth.
app_id = 999999999999999999
app_secret = "app_secret_here"

# Initialise client and choose scopes.
# Supported scopes can be seen in the README.md
client = discordoauth.Client(app_id, app_secret)
scopes = discordoauth.Scopes(identify=True)

# The address that flask is currently running on
address = "localhost:5000"

@app.route("/login", ["GET"])
def _login():

    # Generate an oauth URL and redirect the user to it
    return quart.redirect(
        client.get_oauth_url(scopes, rediret_uri= address+"/return")
    )

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

# Run the app locally on port 5000
app.run("0.0.0.0", 5000)
