# -*- coding: utf-8 -*-
import struct
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from sibyl.main.sibyl_brain import SibylBrain



class SibylServerTimerUdpBinProtocol(DatagramProtocol):

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
        def send_response(response_host_port): #tuple
             self.transport.write(response_host_port[0], response_host_port[1])
        reactor.callLater(len(questionText),send_response,(response,hostPort))
       
