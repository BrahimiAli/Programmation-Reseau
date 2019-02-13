# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from sibyl.main.sibyl_brain import SibylBrain


class SibylServerUdpTextProtocol(DatagramProtocol):

    def __init__(self, sibylServerProxy):
        self.sibylServerProxy = sibylServerProxy

    def datagramReceived(self, datagram, hostPort):
        questionText = str(datagram).split(':')[1][:-4]
        text = self.sibylServerProxy.generateResponse(questionText)
        data = str(datagram).split(':')[0] + ': ' + text + '\r\n'
        self.transport.write(bytes(data, 'utf-8'), hostPort)
