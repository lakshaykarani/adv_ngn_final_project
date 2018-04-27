import json, time
from flask import Flask, render_template, request, Markup
import httplib
import paramiko
from json2html import *
from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker

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
        client.connect(hostname, username = 'root', password = 'lab123', port=port)
	

        stdin, stdout_route, stderr = client.exec_command("sudo vtysh -c 'show ip bgp'")
        stdin, stdout_neighbor, stderr = client.exec_command('sudo vtysh -c "show ip bgp summary"')

        quagga_bgp_routes = stdout_route.read()
        quagga_bgp_neighbors = stdout_neighbor.read()
        print(quagga_bgp_routes)
        print(quagga_bgp_neighbors)

        quagga_bgp_routes = '''
<table class="tg">
  <tr>
    <th class="tg-us36">Network</th>
    <th class="tg-us36">Next Hop</th>
    <th class="tg-us36">Metric</th>
    <th class="tg-us36">LocPrf</th>
    <th class="tg-us36">Weight</th>
    <th class="tg-us36">Path</th>
  </tr>
  <tr>
    <td class="tg-us36">*&gt; 10.0.0.0</td>
    <td class="tg-us36">0.0.0.0</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36"></td>
    <td class="tg-us36">32768</td>
    <td class="tg-us36">i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt; 11.0.0.0</td>
    <td class="tg-us36">0.0.0.0</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36"></td>
    <td class="tg-us36">32768</td>
    <td class="tg-us36">i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt; 20.0.0.0/24</td>
    <td class="tg-us36">11.0.1.1</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36"></td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">300 i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt; 30.0.0.0/24</td>
    <td class="tg-us36">11.0.1.1</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36"></td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">300 i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt; 40.0.0.0/24</td>
    <td class="tg-us36">11.0.1.1</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36"></td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">300 i</td>
  </tr>
</table>'''


        quagga_bgp_neighbors = '''<table class="tg">
  <tr>
    <th class="tg-us36">Neighbor</th>
    <th class="tg-us36">V</th>
    <th class="tg-us36">AS</th>
    <th class="tg-us36">MsgRcvd</th>
    <th class="tg-us36">MsgSent</th>
    <th class="tg-us36">State/PfxRcd</th>
  </tr>
  <tr>
    <td class="tg-us36">10.0.1.2</td>
    <td class="tg-us36">4</td>
    <td class="tg-us36">200</td>
    <td class="tg-us36">4554</td>
    <td class="tg-us36">4626</td>
    <td class="tg-us36">0</td>
  </tr>
  <tr>
    <td class="tg-us36">11.0.1.1</td>
    <td class="tg-us36">4</td>
    <td class="tg-us36">300</td>
    <td class="tg-us36">14392</td>
    <td class="tg-us36">14405</td>
    <td class="tg-us36">3</td>
  </tr>
</table>'''

    finally:
        client.close()

	
    return render_template('bgp_view.html',quagga_bgp_routes=Markup(quagga_bgp_routes), quagga_bgp_neighbors = Markup(quagga_bgp_neighbors))

@app.route('/optimize', methods = ['GET', 'POST'])
def optimize():

        return render_template('network_optimize.html', text=Markup(text))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
