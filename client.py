from sqlite3 import Timestamp
import xmlrpc.client
import traceback

def menu():
    return int(
input(
"""
0) Exit
1) Send a note to the server
2) Fetch a note
3) Query wikipedia
"""))

def start_client():
    with xmlrpc.client.ServerProxy('http://localhost:8000') as proxy:
        if proxy:
            while True:
                i = menu()
                if i == 0:
                    break
                elif i == 1:
                    send_note(proxy)
                elif i == 2:
                    find_note(proxy)
                else:
                    print("Invalid choice\n")
        else:
            print("Couldn't connect to server.")
        
def send_note(proxy):
    topic = input("Give a topic: ")
    title = input("Give a title: ")
    text = input("Give text for the note: ")
    try:
        proxy.add_note(topic, title, text)
        print("Note added!")
    except:
        traceback.print_exc
        print("Couldn't add note.")


def find_note(proxy):
    try:
        topic = input("Give a topic: ")
        print(proxy.find_note(topic))
    except:
        print("Couldn't find topic")

client_commands = {
    send_note
}

if __name__ == '__main__':
    start_client()