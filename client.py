from sqlite3 import Timestamp
import xmlrpc.client
import traceback

def menu():
    return int(
input(
"""
1) Add a note
2) Fetch a note
0) Exit
"""))

def start_client():
    with xmlrpc.client.ServerProxy('http://localhost:8000') as proxy:
        if proxy:
            try:
                while True:
                    i = menu()
                    if i == 0:
                        print("Closing client.")
                        break
                    elif i == 1:
                        send_note(proxy)
                    elif i == 2:
                        find_note(proxy)
                    else:
                        print("Invalid choice\n")
            except KeyboardInterrupt:
                print("Closing client.")
        else:
            print("Couldn't connect to server.")
        
def send_note(proxy):
    topic = input("Give a topic: ")
    title = input("Give a title: ")
    text = input("Give text for the note: ")
    search_terms = input("Give wikipedia search terms (optional):")
    try:
        proxy.add_note(topic, title, text, search_terms)
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