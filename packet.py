import socket
from math import ceil


#### CONSTANTS  #####
PORT = 5200
BROADCAST_ADDR = '255.255.255.255'
UDP_RX_ADDR = "127.0.0.1"

# the value add to the length of input strings will be the correct len in the
# field "NW_DataLen"
NW_DATA_LEN_FIXED_BYTES = 11




TCP=1
UDP=2




def pack_cp5200data(data,text_change_interval):
    
### Input parameters:
# data: input strings; maximum 78texts(chinese/english)
# text_change_interval: the interval for each line of text change to next line
#                       unit is second. valid range: from 0 to 65535    

### Packet format, all values shown in hex in str type without 0x prefix!!
#   
# ID: Control card ID. fixed value 'ffffffff'
# NW_DataLen: the byte length from "packet type" to "packet data check sum"    
#             valid values: '0000' ~ 'ffff'
# Reserved: '0000'
# PacketType: recognition of this type of data. fixed value '68'
# CardType: fixed value '32'
# CardID: Control card ID and Screen No.
#         valid values: '01'~'fe':specific card ID
#                       'ff': the group address, force receive data      
# ProtocolCode: recognition of this type of protocol.
#               fixed value '7b'    
# AdditionalConfirm: whether to return a confirmation
#                    '00': no need return
#                    '01': need to return a confirmation
#                    when the PacketDataLen >'c8'(200 bytes), we will divide
#                    the packet into several sub-packet. Only the first 
#                    sub-packet need to set AdditionalConfirm to '01'
#                    the remained sub-packet should set to '00'    
#    
# PacketDataLen: the length of the CC part content. Lower byte in former LL LH
#                len = CC-code(1byte) window(1byte)+Mode(1byte)
#                      +Alignment(1byte)+Speed(1byte)+staytime(2byte)
#                      + char num * (3 bytes) + CC end (3byte)
#                valid values: '0000'~'ffff'
#                NOTE: if PacketDataLen > 'c8', it will be fixed to 'c8',
#                      and there will be more sub-packets.     
# PacketNum: the current packet(sub-packet) number.
#            when PacketNum == LastPacketNum, means this is last packet
#            valid values: '00'~ value of LastPacketNum   
# LastPacketNum   : the total number of packet -1
#                   LastPacketNum = ceil(PacketDataLen / 'c8') - 1
# CCCode:    the command sub-code, specify the meaning of the data
#            valid values: '01'~'8d', currentlt use '02'
#                          '02': send text data to specific window
# TextWindowNum: the window number
#                valid values '00'~ '07' , now fixed to '00'
# TextEffectMode: the special effect for the text.
#                 '00': draw
#                 '01': open from left
#                 '05': Shutter(vertical)
#                 '0b': scroll to left    
# TextAlignment: the alignment of the text
#                '00': left-aligned
#                '01': Horizontal center
#                '02': right-aligned
# TextSpeed:  the speed of text moving. the smaller the faster
#             valid values: '00'~'64'
# TextStayTime: the stay time of each four text, unit: second
#               valid values: '0000'~'ffff'    
# CCContent: the data strings each charachter is made of 3 bytes
#            first byte: font style
#                        [7:4]: color: 1: red
#                        [3:0]: size: 1:size8,2:size16
#                        currently choose '12', font (red,size=16)
#            byte[3:2]: the big5 ASCII code.      
#
# CCEndContent: fixed value '000000'   
# CheckSum: the check sum from "NW_DataLen" to "packet data content"
#           lower byte in former, the document format is error    
#    

    

    
    
    ID = 'ffffffff'
    #NW_DataLen = 0
    Reserved = '0000'
    PacketType = '68'
    CardType = '32'
    CardID = '01'
    ProtocolCode = '7b'
    AdditionalConfirm = '01'
    #PacketDataLen = 0
    #PacketNum = 0
    #LastPacketNum = 0
    #PacketData = data
    
    
    pack_data_len = len(data)*3 +10
    PacketDataLen = format(pack_data_len,'x').zfill(4)
    # PacketDataLen need to change low byte and high byte
    PacketDataLen = PacketDataLen[2:]+PacketDataLen[0:2]
    
    
    
    last_pack_num = ceil(pack_data_len/65535)-1
    LastPacketNum = format(last_pack_num,'x').zfill(2)
    
    PacketNum = '00'
    
    CCCode = '02'
    TextWindowNum = '00'
    TextEffectMode = '00'
    TextAlignment = '00'
    TextSpeed = '00'
    TextStayTime = format(text_change_interval,'x').zfill(4)
    
    CCEndContent = '000000'
    
    
    # accumulate the amount of bytes from packet type to checksum
    nw_data_len = NW_DATA_LEN_FIXED_BYTES+ pack_data_len
    NW_DataLen = format(nw_data_len,'x').zfill(4)
    # NW_Datalen need to change low byte and high byte
    NW_DataLen = NW_DataLen[2:]+NW_DataLen[0:2]
    

    
    # tmp_byte is the content of packing the character to 3 byte format
    font_type_byte_format = bytearray()
    font_type_byte_format.append(18)
    ascii_byte = bytearray()
    ascii_byte.append(0)
    
    
    tmp_byte = bytearray()
    
#    print('data is ',data)
#    print('len of data is ',len(data))
    for i in range(len(data)):
        tmp_text_byte = bytearray(data[i],encoding=('big5'))
        if tmp_text_byte.isascii() is True:
            tmp_byte = tmp_byte + font_type_byte_format +ascii_byte + tmp_text_byte
        else:
            tmp_byte = tmp_byte + font_type_byte_format +tmp_text_byte
    
    
    # data_hex is the content before the strings(3bytes of each text)
    data_hex = ID+NW_DataLen+Reserved+PacketType+CardType+CardID+ProtocolCode\
              + AdditionalConfirm + PacketDataLen + PacketNum + LastPacketNum\
              + CCCode + TextWindowNum + TextEffectMode + TextAlignment\
              + TextSpeed + TextStayTime
              
#    print(data_hex)
    
    
    ret_byte =bytearray.fromhex(data_hex)
    
    ret_byte = ret_byte + tmp_byte
    
    # calculate the check sum (ignore ID'ffffffff' so start from index5)
    # the field only has 16-bits , so mask with 0xffff
    # the document says start from 'packettype', but is actually starts
    # from 'NW_DataLen'!!!!!!
    checksum = sum(list(ret_byte)[5:])&0xffff
    
    CheckSum = format(checksum,'x').zfill(4)
    # CheckSum need to change low byte and high byte
    CheckSum = CheckSum[2:]+CheckSum[0:2]
    
    end_hex = CCEndContent + CheckSum

    
    ret_byte = ret_byte + bytearray.fromhex(end_hex)


    
    
    return ret_byte







# =============================================================================
#     
# Main Part
# 
# 
# =============================================================================

if __name__ == "__main__":
    
    #MESSAGE = bytearray.fromhex('ffffffff450000006832017b013a00000002000000000003320067320072320065320067320074320065320073320074320067320067320067320067320067320067320067320067000000130b')
    
    
    #### Configuration variables ####
    
    net_connection_type = UDP
    #data = 'gregtestgggggggg'
    print('輸入你要的字串，最多78個字(中英文都一樣')
    data = 'q<=.=>p'
    
    text_change_interval= 3
    
    ######################################
    
    
    
    
    
    if net_connection_type == TCP:
        print('TCP part')
    
    
    
    
        
    elif net_connection_type == UDP:    
        ########## UDP: used for broadcast   ########
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
                    break
            
            s.close()
        except socket.timeout:
            print('timeout')
            s.close()
        
        
        
    
    else:
        print('choose the connection type first!!')
        print('set the variable #net_connection_type# to TCP or UDP ')
    
    
    print('Finished!!!')







