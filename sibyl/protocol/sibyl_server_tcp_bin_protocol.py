# -*- coding: utf-8 -*-
from twisted.internet.protocol import Protocol
from sibyl.main.sibyl_brain import SibylBrain
import struct

def unpack_helper(ftm, data):
    size = struct.calcsize(ftm)
    return struct.unpack(ftm,data[:size]) , data[size:]

class SibylServerTcpBinProtocol(Protocol):
    """The class implementing the Sibyl TCP binary server protocol.

        .. note::
            You must not instantiate this class.  This is done by the code
            called by the main function.

        .. note::

            You have to implement this class.  You may add any attribute and
            method that you see fit to this class.  You must implement the
            following method (called by Twisted whenever it receives data):
            :py:meth:`~sibyl.main.protocol.sibyl_server_tcp_bin_protocol.dataReceived`
            See the corresponding documentation below.

    This class has the following attribute:

    .. attribute:: SibylServerProxy

        The reference to the SibylServerProxy (instance of the
        :py:class:`~sibyl.main.sibyl_server_proxy.SibylServerProxy` class).

            .. warning::

                All interactions between the client protocol and the server
                *must* go through the SibylServerProxy.

    """

    def __init__(self, sibylServerProxy):
        """The implementation of the UDP server text protocol.

        Args:
            sibylServerProxy: the instance of the server proxy.
        """
        self.sibylServerProxy = sibylServerProxy
        self.data=bytes('','utf-8')
    
    def dataReceived(self, line):
        """Called by Twisted whenever a data is received

        Twisted calls this method whenever it has received at least one byte
        from the corresponding TCP connection.

        Args:
            line (bytes): the data received (can be of any length greater than
            one);

        .. warning::
            You must implement this method.  You must not change the parameters,
            as Twisted calls it.

        """
        self.data=self.data+line
        if len(self.data)>=6:
            length=unpack_helper('!IH',self.data)[0][1]
            if len(self.data)>=length:
                timestamp=unpack_helper('!IH',self.data)[0][0]
                questionText=str(unpack_helper('!IH',self.data)[1],'utf-8')
                text=self.sibylServerProxy.generateResponse(questionText)
                response=struct.pack('!IHZs'.replace('Z',str(len(text))),timestamp,len(text)+6,bytes(text,'utf-8'))
                self.transport.write(response)
                self.data=bytes('','utf-8')
    
