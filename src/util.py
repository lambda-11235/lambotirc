
def sanitise(msg):
    msg = msg.replace('\x01', '')
    return msg
