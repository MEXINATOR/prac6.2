from flask import Flask, send_file, render_template
import server
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/SensorStream') #display 10 or less of the most recent messages recieved
def sensor_stream():
    size = 10
    if(len(server.msgs) < 10):
        size = len(server.msgs)
    data = server.msgs[-size:]
    return render_template("stream.html", data=data)
    #TODO: Add code that displays the contents of log file /data/sensorlog.txt

@app.route('/DOWNLOAD')
def download_file():
    path = "/data/sensorlog.csv"
    return send_file(path, as_attachment=True)
    #TODO: Add code to download the file /data/sensorlog.txt

@app.route('/SEND_ON') #enable sending
def send_on():
    server.sendOn()
    return "requesting data from PI1"

@app.route('/SEND_OFF')#disable sending
def send_off():
    server.sendOff()
    return "stopped requesting data from PI1"

@app.route('/CHECK')#get the status
def check():
    status = server.check()
    return status
    #TODO: Add code to download the file /data/sensorlog.txt

@app.route('/EXIT')#terminate connection with PI1
def exit():
    server.exit()
    return "SHUT DOWN PI1"
    #TODO: Add code to download the file /data/sensorlog.txt

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  #    app.run(host='0.0.0.0', port=5080)
    
    