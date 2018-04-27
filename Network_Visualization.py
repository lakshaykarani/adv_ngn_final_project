import json, time
from flask import Flask, render_template, request, Markup
import httplib
import paramiko
from json2html import *
from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker
from conf import *
app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bgp_config')
def bgp_config():

    return render_template('bgp_config.html')

@app.route('/configure')
def bgp_config():


    status = "BGP Configured"
    return render_template('bgp_config.html', status=status)

@app.route('/bgp_view')
def bgp_view():

    

    hostname = "10.0.1.1"
    port = 22

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(hostname, username = 'root', password = 'lab123', port=port)
	

        stdin, stdout_route, stderr = client.exec_command("sudo vtysh -c 'show ip bgp'")
        stdin, stdout_neighbor, stderr = client.exec_command('sudo vtysh -c "show ip bgp summary"')

        bgp_routes = stdout_route.read()
        bgp_neighbors = stdout_neighbor.read()
        print(bgp_routes)
        print(bgp_neighbors)


    finally:
        client.close()

	
    return render_template('bgp_view.html',quagga_bgp_routes=Markup(quagga_bgp_routes), quagga_bgp_neighbors = Markup(quagga_bgp_neighbors),ryu_bgp_routes=Markup(ryu_bgp_routes), ryu_bgp_neighbors=Markup(ryu_bgp_neighbors))

@app.route('/optimize', methods = ['GET', 'POST'])
def optimize():

        return render_template('network_optimize.html', text=Markup(text))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
