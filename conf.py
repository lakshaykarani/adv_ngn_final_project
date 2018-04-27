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

ryu_bgp_routes = '''
<table class="tg">
  <tr>
    <th class="tg-us36">Network</th>
    <th class="tg-us36">Labels</th>
    <th class="tg-us36">Next Hop</th>
    <th class="tg-us36">Reason</th>
    <th class="tg-us36">Metric </th>
    <th class="tg-us36">LocPrf</th>
    <th class="tg-us36">Path</th>
  </tr>
  <tr>
    <td class="tg-us36">*&gt;10.0.0.0/8</td>
    <td class="tg-us36">None</td>
    <td class="tg-us36">10.0.1.1</td>
    <td class="tg-us36">Only Path</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">100</td>
    <td class="tg-us36">i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt;11.0.0.0/8</td>
    <td class="tg-us36">None</td>
    <td class="tg-us36">10.0.1.1</td>
    <td class="tg-us36">Only Path</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">100</td>
    <td class="tg-us36">i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt;20.0.0.0/24</td>
    <td class="tg-us36">None</td>
    <td class="tg-us36">11.0.1.1</td>
    <td class="tg-us36">Only Path</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">100</td>
    <td class="tg-us36">300 i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt;30.0.0.0/24</td>
    <td class="tg-us36">None</td>
    <td class="tg-us36">11.0.1.1</td>
    <td class="tg-us36">Only Path</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">100</td>
    <td class="tg-us36">300 i</td>
  </tr>
  <tr>
    <td class="tg-us36">*&gt;40.0.0.0/24</td>
    <td class="tg-us36">None</td>
    <td class="tg-us36">11.0.1.1</td>
    <td class="tg-us36">Only Path</td>
    <td class="tg-us36">0</td>
    <td class="tg-us36">100</td>
    <td class="tg-us36">300 i</td>
  </tr>
</table>'''

ryu_bgp_neighbors = '''
<table class="tg">
  <tr>
    <th class="tg-us36">IP Address</th>
    <th class="tg-us36">AS Number</th>
    <th class="tg-us36">BGP State</th>
  </tr>
  <tr>
    <td class="tg-us36">10.0.1.1</td>
    <td class="tg-us36">200</td>
    <td class="tg-us36">Established</td>
  </tr>
</table>'''
