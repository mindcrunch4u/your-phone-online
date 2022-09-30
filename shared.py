from datetime import datetime
import random
import os

name_searchdir = "/storage/emulated/0/DCIM/Camera"
archive_path = "/data/data/com.termux/files/usr/html/boxarch/"

def timestring_now():
    content_time = datetime.now()
    content_time = content_time.strftime("%m %d %Y - %H:%M:%S")
    return content_time

def build_message(original, latest):
    tmpdict = {"timestamp": timestring_now(), "message": latest}
    original.append(tmpdict)
    return original

def archive_message(original):
    try:
        outfile = open(os.path.join(archive_path, timestring_now() + str(random.randint(200, 500)) + ".txt"), "w", encoding="utf-8")
        for line in original:
            outfile.write(line["timestamp"] + os.linesep)
            outfile.write(line["message"] + os.linesep)
            outfile.write('-------------'+ os.linesep)
        print("[i] chat archived")    
    except Exception as e:
        print("[x] unable to archive chat.", e)
    finally:
        outfile.close()
