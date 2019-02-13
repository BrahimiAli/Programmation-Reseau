# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
import time
import struct


class SibylClientUdpBinProtocol(DatagramProtocol):

    def __init__(self, sibylClientProxy, port, host):
        self.serverAddress = host
        self.serverPort = port
        self.clientProxy = sibylClientProxy

    def sendRequest(self, line):
        timestamp = int(time.time())
        lineLength = len(line)
        line = bytes(line, 'utf-8')
        datagram = struct.pack('>IHZs'.replace('Z', str(lineLength)), timestamp, lineLength+6, line)
        self.transport.write(datagram, (self.serverAddress, self.serverPort))

    def datagramReceived(self, datagram, hostPort):
        length = struct.unpack('>H', datagram[4:6])[0]
        unpackedDatagram = struct.unpack('>IHZs'.replace('Z', str(length-6)), datagram)
        responseText = unpackedDatagram[2].decode('utf-8')
        self.clientProxy.responseReceived(responseText)
