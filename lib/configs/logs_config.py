"""
    A series of variables and commands of where to send things
    Also sents who can use certain commands
"""

log_channel_id = None #can be changed using a command

mod_role_title = "Mod" #defaults to what my server is set as creating command to change

def set_log_channel(channel_id):
    global log_channel_id
    log_channel_id = channel_id

def get_log_channel(): #for debugging bc I feel like I'm going to fuck this up
    return log_channel_id

#mod role commands
def set_mod_role(role_name):
    global mod_role_title
    mod_role_title = role_name

def get_mod_role_title():
    return mod_role_title