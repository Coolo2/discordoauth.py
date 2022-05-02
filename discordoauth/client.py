
from __future__ import annotations
import typing 

if typing.TYPE_CHECKING:
    from discordoauth.scopes import Scopes

from discordoauth import session as s
from discordoauth import http

import asyncio
import nest_asyncio

class Object():
    def __init__(self, id : int):
        self.id = id 
    
    def __int__(self):
        return self.id

class Client():
    def __init__(self, app_id : int, app_secret : str):
        self.app_id = app_id 
        self.app_secret = app_secret

        self.loop = asyncio.new_event_loop()
        nest_asyncio.apply(self.loop)

        self.http = http.HTTP(self)
    
    def new_session(self, code : str, scopes : Scopes, rediret_uri=None) -> s.Session:

        session = s.Session(self, code, scopes, rediret_uri)

        return session
    
    def get_oauth_url(self, scopes : Scopes, rediret_uri=None):

        url = f"{self.http.base}/oauth2/authorize?client_id={self.app_id}"

        if rediret_uri:
            url += f"&rediret_uri={rediret_uri}"
        
        url += f"&scope={str(scopes)}"

        if scopes.identify:
            url += "&response_type=code"

        return url