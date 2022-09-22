#!/usr/bin/env python3
import serial
import flask
import os.path
import pathlib
import random
import requests

app = flask.Flask(__name__)

@app.route('/')
def root():
    return flask.current_app.send_static_file("./index.html")

@app.route('/getcode')
def get_code():
    if (flask.request.args.get("mdp") == mdp):
        ser.write(b"getcode\n");
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        return flask.jsonify({"code": line[:4]})
    return flask.Response(None, 401)

@app.route('/setcode')
def set_code():
    if flask.request.args.get("mdp") == mdp:
        code = ""
        for i in range(4):
            code += str(random.randint(1, 10))
        code += '\n'
        ser.write(b"setcode\n");
        print(len(code))
        print(code)
        ser.write(bytes(code, "UTF-8"))
        return flask.Response(None, 200)
    return flask.Response(None, 401)

if __name__ == '__main__':
    global ser
    i = 0
    while not pathlib.Path(f"/dev/ttyACM{i}").exists():
        print(f"file /dev/ttyACM{i} do not exists")
        i += 1
    print(f"found /dev/ttyACM{i}")
    ser = serial.Serial(f"/dev/ttyACM{i}", 9600, timeout=1)
    ser.reset_input_buffer()

    global mdp
    f = pathlib.Path("./PASS")
    if not f.exists():
        print("le fichier PASS n'existe pas, veuillez le créer et entrer le mod de passe dedans")
        exit(1)
    with f.open() as ff:
        mdp = ff.readline()[:-1]
    print(f"password is {mdp}")

    requests.get(url = "https://127.0.0.1:5000/setcode", params = {"mdp":mdp})

    app.run(host="0.0.0.0")
