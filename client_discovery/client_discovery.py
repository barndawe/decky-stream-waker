import socket
import steamdiscover_pb2
import math
import random


class SteamClientDetail:
    def __init__(self, body: steamdiscover_pb2.CMsgRemoteClientBroadcastStatus):
        self.host = body.hostname
        self.mac = body.mac_addresses[0]

class SteamClientDiscover:
    _seq_num = 1
    _magic_bytes = bytes([0xff, 0xff, 0xff, 0xff, 0x21, 0x4c, 0x5f, 0xa0])
    _int_bytes = 4

    def get_active_network_client_details(self) -> list[SteamClientDetail]:
        disco_message = self._build_discovery_message()

        client_responses = self._send_disco_message(disco_message)

        for message in client_responses:
            body = self._decode_steam_message_response(message)
            yield SteamClientDetail(body)

    def _build_discovery_message(self) -> bytes:
        disco_message_array = bytearray()

        #add magic byte packet for Steam
        disco_message_array.extend(self._magic_bytes)

        #build and add header length and content
        header = steamdiscover_pb2.CMsgRemoteClientBroadcastHeader()
        header.client_id = math.ceil(random.random() * 100000000)
        header.msg_type = steamdiscover_pb2.k_ERemoteClientBroadcastMsgDiscovery              

        header_array = header.SerializeToString()
        disco_message_array.extend(len(header_array).to_bytes(self._int_bytes, byteorder="little"))
        disco_message_array.extend(header_array)

        #build and add body length and content
        body = steamdiscover_pb2.CMsgRemoteClientBroadcastDiscovery()
        body.seq_num = self._seq_num
        self._seq_num += 1

        body_array = body.SerializeToString()
        disco_message_array.extend(len(body_array).to_bytes(self._int_bytes, byteorder="little"))
        disco_message_array.extend(body_array)

        return bytes(disco_message_array)

    def _send_disco_message(self, disco_message: bytes) -> list[bytes]:
        disco_responses: list[bytes] = []        

        #setup socket for UDP with 2.5 second timeout and broadcast the discovery message
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.settimeout(5)
        sock.sendto(disco_message, ("<broadcast>", 27036))
        
        #read back responses until the timeout happens
        try:
            while True:
                data, ip = sock.recvfrom(1024)
                disco_responses.append(data)
                print(f"Received message from {ip}")

        except socket.timeout:
            print("scan finished")

        return disco_responses

    def _decode_steam_message_response(self, response: bytes) -> steamdiscover_pb2.CMsgRemoteClientBroadcastStatus:
        #not interested if this isn't a Steam message
        if not response.startswith(self._magic_bytes):
            print("Non-Steam message received")
            return
        
        #read header and advance offset to after header
        offset = len(self._magic_bytes)
        
        header_length = int.from_bytes(response[offset:offset + self._int_bytes], byteorder="little")

        offset = offset + self._int_bytes

        header_array = response[offset:offset+ header_length]
        header =  steamdiscover_pb2.CMsgRemoteClientBroadcastHeader()
        header.ParseFromString(header_array)

        offset = offset + header_length
        
        #not interested if the message isn't a client status one
        if not header.msg_type == steamdiscover_pb2.k_ERemoteClientBroadcastMsgStatus:
            return
        
        #read body and return it
        body_length = int.from_bytes(response[offset:offset + self._int_bytes], byteorder="little")

        offset = offset + self._int_bytes

        body_array = response[offset:offset + body_length]
        body = steamdiscover_pb2.CMsgRemoteClientBroadcastStatus()
        body.ParseFromString(body_array)

        return body
