"""
    A series of variables and commands of where to send things
    Also sents who can use certain commands
"""

log_channel_id = None #can be changed using a command

def set_log_channel(channel_id):
    global log_channel_id
    log_channel_id = channel_id

def get_log_channel(): #for debugging bc I feel like I'm going to fuck this up
    return log_channel_id