import json
from flask import Flask, render_template, request, Markup
import httplib
import paramiko
from json2html import *
from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker

class FlowRetriever(object):
    def __init__(self, server):
        self.server = server

    def get(self, path, function):
        ret = self.rest_call(path, function, 'GET')
        return json.loads(ret[2])

    def set(self, path, data):
        ret = self.rest_call(path, data, 'POST')
        return ret[0] == 200

    def rest_call(self, path, data, action):


        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }

        if action == 'POST':
            body = json.dumps(data)
        else:
            body = ''

        conn = httplib.HTTPConnection(self.server, 8080)
        print(body)
        conn.request(action, path, body, headers)

        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print(ret)
        conn.close()
        return ret

retriever = FlowRetriever('192.168.56.104')
app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bgp_config')
def bgp_config():

    return render_template('bgp_config.html')

@app.route('/bgp_view')
def bgp_view():

    

    hostname = "10.0.1.1"
    port = 22

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(hostname, username = 'ubuntu', password = 'lab123', port=port)


        stdin, stdout_route, stderr = client.exec_command("sudo vtysh -c \"show ip bgp\"")
	print(stdout_route)
        stdin, stdout_neighbor, stderr = client.exec_command("sudo vtysh -c \"show ip bgp summary\"")
	print(stdout_neighbor)

    finally:
        client.close()

	
    return render_template('bgp_view.html')

@app.route('/optimize', methods = ['GET', 'POST'])
def optimize():

        return render_template('network_optimize.html', text=Markup(text))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
