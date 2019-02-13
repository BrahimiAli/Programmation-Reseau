# -*- coding: utf-8 -*-
import struct
from twisted.internet.protocol import DatagramProtocol
from sibyl.main.sibyl_brain import SibylBrain


class SibylServerUdpBinProtocol(DatagramProtocol):

    def __init__(self, sibylServerProxy):
        self.sibylServerProxy = sibylServerProxy

    def datagramReceived(self, datagram, hostPort):
        length = struct.unpack('>H', datagram[4:6])[0]
        unpackedDatagram = struct.unpack('>IHZs'.replace('Z', str(length-6)), datagram)
        timestamp = unpackedDatagram[0]
        questionText = unpackedDatagram[2]
        sibylResponse = bytes(self.sibylServerProxy.generateResponse(questionText), 'utf-8')
        responseLength = len(sibylResponse)
        response = struct.pack('>IHZs'.replace('Z', str(responseLength)), timestamp, responseLength+6, sibylResponse)
        self.transport.write(response, hostPort)
