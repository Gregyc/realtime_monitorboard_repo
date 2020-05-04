
import os
import socket
import ctypes
import netifaces
from flask import Flask, request
from flask_cors import CORS

#from flask import jsonify
from packet import pack_cp5200data

from packet_huidu import send_huidu_packet
from packet_huidu import send_huidu_simple_text

from network_scanner import scan_ip
from network_scanner import get_host_ip
import scapy.all as scapy



# =============================================================================
# constants
TCP = 0
SERIAL = 1
UDP = 2

PORT_CHUNGBANG = 5200
PORT_HUIDU = 6101


# =============================================================================
# Configurations
control_board = 'HUIDU' # 'CHUNGBANG' or 'HUIDU'


# =============================================================================
# load library from dll files (digital board)
hdsdkdll = ctypes.WinDLL (os.getcwd()+"/HDSDK.dll")


if control_board == 'CHUNGBANG':

    #### CONSTANTS  #####
    PORT = PORT_CHUNGBANG
    BROADCAST_ADDR = '255.255.255.255'
    UDP_RX_ADDR = "127.0.0.1"
    MAX_DATA_LEN = 78
    net_connection_type = UDP

    # the value add to the length of input strings will be the correct len in the
    # field "NW_DataLen"
    NW_DATA_LEN_FIXED_BYTES = 11

elif control_board == 'HUIDU': # 'HUIDU'
    #### CONSTANTS  #####
    PORT = PORT_HUIDU
    MAX_DATA_LEN = 65535
    net_connection_type = TCP

  

else: 
    raise RuntimeError('control board setting error! \
    please choose set the control_board to CHUNGBANG or HUIDU' )




# =============================================================================


# ====Global Lists ===============
sos_id_list = []
sos_msg_list = []

sos_dict = {}


# ===== Global Variables
Test_ClearMsg_En = 0 #0: normal mode, 1: test mode

if Test_ClearMsg_En :
    G_IDX = 0



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

##  the template of @app.route  (HTTP method)
# =============================================================================
# In addition to accepting the URL of a route as a parameter,
# Route decorators can accept a second parameter:
# a list of accepted HTTP Methods.
# By default, a Flask route accepts all methods on a route (GET, POST, etc).
# Providing a list of accepted methods is a good way to build constraints into
# the route for a REST API endpoint which only makes sense in specific contexts.
# =============================================================================
##  @app.route("/api/v1/users/", methods=['GET', 'POST', 'PUT'])



## Route Variable Rules
# =============================================================================
# When defining our route, values within carrot brackets <> indicate a variable; 
# this enables routes to be dynamically generated.
# Variables can be type-checked by adding a colon followed by
# the data type constraint.
# Routes can accept the following variable types:
#     string: Accepts any text without a slash (the default).
#     int: Accepts integers.
#     float: Accepts numerical values containing decimal points.
#     path: Similar to a string, but accepts slashes.
#     
# Unlike static routes, routes created with variable rules do accept parameters,
# with those parameters being the route variables themselves.
# 
# =============================================================================


@app.route('/hello', methods = ['GET'])
def hello():
    return "OK"


#@app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE'])
@app.route('/getsos', methods = ['POST'])
def getsos():
#    print(request.json)

    if Test_ClearMsg_En :
        global G_IDX
        G_IDX  = G_IDX + 1
    
    try:
	
        result = {'macaddr':request.json['MacAddress'],\
                  'owner':request.json['Owner'],\
                  'tag_type':request.json['Category'],\
                  'timestamp':request.json['Timestamp'],\
                  'mapname':request.json['MapName']
                  }

        print('get some result!!!')
        print(result)

        if Test_ClearMsg_En :
            if G_IDX != 1:
                result['timestamp']=0

        # TEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if result['tag_type'] == 1:
            if result['owner'] not in sos_dict:
                if result['timestamp'] != 0:
                    sos_dict[result['owner']] = result['owner'] + result['mapname']

            else:
                if result['timestamp'] == 0:
                    del sos_dict[result['owner']]


            #combine all the messages from the sos_dict
            if len(sos_dict) == 0:
                data = ' '
            else:
                data = ''    

            for idx in sos_dict:
                # currently data limitation in single packet is MAX_DATA_LEN
                # drop any packet if the length is over single packet maximum length
                if len(data) > MAX_DATA_LEN:
                    break
                data = data + sos_dict[idx]








        # # tag_type: 1(長者)
        # if result['tag_type'] == 1:
        #     # check if SOS ID in the sos list
        #     if result['owner'] not in sos_id_list:
        #         # timeestamp equal 0 is cancel , so only not zero value can add to list
        #         if result['timestamp'] != 0:
        #             sos_id_list.append(result['owner'])
        #             sos_msg_list.append(result['owner'] + result['mapname'])
        #     # already in list or need cancel
        #     else:
        #         # timestamp==0: cancel SOS command for specific ID when timestamp ==0
        #         if result['timestamp'] == 0:
        #             rmv_idx = sos_id_list.index(result['owner'])
        #             del sos_id_list[rmv_idx]
        #             # sos_id_list.remove(rmv_idx)
        #             del sos_msg_list[rmv_idx]
        #             # sos_msg_list.remove(rmv_idx)

        #     #combine all the messages from the sos_msg_list
        #     if len(sos_msg_list) == 0:
        #         data = ' '
        #     else:
        #         data = ''    

        #     for idx in sos_msg_list:
        #         # currently data limitation in single packet is MAX_DATA_LEN
        #         # drop any packet if the length is over single packet maximum length
        #         if len(data) > MAX_DATA_LEN:
        #             break
        #         data = data + idx
      

            if control_board == 'HUIDU':
                print('ready to send message to all boards')
                for ip_addr in dgboard_ip_list:
                    # ret = send_huidu_packet(net_connection_type,ip_addr,PORT,data)

                    ret = send_huidu_simple_text(net_connection_type,ip_addr,PORT,data)

                    if ret == 0:
                        print('Send packet to {0} pass'.format(ip_addr))
                        return 'True' 
                    else:
                        print('Send packet to {0} fail, fail reason is {1}'.format(ip_addr,ret))
                        return 'False'                    


    

            elif control_board == 'CHUNGBANG':
                ########################################
                # combine packet.py        
                text_change_interval= 2
                UDP_PORT = PORT    
                
                # AF_INET is IPv4
                # SOCK_DGRAM is only for UDP
                s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                
                
                message = pack_cp5200data(data,text_change_interval)
                
            
                print('ready to send message')
                try:
                    s.sendto(message,(BROADCAST_ADDR,UDP_PORT))
                    s.settimeout(10)
                    
                    while 1:
                        data,addr = s.recvfrom(1024)
                        if data:
                            print('get DATA!!')
                            print('the ip from ',addr)
                            break
                    
                    s.close()
                except socket.timeout:
                    print('timeout')
                    s.close()

                
                return 'True'
            ######################################
            



        else:
            # 非長者 
            return 'False'
    
    
    



    except Exception as e:
        print("exception happen")
        #flash(e)
        return e  


if __name__ == "__main__":

    if control_board == 'HUIDU':
        #### ip-related variables ####
        host_ip = get_host_ip()
        dgboard_ip_list = []
        print('Scanning for all the digital boards')
        # dgboard_ip_list = scan_ip(host_ip)
        dgboard_ip_list = ['192.168.2.200']

        if not dgboard_ip_list :
            raise RuntimeError('Do not detect any board, check connection!!')
        else:    
            # print clients
            print("Available devices in the network:")
            print(dgboard_ip_list) 


    app.run(host="0.0.0.0")

