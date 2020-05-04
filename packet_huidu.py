import os
#import sys
import ctypes
import socket
# from math import ceil
hdsdkdll = ctypes.WinDLL (os.getcwd()+"/HDSDK.dll")

#### CONSTANTS  #####
PORT_HUIDU = 6101
TCP = 0


# defines

# create the screen for the digital board, only need initial once
# int HDAPI Hd_CreateScreen(int nWidth, int nHeight, int nColor, int nGray, int nCardType, void *pExParamsBuf, int nBufSize);
# ret: 0: success -1: failure
def create_screen():
    # Set up prototype and parameters for the desired function call.
    Hd_CreateScreen_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,      # Return type.
        ctypes.c_int,    # width
        ctypes.c_int,    # height   
        ctypes.c_int,    # nColor : 0: single color 1: double color 2: rgb
        ctypes.c_int,    # nGray: default set to 1
        ctypes.c_int,    # nCardType: default to 0
        ctypes.c_int,    # dummy1: no use set to 0
        ctypes.c_int)    # dummy2: no use set to 0
    Hd_CreateScreen_Params = (1, "width", 128), (1, "height", 16), (1, "nColor",0), \
                             (1, "nGray",1), (1, "nCardType",0), \
                             (1,"dummy1",0),(1,"dummy2",0)

    # Map the call ("Hd_CreateScreen(...)") to a Python name.

    Hd_CreateScreen = Hd_CreateScreen_Proto (("Hd_CreateScreen", hdsdkdll), Hd_CreateScreen_Params)

    ret = Hd_CreateScreen ()
    return ret


# add a real time area to the screen
#  int HDAPI Hd_Rt_AddRealAreaToScreen(int nX, int nY, int nWidth, int nHeight, int nMaxPageCount);
# ret:  -1: failure
def add_real_area_to_screen():
    # Set up prototype and parameters for the desired function call.
    Hd_Rt_AddRealAreaToScreen_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,      # Return type.
        ctypes.c_int,    # nX: Regional X starting point.
        ctypes.c_int,    # nY: Regional Y starting point.   
        ctypes.c_int,    # nWidth : Area width 
        ctypes.c_int,    # nHeight: Area height
        ctypes.c_int)    # nMaxPageCount: default to 0

    Hd_Rt_AddRealAreaToScreen_Params = (1, "nX", 0), (1, "nY", 0), (1, "width",128), \
                                       (1, "height",16), (1, "MaxPageCount",10)

    Hd_Rt_AddRealAreaToScreen = Hd_Rt_AddRealAreaToScreen_Proto \
                                (("Hd_Rt_AddRealAreaToScreen", hdsdkdll), Hd_Rt_AddRealAreaToScreen_Params)

    ret = Hd_Rt_AddRealAreaToScreen ()
    return ret



# Send screen data to the specified device.
# int HDAPI Hd_SendScreen(int nSendType, void *pStrParams, void *pDeviceGUID, void *pExParamsBuf, int nBufSize);
# ret: 0: success -1: failure
def send_screen_to_device( net_connection_type,ip_addr,portid):
    # Set up prototype and parameters for the desired function call.
    """
    pStrParams: 
    When sending type is 0,
       pStrParams written IP address like L"192.168.2.200".
       The default connection is 6101 port, if used port mapping,
       pStrParams it should add port information, like L"192.168.2.200:6101",6101 is port number.
    When sending type is 1,
        pStrParams written serial information like"4:115200",4 is serial number,
        115200 is serial Baud rate. If not known equipment Baud rate, it can use function of Cmd_GetBaudRate and get equipment Baud rate.
    """
    Hd_Rt_SendScreen_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,     # Return type.
        ctypes.c_int,     # nSendType: 0 TCP 1 serial  2 UDP.
        ctypes.c_wchar_p, # pStrParams: IP information (UTF-16 code)   
        ctypes.c_int,     # dummy1: no use set to 0
        ctypes.c_int,     # dummy2: no use set to 0
        ctypes.c_int)     # dummy3: no use set to 0

    Hd_Rt_SendScreen_Params = (1, "nSendType", 0), (1, "pStrParams", "192.168.2.200:6101"), \
                                       (1, "dummy1",0), (1, "dummy2",0), (1, "dummy3",0)

    Hd_Rt_SendScreen = Hd_Rt_SendScreen_Proto \
                       (("Hd_Rt_SendScreen", hdsdkdll), Hd_Rt_SendScreen_Params)
    nSendType = ctypes.c_int (net_connection_type)
    pStrParams = ctypes.c_wchar_p (ip_addr+":"+str(portid))


    ret = Hd_Rt_SendScreen (nSendType,pStrParams)
    return ret




# Get RGB color value, set this value to text or background.
# default is Red (255,0,0)
# int Hd_GetColor(int r, int g, int b);
# color:  value
def get_color_value():
    # Set up prototype and parameters for the desired function call.
    Hd_GetColor_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,      # Return type.
        ctypes.c_int,    # r: 
        ctypes.c_int,    # g:    
        ctypes.c_int)    # b: 

    Hd_GetColor_Params = (1, "r", 255), (1, "g", 0), (1, "b",0)

    Hd_GetColor = Hd_GetColor_Proto \
                  (("Hd_GetColor", hdsdkdll), Hd_GetColor_Params)

    color = Hd_GetColor ()
    return color



# Send the real time text to the board 
# int Hd_Rt_SendRealTimeText(int nSendType, void *pStrParams, int nRealTimeAreaIndex, int nMaxPageCount,
#     int nColor, int nGray, int nX, int nY, int nWidth, int nHeight,
#     void *pText,int nTextColor, int nBackGroupColor, int nStyle, void *pFontName,
#     int nFontHeight,int nShowEffect, int nShowSpeed,int nStayTime, int nLiveTime,
#     int bSaveToFlash, void *pDeviceGUID);

# ret: 0: success -1: failure
def send_realtime_text( net_connection_type,ip_addr,portid,areaidx,data):
    # Set up prototype and parameters for the desired function call.
    """
    pStrParams: 
    When sending type is 0,
       pStrParams written IP address like L"192.168.2.200".
       The default connection is 6101 port, if used port mapping,
       pStrParams it should add port information, like L"192.168.2.200:6101",6101 is port number.
    When sending type is 1,
        pStrParams written serial information like"4:115200",4 is serial number,
        115200 is serial Baud rate. If not known equipment Baud rate, it can use function of Cmd_GetBaudRate and get equipment Baud rate.

    Text style:0-8
        0x0000 Align upper left,
        0x0001 Align upper center,
        0x0002 Align upper right,
        0x0003 Align left center,
        0x0004 Alignhorizontal and vertical center,
        0x0005 Align right Center,
        0x0006 Align left lower,
        0x0007 Align lower center,
        0x0008 Alignlower right 
    """
    Hd_Rt_SendRealTimeText_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,     # Return type.
        ctypes.c_int,     # nSendType: 0 TCP 1 serial  2 UDP.
        ctypes.c_wchar_p, # pStrParams: IP information (UTF-16 code)   
        ctypes.c_int,     # nRealTimeAreaIndex:Realtime Area index ，start from 0，the return value of Hd_Rt_AddRealAreaToScreen
        ctypes.c_int,     # nMaxPageCount: the max page of realtime area, set to 1
        ctypes.c_int,     # nColor: Screen color. 0 single color, 1 dual color, 2 tricolor. 
        ctypes.c_int,     # nGray: default is 1
        ctypes.c_int,     # nX:Regional X starting point. default set to 0
        ctypes.c_int,     # nY:Regional Y starting point. default set to 0
        ctypes.c_int,     # nWidth: Area width
        ctypes.c_int,     # nHeight: Area height
        ctypes.c_wchar_p, # pText: Text. utf-16 string
        ctypes.c_int,     # nTextColor: text color, default red(255)
        ctypes.c_int,     # nBackGroupColor: default black (0)
        ctypes.c_int,     # nStyle: 4(Alignhorizontal and vertical center)
        ctypes.c_wchar_p, # pFontName: Font name. utf-16 string, default  L"Arial"
        ctypes.c_int,     # nFontHeight: 16 or 12
        ctypes.c_int,     # nShowEffect: effect ID.0 static  1 continue move letf 、2 continue move right.
        ctypes.c_int,     # nShowSpeed: show speed，ms，10～1000ms。default 30.
        ctypes.c_int,     # nStayTime: stay time,second，0～255。defualt 3.
        ctypes.c_int,     # nLiveTime: live time(second).0 allway show.
        ctypes.c_int,     # bSaveToFlash: Save to flash ( 1 still displayed after power failure restart. the screen will blank when send data). The default is 0. 
        ctypes.c_int,)     # dummy: set to 0


    Hd_Rt_SendRealTimeText_Params = (1, "nSendType", 0), (1, "pStrParams", "192.168.2.200:6101"), \
                              (1, "nRealTimeAreaIndex",0), (1, "nMaxPageCount",10), (1, "nColor",0), \
                              (1, "nGray",1),(1, "nX",0),(1, "nY",0),(1, "nWidth",128),(1, "nHeight",16), \
                              (1, "pText","友達預設AUO"),(1, "nTextColor",255),(1, "nBackGroupColor",0),(1, "nStyle",4), \
                              (1, "pFontName","Arial"),(1, "nFontHeight",16), (1, "nShowEffect",0),(1, "nShowSpeed",30), \
                              (1, "nStayTime",3),(1, "nLiveTime",0), (1, "bSaveToFlash",0),(1, "dummy",0)

    Hd_Rt_SendRealTimeText = Hd_Rt_SendRealTimeText_Proto \
                       (("Hd_Rt_SendRealTimeText", hdsdkdll), Hd_Rt_SendRealTimeText_Params)
    nSendType = ctypes.c_int (net_connection_type)

    pStrParams = ctypes.c_wchar_p (ip_addr+":"+str(portid))
    nRealTimeAreaIndex = ctypes.c_int (areaidx)

    # pText = ctypes.c_wchar_p (data)
    # ret = Hd_Rt_SendRealTimeText (nSendType,pStrParams,nRealTimeAreaIndex,pText)

    pText = ctypes.c_wchar_p (data)
    ret = Hd_Rt_SendRealTimeText (nSendType,pStrParams,nRealTimeAreaIndex,pText=data)

    # ret = Hd_Rt_SendRealTimeText (nSendType,pStrParams,nRealTimeAreaIndex,pText.value,pFontName.value)
    return ret



def send_huidu_packet(net_connection_type,ip_addr,port_id,data):

    # some initial value
    ret_dic = {'send_packet_fail':-1,
               'pass':0,
               'conn_type_err':1,
               'port_id_err':2,
               'create_screen_err':3,
               'add_area_err':4
               }
    ret = -1
    area_idx = -1

    # input variables
    if net_connection_type != TCP:
        print('please set net_connection_type to TCP')
        return ret_dic['conn_type_err']
    if port_id !=  PORT_HUIDU:
        print('please set port_id to TCP')
        return ret_dic['port_id_err']

    ret = create_screen()
    if ret != 0:
        return ret_dic['create_screen_err']
        # raise RuntimeError('Can not create the screen for the board')
    area_idx = add_real_area_to_screen()
    if area_idx == -1:
        return ret_dic['add_area_err']
        # raise RuntimeError('Can not add the area to the screen')    

    ret = send_realtime_text(net_connection_type,ip_addr,port_id,area_idx,data)


    # #original version
    # ret = send_screen_to_device(net_connection_type,ip_addr,port_id)
    # if ret == 0:
    #     #font_color = get_color_value()
    #     ret = send_realtime_text(net_connection_type,ip_addr,port_id,area_idx,data)
    # else:
    #     raise RuntimeError('Can not connect to the device! check IP or connection!')

    return ret







# add a Adding a program to the screen
# int HDAPI Hd_AddProgram( void *pBoderImgPath, int nBorderEffect, int nBorderSpeed, void *pExParamsBuf, int nBufSize);
# program_id: -1: failure, other value: program id
def add_program_to_screen():
    # Set up prototype and parameters for the desired function call.
    Hd_AddProgram_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,      # Return type.
        ctypes.c_int,    # dummy1: no use, set to 0
        ctypes.c_int,    # nBorderEffect: set to 0   
        ctypes.c_int,    # nBorderSpeed : Borders speed. 1-9, default is 5.
        ctypes.c_int,    # dummy2: no use, set to 0
        ctypes.c_int)    # dummy3: no use, set to 0

    Hd_AddProgram_Params = (1, "dummy1", 0), (1, "nBorderEffect", 0), (1, "nBorderSpeed",5), \
                           (1, "dummy2",0), (1, "dummy3",0)

    Hd_AddProgram = Hd_AddProgram_Proto \
                                (("Hd_AddProgram", hdsdkdll), Hd_AddProgram_Params)

    program_id = Hd_AddProgram ()
    return program_id



# Adding a program to the designated screen
#  int HDAPI Hd_AddArea(int nProgramID, int nX, int nY, int nWidth, int nHeight,
#                       void *pBoderImgPath, int nBorderEffect, int nBorderSpeed,
#                       void *pExParamsBuf, int nBufSize);
# area_id:  -1: failure, other: area id
def add_area_to_screen(program_id):
    # Set up prototype and parameters for the desired function call.
    Hd_AddArea_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,    # Return type.
        ctypes.c_int,    # nProgramID: specific program id.        
        ctypes.c_int,    # nX: Regional X starting point.
        ctypes.c_int,    # nY: Regional Y starting point.   
        ctypes.c_int,    # nWidth : Area width 
        ctypes.c_int,    # nHeight: Area height
        ctypes.c_int,    # dummy1: no use, set to 0       
        ctypes.c_int,    # nBorderEffect: set to 0 
        ctypes.c_int,    # nBorderSpeed: set to 5 
        ctypes.c_int,    # dummy2: set to 0         
        ctypes.c_int)    # dummy3: set to 0 

    Hd_AddArea_Params = (1, "nProgramID", 0), (1, "nX", 0), (1, "nY", 0), \
                        (1, "width",128), (1, "height",16), (1, "dummy1",0), \
                        (1, "nBorderEffect",0), (1, "nBorderSpeed",5), \
                        (1, "dummy2",0),  (1, "dummy3",0)      

    Hd_AddArea = Hd_AddArea_Proto \
                                (("Hd_AddArea", hdsdkdll), Hd_AddArea_Params)

    nProgramID = ctypes.c_int (program_id)


    area_id = Hd_AddArea (nProgramID)
    return area_id


# Adding a simple text area to the designated area.
# int HDAPI Hd_AddSimpleTextAreaItem(int nAreaID, void *pText, int nTextColor, int nBackGroupColor,
#                                    int nStyle, void *pFontName, int nFontHeight,  int nShowEffect,
#                                    int nShowSpeed, int nClearType, int nStayTime,
#                                    void *pExParamsBuf, int nBufSize); 
# text_area: -1: failure, other value: should be the same with area_idx


def send_simpletext_to_area( area_idx, data):
    # Set up prototype and parameters for the desired function call.
    Hd_AddSimpleTextAreaItem_Proto = ctypes.WINFUNCTYPE (
        ctypes.c_int,      # Return type.
        ctypes.c_int,    # nAreaID: area index
        ctypes.c_wchar_p,    # pText: Text. utf-16 string.   
        ctypes.c_int,    # nTextColor : default red(255).
        ctypes.c_int,    # nBackGroupColor: default black (0)
        ctypes.c_int,    # nStyle: 4(Alignhorizontal and vertical center)
        ctypes.c_wchar_p,# pFontName: Font name. utf-16 string, default  L"Arial"
        ctypes.c_int,    # nFontHeight: 16
        ctypes.c_int,    # nShowEffect: effect ID.0 static  1 continue move letf 、2 continue move right.
        ctypes.c_int,    # nShowSpeed: show speed，ms，10～1000ms。default 30.
        ctypes.c_int,    # nClearType: set to 201.
        ctypes.c_int,    # nStayTime: stay time,second，0～255。defualt 3.
        ctypes.c_int,    # dummy1: no use, set to 0
        ctypes.c_int,)   # dummy2: no use, set to 0




    Hd_AddSimpleTextAreaItem_Params = (1, "nAreaID", 0), (1, "pText", "HELLOGREG"), (1, "nTextColor",255), \
                                      (1, "nBackGroupColor",0), (1, "nStyle",4), (1,"pFontName","Arial"), \
                                      (1, "nFontHeight",16),(1, "nShowEffect",0),(1, "nShowSpeed",30), \
                                      (1, "nClearType",201),(1, "nStayTime",3), \
                                      (1, "dummy1",0),(1, "dummy2",0)



    Hd_AddSimpleTextAreaItem = Hd_AddSimpleTextAreaItem_Proto \
                                (("Hd_AddSimpleTextAreaItem", hdsdkdll), Hd_AddSimpleTextAreaItem_Params)

    nAreaID = ctypes.c_int (area_idx)


    text_area = Hd_AddSimpleTextAreaItem(nAreaID,pText=data )
    return text_area





def send_huidu_simple_text(net_connection_type,ip_addr,port_id,data):

    # some initial value
    ret_dic = {'send_packet_fail':-1,
               'pass':0,
               'conn_type_err':1,
               'port_id_err':2,
               'create_screen_err':3,
               'add_area_err':4,
               'add_program_idx_err':5,
               'add_text_to_area_err':6,
               }
    ret = -1
    area_idx = -1

    # input variables
    if net_connection_type != TCP:
        print('please set net_connection_type to TCP')
        return ret_dic['conn_type_err']
    if port_id !=  PORT_HUIDU:
        print('please set port_id to TCP')
        return ret_dic['port_id_err']

    ret = create_screen()
    if ret != 0:
        return ret_dic['create_screen_err']
        # raise RuntimeError('Can not create the screen for the board')
    program_idx = add_program_to_screen()
    if program_idx == -1:
        return ret_dic['add_program_idx_err']
    area_idx = add_area_to_screen(program_idx)
    if area_idx == -1:
        return ret_dic['add_area_err']
        # raise RuntimeError('Can not add the area to the screen')    

    text_area = send_simpletext_to_area( area_idx, data)
    if text_area != area_idx:
        return ret_dic['add_text_to_area_err']
    ret = send_screen_to_device(net_connection_type,ip_addr,port_id)



    return ret







# =============================================================================
#     
# Main Part
# 
# 
# =============================================================================

if __name__ == "__main__":

    # some initial value
    ret = -1
    area_idx = -1

    # input variables
    net_connection_type = TCP # TCP, UDP, SERIAL
    # ip_addr = '192.168.2.200'
    ip_addr = '255.255.255.255'
    port_id = PORT_HUIDU
    data = 'hello!EWFEWGWEGW'


    if net_connection_type!= TCP:
        raise RuntimeError('Support TCP only, set the net_connection_type to TCP')

    ret = create_screen()
    if ret != 0:
        raise RuntimeError('Can not create the screen for the board')

    area_idx = add_real_area_to_screen()
    if area_idx == -1:
        raise RuntimeError('Can not add the area to the screen')    

    ret=0
    # ret = send_screen_to_device(net_connection_type,ip_addr,port_id)
    if ret == 0:
        #font_color = get_color_value()
        ret = send_realtime_text(net_connection_type,ip_addr,port_id,area_idx,data)



    else:
        raise RuntimeError('Can not connect to the device! check IP or connection!')

    print('the end!!')







# if __name__ == "__main__":
    
#     #MESSAGE = bytearray.fromhex('ffffffff450000006832017b013a00000002000000000003320067320072320065320067320074320065320073320074320067320067320067320067320067320067320067320067000000130b')
    
    
#     #### Configuration variables ####
    
#     net_connection_type = UDP
#     #data = 'gregtestgggggggg'
#     print('輸入你要的字串，最多78個字(中英文都一樣')
#     data = 'q<=.=>p'
    
#     text_change_interval= 3
    
#     ######################################
    
    
    
    
    
#     if net_connection_type == TCP:
#         print('TCP part')
    
    
    
    
        
#     elif net_connection_type == UDP:    
#         ########## UDP: used for broadcast   ########
#         UDP_PORT = PORT    
        
#         # AF_INET is IPv4
#         # SOCK_DGRAM is only for UDP
#         s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        
        
#         message = pack_cp5200data(data,text_change_interval)
        
    
#         print('ready to send message')
#         try:
#             s.sendto(message,(BROADCAST_ADDR,UDP_PORT))
#             s.settimeout(10)
            
#             while 1:
#                 data,addr = s.recvfrom(1024)
#                 if data:
#                     print('get DATA!!')
#                     break
            
#             s.close()
#         except socket.timeout:
#             print('timeout')
#             s.close()
        
        
        
    
#     else:
#         print('choose the connection type first!!')
#         print('set the variable #net_connection_type# to TCP or UDP ')
    
    
#     print('Finished!!!')







