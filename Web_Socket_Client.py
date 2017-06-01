from ws4py.client.threadedclient import WebSocketClient
 
##-----------communication between cordinator and agent

class DummyClient(WebSocketClient):
    def opened(self): 
        self.send("Hello")      

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        print m
        if len(m) == 175:
            self.close(reason='Bye bye')


if __name__ == '__main__':

    try:
##        ws = DummyClient('ws://localhost:8080/Coordinator/websocketserver', protocols=['http-only', 'chat'])
        ws = DummyClient('ws://192.168.8.102:8080/Coordinator/websocketserver', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:        
        ws.close()
   
