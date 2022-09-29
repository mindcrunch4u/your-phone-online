import os
import io
import base64
from shared import name_searchdir
from PIL import Image

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
        for root_path, dirs, files in os.walk(folder)
        for f in files))

def latest_file_by_type(file_type):
    file_image = os.listdir(name_searchdir)
    file_image.sort(key=lambda fn: os.path.getmtime(os.path.join(name_searchdir, fn)))
    files = list()
    file_single = None
    if file_type == "image":
        for item in file_image:
            if item.endswith(".jpg"):
                files.append(item)
        file_single = os.path.join(name_searchdir, files[-1])
    elif file_type == "video":
        for item in file_image:
            if item.endswith(".webm") or item.endswith(".mp4"):
                files.append(item)
        file_single = os.path.join(name_searchdir, files[-1])
    return file_single

def compress(b64image):
    if b64image == None:
        return None
    img_base_width = 400
    img_base_height = 250
    b64image = b64image.decode("UTF-8")
    image_data = base64.b64decode(b64image)
    im_file = io.BytesIO(image_data)  # convert image to file-like object
    img = Image.open(im_file)
    if img.size[0] > img.size[1]:
        w_percent = (img_base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((img_base_width, h_size), Image.ANTIALIAS)
    else:
        h_percent = (img_base_height / float(img.size[1]))
        w_size = int((float(img.size[0]) * float(h_percent)))
        img = img.resize((w_size, img_base_height), Image.ANTIALIAS)

    try:
        buf = io.BytesIO()
        img.save(buf, format="PNG", quality=60)
        bytes_im = buf.getvalue()
        return bytes_im
    except Exception as e:
        return None

def serve_latest_image_base64():
    content_image = None
    file_single = latest_file_by_type("image")
    with open(file_single, "rb") as image_file:
        content_image = base64.b64encode(image_file.read())
    try:
        content_image = compress(content_image)
    except:
        print("[i] image compression failedd")
        content_image = None
    if content_image != None:
        content_image = base64.b64encode(content_image)
        content_image = content_image.decode('UTF-8')
    return content_image

