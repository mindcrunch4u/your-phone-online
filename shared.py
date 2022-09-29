from datetime import datetime

name_searchdir = "/storage/emulated/0/DCIM/Camera"

def timestring_now():
    content_time = datetime.now()
    content_time = content_time.strftime("%m/%d/%Y, %H:%M:%S")
    return content_time

def build_message(original, latest):
    tmpdict = {"timestamp": timestring_now(), "message": latest}
    original.append(tmpdict)
    return original

