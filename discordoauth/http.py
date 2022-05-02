from __future__ import annotations
import typing 

if typing.TYPE_CHECKING:
    from discordoauth.client import Client
    from discordoauth.session import Session

import aiohttp 
import json as j

import asyncio
from discordoauth import errors

INFINITY = 9999999999

class HTTP():

    def __init__(self, client : Client):

        self.client = client 
        
        self.base = "https://discord.com/api"

        self.session : aiohttp.ClientSession = None
    
    async def get_aiohttp_session(self) -> aiohttp.ClientSession:

        if not self.session:
            self.session = aiohttp.ClientSession()

        return self.session 
    
    async def request_rate(self, oauth_session : Session, request : str, path : str, data : dict = None, headers : dict =None, json : dict = None):

        session = await self.get_aiohttp_session()
        retry_after = INFINITY
        tried_refresh = False

        # Rate limit handling.
        while retry_after > 0:
            async with session.request(request, self.base + path, data=data, headers=headers, json=json) as r:
                print(await r.text())
                print(r.status)

                if r.status == 400 and not tried_refresh:
                    await oauth_session.refresh_access_token()
                    tried_refresh = True
                if r.status == 429:
                    retry_after = ((await r.json())["retry_after"] / 1000) + 0.5
                    await asyncio.sleep(retry_after + 1)
                
                retry_after = 0  

                if r.status == 204:
                    return None
                
                data = j.loads(await r.text())

                if r.status == 403:
                    raise errors.HTTPError(data["message"])

                return data


        


