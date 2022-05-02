
from __future__ import annotations
import typing 

if typing.TYPE_CHECKING:
    from discordoauth.client import Client, Object as ObjectType
    from discordoauth.scopes import Scopes
    from discordoauth.session import Session as SessionType, Member as MemberType

from discordoauth import scopes, errors
from discordoauth import utils

class Access():
    def __init__(self, data : dict):
        self.access_token : str = data["access_token"]
        self.expires_in : int = data["expires_in"]
        self.refresh_token : str= data["refresh_token"]

        self.scopes = scopes.Scopes().from_string(data["scope"])

class User():

    def __init__(self, data : dict):

        self.raw = data

        self.id = int(data["id"])
        self.name : str = data["username"]
        self.avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{data['avatar']}.webp?size=1024"
        self.discriminator = int(data["discriminator"])
        self.banner : str = data["banner"] if "banner" in data else None
        self.banner_color : str = data["banner_color"] if "banner_color" in data else None
        self.locale : str = data["locale"] if "locale" in data else None
        self.mfa_enabled : bool = data["mfa_enabled"] if "mfa_enabled" in data else None

        if "email" in data:
            self.verified : bool = data["verified"]
            self.email : str = data["email"]
    
    def __str__(self):
        return f"{self.name}#{self.discriminator}"
    
    def __dict__(self):
        return self.raw

class Guild():
    def __init__(self, session : SessionType, data : dict):

        self.raw = data
        self.session = session
        
        self.id = int(data["id"])
        self.name : str = data["name"]
        self.icon : str = f"https://cdn.discordapp.com/icons/{self.id}/{data['icon']}.webp?size=1024"
        self.is_owner : bool = data["owner"]
        self.features : typing.List[str] = data["features"]

        self.member : MemberType = None
    
    async def fetch_member_information(self):
        
        if not self.session.scopes.guilds_members_read:
            raise errors.MissingScope("This method requires the guilds_members_read scope")

        if not self.session.access:
            await self.session.get_access_token()
        
        headers = {"Content-Type":"application/json", 'Authorization': "Bearer {}".format(self.session.access.access_token)}

        data = await self.session.client.http.request_rate(self.session, "GET", f"/users/@me/guilds/{self.id}/member", headers=headers)

        self.member = Member(data) 

        return self.member
    
    def __str__(self):
        return self.name 
    
    def __dict__(self):
        return self.raw

class Connection():
    def __init__(self, data : dict):

        self.raw = data
        
        self.type : str = data["type"]
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.is_visible = bool(data["visibility"])
        self.friend_sync : bool = data["friend_sync"]
        self.show_activity : bool = data["show_activity"]
        self.id_verified : bool = data["verified"]
    
    def __str__(self):
        return self.name 
    
    def __dict__(self):
        return self.raw

class Member():
    def __init__(self, data : dict):

        self.raw = data
        
        self.user = User(data["user"])
        self.avatar_url : str = f"https://cdn.discordapp.com/avatars/{self.user.id}/{data['avatar']}.webp?size=1024"

        self.communication_disabled_until : str = data["communication_disabled_until"]
        self.flags : int = data["flags"]
        self.is_pending : bool = data["is_pending"]
        self.joined_at : str = data["joined_at"]
        self.nick : str = data["nick"]
        self.premium_since : str = data["premium_since"]
        self.roles : typing.List[dict] = data["roles"]
        self.is_mute : bool = data["mute"]
        self.is_deaf : bool = data["deaf"]
    
    def __str__(self):
        return f"{self.user.name}#{self.user.discriminator}"
    
    def __dict__(self):
        return self.raw

class Session():

    def __init__(self, client : Client, code : str, scopes : Scopes, rediret_uri : str = None):

        self.client = client 

        self.code = code 
        self.scopes = scopes 
        self.redirect_uri = rediret_uri

        self.access : Access = None

        self.user : User = None 
        self.guilds : typing.List[Guild] = []
        self.connections : typing.List[Connection] = []
        self.member : Member = None
    
    def get_access_token_sync(self) -> Access:
        return self.client.loop.run_until_complete(self.get_access_token())
    
    def refresh_access_token_sync(self, refresh_token : str = None) -> Access:
        return self.client.loop.run_until_complete(self.refresh_access_token(refresh_token))
    
    def fetch_user_sync(self) -> User:
        return self.client.loop.run_until_complete(self.fetch_user())
    
    def fetch_guilds_sync(self) -> typing.List[Guild]:
        return self.client.loop.run_until_complete(self.fetch_guilds())
    
    def fetch_connections_sync(self) -> typing.List[Connection]:
        return self.client.loop.run_until_complete(self.fetch_connections())
    
    def join_guild_sync(
            self, 
            bot_token : str, 
            guild_id : int, 
            nick : str = None, 
            roles : typing.List[typing.Union[ObjectType, int]] = None, 
            mute : bool = False,
            deaf : bool = False,
            user_id : int = None
    ) -> typing.Union[Member, None]:
        return self.client.loop.run_until_complete(self.join_guild(bot_token, guild_id, nick, roles, mute, deaf, user_id))
    
    
    async def get_access_token(self) -> Access:

        """
            Retrives an oauth access token from discord

            This must be called before retreiving any data.
        """

        payload = {
            'client_id': self.client.app_id,
            'client_secret': self.client.app_secret,
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': self.redirect_uri,
            'scope': str(self.scopes)
        }

        data = await self.client.http.request_rate(self, "POST", "/oauth2/token", payload, {'Content-Type': 'application/x-www-form-urlencoded'})
        self.access = Access(data)

        return self.access
    
    async def refresh_access_token(self, refresh_token : str = None) -> Access:

        """
            Retrives an oauth access token from discord

            This must be called before retreiving any data.
        """

        refresh_token = refresh_token or self.access.refresh_token

        payload = {
            'client_id': self.client.app_id,
            'client_secret': self.client.app_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        data = await self.client.http.request_rate(self, "POST", "/oauth2/token", payload, {'Content-Type': 'application/x-www-form-urlencoded'})
        self.access = Access(data)

        return self.access
    
    async def fetch_user(self) -> User:

        if not self.scopes.identify:
            raise errors.MissingScope("This method requires the identify scope")

        if not self.access:
            await self.get_access_token()
        
        headers = {
            'Authorization': "Bearer {}".format(self.access.access_token)
        }

        data = await self.client.http.request_rate(self, "GET", "/users/@me", headers=headers)
        self.user = User(data)

        return self.user
    
    async def fetch_guilds(self) -> typing.List[Guild]:

        if not self.scopes.guilds:
            raise errors.MissingScope("This method requires the guilds scope")

        if not self.access:
            await self.get_access_token()
        
        headers = {
            'Authorization': "Bearer {}".format(self.access.access_token)
        }

        data = await self.client.http.request_rate(self, "GET", "/users/@me/guilds", headers=headers)
        self.guilds : typing.List[Guild] = []

        for raw_guild in data:     
            self.guilds.append(Guild(self, raw_guild))   
        
        return self.guilds
    
    async def fetch_connections(self) -> typing.List[Connection]:

        if not self.scopes.connections:
            raise errors.MissingScope("This method requires the connections scope")

        if not self.access:
            await self.get_access_token()
        
        headers = {
            'Authorization': "Bearer {}".format(self.access.access_token)
        }

        data = await self.client.http.request_rate(self, "GET", "/users/@me/connections", headers=headers)
        self.connections : typing.List[Connection] = []

        for raw_connection in data:     
            self.connections.append(Connection(raw_connection))   
        
        return self.connections
    
    async def join_guild(
            self, 
            bot_token : str, 
            guild_id : int, 
            nick : str = None, 
            roles : typing.List[typing.Union[ObjectType, int]] = None, 
            mute : bool = False,
            deaf : bool = False,
            user_id : int = None
    ) -> typing.Union[Member, None]:

        if not self.scopes.guilds_join:
            raise errors.MissingScope("This method requires the guilds_join scope")
        
        if not user_id and not self.user:
            raise errors.MissingArgument("Argument user_id is missing and no previous user data was found.")

        if hasattr(roles, '__iter__'):
            for i, role in enumerate(roles):
                if hasattr(role, "id"):
                    roles[i] = str(role.id)
                else:
                    roles[i] = str(role)
        
        user_id = user_id or self.user.id

        if not self.access:
            await self.get_access_token()
        
        headers = {
            'Authorization': "Bot {}".format(bot_token),
            "Content-Type":"application/json"
        }

        data = {
            "access_token":self.access.access_token,
            "nick":nick,
            "deaf":deaf,
            "mute":mute,
            "roles":roles
        }



        data = await self.client.http.request_rate(self, "PUT", f"/guilds/{guild_id}/members/{user_id}", json=data, headers=headers)

        if data:
            self.member = Member(data) 

            return self.member
    
    def get_guild(self, guild_id : int) -> typing.Union[Guild, None]:

        return utils.item_by_value(self.guilds, "id", guild_id)
    

    