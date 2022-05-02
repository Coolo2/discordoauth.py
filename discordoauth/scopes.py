

VALID_SCOPES = ["bot", "identify", "guilds", "connections", "email", "guilds_join", "guilds_members_read", "applications_commands"]

class Scopes():

    """
        Scopes - A list of Discord Oauth2 scopes
        
        Supported scopes: bot, identify, guilds, connections, email, guilds_join, guilds_members_read, applications_commands

        Example:
        `discordoauth.Scopes(bot=True, identify=True)`
    """    

    def __init__(self, **scopes):

        self.bot = False 
        self.identify = False
        self.guilds = False
        self.connections = False
        self.email = False
        self.guilds_join = False
        self.guilds_members_read = False
        self.applications_commands = False

        self.scopes = []
        
        for key, value in scopes.items():
            if key not in VALID_SCOPES:
                raise TypeError(f'{key!r} is not a valid scope name')
            
            if value:
                self.scopes.append(key.replace("_", "."))
            
            setattr(self, key, value)
    
    def __str__(self):
        return "%20".join(self.scopes)
    
    
    def from_string(self, string : str):
        
        scope_list = string.split("%20")

        for scope in scope_list:
            setattr(self, scope, True)
        self.scopes = scope_list