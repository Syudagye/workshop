#!/usr/bin/env python3
import serial
import time
import flask
import threading
import os.path
import time
import pathlib

class FlaskWrapper(threading.Thread):
    def __init__(self, target):
        self.mt_name = "flask"
        self.mt_target = target
        threading.Thread.__init__(self, name = "flask", target = target)
    def start(self):
        super().start()
        threading.Thread.__init__(self, name = self.mt_name, target = self.mt_target)
    def run(self):
        super().run()
        threading.Thread.__init__(self, name = self.mt_name, target = self.mt_target)

message_queue = []
app = flask.Flask(__name__)
def run_flask():
    app.run()

appWrap = FlaskWrapper(run_flask)


@app.route('/')
def root():
    return flask.current_app.send_static_file("./index.html")

@app.route('/getcode')
def get_code():
    if (flask.request.args.get("mdp") == mdp):
        # message_queue.append(b"getcode")
        ser.write(b"getcode\n");
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        return flask.jsonify({"code": line[:4]})
    return flask.Response(None, 401)

@app.route('/setcode')
def set_code():
    if flask.request.args.get("mdp") == mdp:
        code = flask.request.args.get("code")
        if code is not None and len(code) == 4:
            # message_queue.append(b"getcode")
            code += '\n'
            ser.write(b"setcode\n");
            print(len(code))
            print(code)
            ser.write(bytes(code, "UTF-8"))
            return flask.Response(None, 200)
        return flask.Response(None, 400)
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

    appWrap.start()
    while True:
        pass
        # for i in range(len(message_queue)):
        #     msg = message_queue.pop()
        #     ser.write(msg + b"\n")
        #     line = ser.readline().decode('utf-8').rstrip()
        #     print(line)
        # line = ser.readline().decode('utf-8').rstrip()
        # print(line)
        # time.sleep(1)
