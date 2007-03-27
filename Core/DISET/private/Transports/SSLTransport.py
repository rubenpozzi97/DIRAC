# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/Core/DISET/private/Transports/SSLTransport.py,v 1.2 2007/03/27 10:56:47 acasajus Exp $
__RCSID__ = "$Id: SSLTransport.py,v 1.2 2007/03/27 10:56:47 acasajus Exp $"

import OpenSSL
from DIRAC.Core.DISET.private.Transports.BaseTransport import BaseTransport
from DIRAC.LoggingSystem.Client.Logger import gLogger

class SSLTransport( BaseTransport ):
    
  def _write( self, sBuffer ):
    self.oSocket.send( sBuffer )
    
  def _read( self ):
    try:
      return self.oSocket.recv( 8192 )
    except socket.error:
      return ""
  
  def getUserInfo( self ):
    return {}
  
  def initAsClient( self ):
    self.oSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    self.oSocket.connect( self.stServerAddress )
  
  def initAsServer( self ):
    if not self.serverMode():
      raise RuntimeError( "Must be initialized as server mode" )
    self.oSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    if self.bAllowReuseAddress:
      self.oSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    self.oSocket.bind( self.stServerAddress )
    self.oSocket.listen( self.iListenQueueSize )
    
  def close( self ):
    gLogger.debug( "Closing socket" )
    self.oSocket.close()
    
  def setClientSocket( self, oSocket ):
    if self.serverMode():
      raise RuntimeError( "Mustbe initialized as client mode" )
    self.oSocket = oSocket
    
  def acceptConnection( self ):
    oClientTransport = PlainTransport( self )
    oClientSocket, stClientAddress = self.oSocket.accept() 
    oClientTransport.setClientSocket( oClientSocket )
    return oClientTransport
    
