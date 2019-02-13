# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
import time


# noinspection PyPep8Naming
class SibylClientUdpTextProtocol(DatagramProtocol):

    def __init__(self, sibylClientProxy, port, host):
        self.serverAddress = host
        self.serverPort = port
        self.clientProxy = sibylClientProxy

    def sendRequest(self, line):
        timestamp = time.time()
        datagram = str(int(timestamp)) + ': ' + line + '\r\n'
        question = bytes(datagram, 'utf-8')
        self.transport.write(question, (self.serverAddress, self.serverPort))

    def datagramReceived(self, datagram, hostPort):
        responseText = str(datagram).split(':')[1][:-5]
        self.clientProxy.responseReceived(responseText)
