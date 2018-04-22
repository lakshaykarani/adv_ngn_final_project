import json
from flask import Flask, render_template, request, Markup
import networkx as nx
from networkx.readwrite import json_graph
import http.client
from json2html import *

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

        conn = http.client.HTTPConnection(self.server, 8080)
        print(body)
        conn.request(action, path, body, headers)

        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print(ret)
        conn.close()
        return ret

retriever = FlowRetriever('192.168.56.104')
app = Flask(__name__, static_url_path='')

G = nx.Graph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/network_topo')
def network_topo():
    raw_json_nodes = retriever.get("/v1.0/topology/switches", "")
    raw_json_links = retriever.get("/v1.0/topology/links", "")
    raw_json_hosts = retriever.get("/v1.0/topology/hosts", "")



    node_count = 0
    node_id = {}
    for switch in raw_json_nodes:
        #node_id.append(switch['dpid'])
        G.add_node(node_count, name = switch['dpid'])
        node_id[switch['dpid']] = node_count
        node_count+=1


    #network_links = []
    for link in raw_json_links:
        #network_links.append(link['src']['dpid'],link['dst']['dpid'])
        G.add_edge(node_id[link['src']['dpid']],node_id[link['dst']['dpid']])

    for host in raw_json_hosts:
        # node_id.append(host['ipv4'])
        G.add_node(node_count, name=host['ipv4'][0])

        node_id[host['ipv4'][0]]=node_count
        node_count += 1
        #network_links.append(host['port']['dpid'], host['ipv4'])
        G.add_edge(node_id[host['port']['dpid']], node_id[host['ipv4'][0]])


    '''G = nx.barbell_graph(6, 3)
    for n in G:
    G.nodes[n]['name'] = n'''

    d = json_graph.node_link_data(G)
    print(d)
    json.dump(d, open('static/force.json', 'w'))
    print('Wrote node-link JSON data to force/force.json')

    return render_template('network_topo.html')

@app.route('/net_stats')
def net_stats():
    html_data = {}
    json_switch_details = retriever.get("/v1.0/topology/switches", "")
    sort_switch_details=json.dumps(json_switch_details, sort_keys=True)
    switch_details_html = json2html.convert(json=sort_switch_details, table_attributes="class=\"table table-bordered table-striped\"")

    json_host_details = retriever.get("/v1.0/topology/hosts", "")
    sort_host_details=json.dumps(json_host_details, sort_keys=True)
    host_details_html = json2html.convert(json=sort_host_details, table_attributes="class=\"table table-bordered table-striped\"")

    switch_count = retriever.get("/stats/switches", "")

    all_switch_desc = []
    all_switch_flows = []
    all_port_stats = []

    for dpid in switch_count:
        print(dpid)
        switch_desc = retriever.get("/stats/desc/{}".format(dpid), "")
        all_switch_desc.append(switch_desc)

        switch_flows = retriever.get("/stats/flow/{}".format(dpid), "")
        all_switch_flows.append(switch_flows)

        port_stats= retriever.get("/stats/port/{}".format(dpid), "")
        all_port_stats.append(port_stats)


    sort_switch_desc=json.dumps(all_switch_desc, sort_keys=True)
    switch_desc_html = json2html.convert(json=sort_switch_desc, table_attributes="class=\"table table-bordered table-striped\"")

    sort_switch_flows=json.dumps(all_switch_flows, sort_keys=True)
    switch_flows_html = json2html.convert(json=sort_switch_flows, table_attributes="class=\"table table-bordered table-striped\"")

    sort_port_stats=json.dumps(all_port_stats, sort_keys=True)
    port_stats_html = json2html.convert(json=sort_port_stats, table_attributes="class=\"table table-bordered table-striped\"")



    return render_template('network_stats.html', switch_details_html= Markup(switch_details_html),
                           host_details_html= Markup(host_details_html),
                           switch_desc_html= Markup(switch_desc_html),
                           switch_flows_html= Markup(switch_flows_html),
                           port_stats_html= Markup(port_stats_html))

@app.route('/network_optimize')
def network_optimize():
    return render_template('network_optimize.html')

@app.route('/optimize', methods = ['GET', 'POST'])
def optimize():

    if request.method == 'POST':
        source_IP = request.form['source']
        target_IP = request.form['target']
        print(source_IP, target_IP)

        topology = json_graph.node_link_data(G)
        for node in topology['nodes']:
            print(node)
            if source_IP in node['name']:
                source_id = node['id']
            if target_IP in node['name']:
                target_id = node['id']

        for link in topology['links']:
            print("links",link)
            if source_id == link['source']:
                source_switch_id = link['target']
            if source_id == link['target']:
                source_switch_id = link['source']
            if target_id == link['source']:
                target_switch_id = link['target']
            if target_id == link['target']:
                target_switch_id = link['source']


        shortest_path_nodes = nx.shortest_path(G,source_switch_id,target_switch_id)
        print(shortest_path_nodes)
        shortest_path_dpids = []
        node_dpid_dict = {}
        for node in topology['nodes']:
            if node['id'] in shortest_path_nodes:
                shortest_path_dpids.append(node['name'])
                node_dpid_dict[node['id']] = node['name']


        print(node_dpid_dict)

        raw_json_links = retriever.get("/v1.0/topology/links", "")
        print("BELOW")
        print(len(shortest_path_nodes))

        for count in range(0, len(shortest_path_nodes)-1):
            print(count)
            for link in raw_json_links:
                if node_dpid_dict[shortest_path_nodes[count]] == link['src']['dpid'] and node_dpid_dict[shortest_path_nodes[count+1]] == link['dst']['dpid']:
                    jsonDict = {}
                    jsonDict['match'] = {}
                    print("UP", link['src']['dpid'], link['dst']['dpid'])
                    out_port = link['src']['port_no']
                    print("out_port", out_port)

                    #Add flow for dst IP to out port
                    jsonDict['dpid'] = int(link['src']['dpid'])
                    jsonDict['priority'] = 20000
                    jsonDict['match']['ipv4_dst'] = target_IP
                    jsonDict['match']['eth_type'] = '0x800'
                    jsonDict['actions'] = [{"type": "OUTPUT", "port": int(out_port)}]
                    retriever.set('/stats/flowentry/add', jsonDict)


        for count in range(len(shortest_path_nodes)-1, 0, -1):
            print(count)
            for link in raw_json_links:
                if node_dpid_dict[shortest_path_nodes[count]] == link['src']['dpid'] and node_dpid_dict[shortest_path_nodes[count-1]] == link['dst']['dpid']:
                    print("DOWN", link['src']['dpid'], link['dst']['dpid'])
                    out_port = link['src']['port_no']

                    print("out_port", out_port)
                    #Add flow for src IP to out port
                    jsonDict = {}
                    jsonDict['match'] = {}
                    jsonDict['dpid'] = int(link['src']['dpid'])
                    jsonDict['priority'] = 20000
                    jsonDict['match']['ipv4_dst'] = source_IP
                    jsonDict['match']['eth_type'] = '0x800'
                    jsonDict['actions'] = [{"type": "OUTPUT", "port": int(out_port)}]
                    retriever.set('/stats/flowentry/add', jsonDict)

        raw_json_hosts = retriever.get("/v1.0/topology/hosts", "")

        print("Host Conn")
        for host in raw_json_hosts:
            if host['ipv4'][0] in [source_IP, target_IP]:
                switch_host_dpid = host['port']['dpid']
                switch_host_port_no = host['port']['port_no']
                print(switch_host_dpid,switch_host_port_no)
                #Add flows for hosts at out port
                jsonDict = {}
                jsonDict['match'] = {}
                jsonDict['dpid'] =int(switch_host_dpid)
                jsonDict['priority'] = 20000
                jsonDict['match']['ipv4_dst'] = host['ipv4'][0]
                jsonDict['match']['eth_type'] = '0x800'
                jsonDict['actions'] = [{"type": "OUTPUT", "port": int(switch_host_port_no)}]
                retriever.set('/stats/flowentry/add', jsonDict)

        spf_dpid = []
        for dpid in shortest_path_nodes:
            spf_dpid.append(int(dpid) + 1 )
        text ='''<div class="alert alert-success alert-block"> <a class="close" data-dismiss="alert" href="#">
        <h3 class="alert-heading">Success!</h3>
        <h5>Shortest Path for Source: {} and Destination: {} is dpid: {}. Added respect flows! </h5></div>'''.format(source_IP,target_IP,spf_dpid)
        return render_template('network_optimize.html', text=Markup(text))


if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.56.1', port=5000)
