from flask import Flask, render_template, request, send_from_directory, send_file, jsonify
from threading import Thread, Lock

from security import is_password_valid
from shared import name_searchdir, build_message, timestring_now
from multimedia import serve_latest_image_base64, dir_last_updated, latest_file_by_type

app = Flask(__name__)
message_from_a = list()
message_mutex = Lock()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def home():
    file_power = open("/sys/class/power_supply/battery/capacity", "r")
    content_power  = file_power.readline()
    return render_template("message.html", title=timestring_now(), power=content_power+"%", sendimage=serve_latest_image_base64(), latest=dir_last_updated(name_searchdir))

@app.route('/static/see.webm')
def send_static():
    file_single = latest_file_by_type("video")
    print("[i] serving: " + str(file_single))
    return send_file(file_single)

@app.route('/ding',methods = ['POST', 'GET'])
def ding():
    password = request.form.get("password")
    if is_password_valid(password):
        os.system("mpv ding.mp3")
    else:
        print(password)
    return ('', 204)


# Messaging

@app.route('/message_from_a_get',methods = ['POST', 'GET'])
def message_from_a_get():
    global message_mutex
    message_mutex.acquire()
    try:
        global message_from_a
        return jsonify(message_from_a)
    finally:
        print("[i] mutex released")
        message_mutex.release()

@app.route('/message_from_a_post',methods = ['POST'])
def message_from_a_post():
    global message_from_a
    global message_mutex
    message_mutex.acquire()
    try:
        password = request.form.get("password")
        message = request.form.get("message")
        if is_password_valid(password):
            message_from_a = build_message(message_from_a, message)
        else:
            print(password)
    finally:
        print("[i] mutex released")
        message_mutex.release()
        return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)
