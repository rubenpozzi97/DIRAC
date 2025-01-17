""" This is a simple example of implementation of a Ping/Pong service for executors.

    This service does not any specific configuration to run, only the Port number, and authz e.g.:

    {
      Port = 9145
      {
        Authorization
        {
          Default = all
        }
      }
    }
"""
from DIRAC import S_OK
from DIRAC.Core.DISET.RequestHandler import RequestHandler


class PingPongHandler(RequestHandler):

    MSG_DEFINITIONS = {"Ping": {"id": int}, "Pong": {"id": int}}

    auth_conn_connected = ["all"]

    def conn_connected(self, trid, identity, kwargs):
        """
        This function will be called when a new client connects.
        It is not mandatory to have this function

        params:
          @trid: Transport ID: Unique for each connection
          @identity: Unique for each client even if it reconnects
          @kwargs: Arguments sent by the client for the connection
        """
        # Do something with trid/identity/kwargs if needed
        return S_OK()

    auth_conn_drop = ["all"]

    def conn_drop(self, trid):
        """
        This function will be called when a client disconnects.
        It is not mandatory to have this function
        """
        return S_OK()

    auth_msg_Ping = ["all"]

    def msg_Ping(self, msgObj):
        """
        Callback for Ping message
        """
        pingid = msgObj.id
        result = self.srv_msgCreate("Pong")
        if not result["OK"]:
            # Something went wrong :P
            return result
        pongObj = result["Value"]
        pongObj.id = pingid
        # Could have been
        # return self.srv_msgReply( pongObj )
        return self.srv_msgSend(self.srv_getTransportID(), pongObj)
