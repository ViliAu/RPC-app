from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import data.datamanager as datamanager

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class server_rpc_commands:
    def __init__(self) -> None:
        self.DB = datamanager.DB("./data/db.xml")
    def add_note(self, topic: str, title: str, text: str, search_terms: str):
        self.DB.add_note(datamanager.Note(topic, title, text), search_terms)
        return "Note added!"
    def find_note(self, topic: str):
        notes = self.DB.find_topic(topic)
        if notes is None:
            return "Could find note!"
        else:
            return notes


# Creates server
def create_server():
    with SimpleXMLRPCServer(('localhost', 8000),
                            requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        server.register_instance(server_rpc_commands())

        # Run the server's main loop
        try:
            print("Server started! Close server with ctrl + c")
            server.serve_forever()
        except KeyboardInterrupt:
            print("Closing server.")
            server.server_close()

if __name__ == '__main__':
    create_server()