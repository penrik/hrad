#!/usr/bin/python3
from pyrad import dictionary, packet, server
import logging

print ("Starting hrad v1.0")

logging.basicConfig(filename="pyrad.log", level="DEBUG",
                    format="%(asctime)s [%(levelname)-8s] %(message)s")

class HradServer(server.Server):

    def _HandleAuthPacket(self, pkt):
        server.Server._HandleAuthPacket(self, pkt)

        print("")
        print("Received an authentication request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))
        #Här kan man gå lös sen
        if attr == "User-Name" and pkt[attr][0] == "henrik":
            reply = self.CreateReplyPacket(pkt, **{
                "Service-Type": "Framed-User",
                "Framed-IP-Address": '192.168.0.10',
            })
            reply.code = packet.AccessAccept
            self.SendReplyPacket(pkt.fd, reply)
        else:
            reply = self.CreateReplyPacket(pkt)
            reply.code = packet.AccessReject
            self.SendReplyPacket(pkt.fd, reply)


if __name__ == '__main__':
    srv = HradServer(dict=dictionary.Dictionary("dictionary"))

    srv.hosts["127.0.0.1"] = server.RemoteHost("127.0.0.1", b"secret", "127.0.0.1")
    srv.BindToAddress("")

    srv.Run()
