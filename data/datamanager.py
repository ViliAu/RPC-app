from datetime import datetime
import xml.etree.ElementTree as ET
from os.path import exists
import requests

class Note:
    def __init__(self, topic, title, text) -> None:
        self.topic = topic
        self.title = title
        self.text = text
        self.timestamp = str(datetime.now())

class DB:
    def __init__(self, path) -> None:
        self.path = path
        if (exists(path)):
            self.tree = ET.parse(path)
            self.root = self.tree.getroot()
        else:
            self.root = ET.Element("data")
            self.tree = ET.ElementTree(self.root)
            self.tree.write("db.xml")

    def find_topic(self, topic: str):
        topic_element = self.root.find(f"topic[@name='{topic}']")
        if topic_element:
            note_list = []
            note_list.append(f"\n\tNotes for topic {topic}:\n")
            for note in topic_element.findall('note'):
                note_list.append(f"\tTitle: {note.get('name')}\n\tText: {note.find('text').text}\n\tCreated: {note.find('timestamp').text}")
                link = note.find('link')
                if link != None:
                    print(link.text)
                    note_list.append(f"\tRelated article: {link.text}")
            return "\n".join(note_list)
        else:
            return None

    def add_note(self, note: Note, search_terms: str):
        new_topic = self.root.find(f"topic[@name='{note.topic}']")
        if new_topic is None:
            new_topic = ET.SubElement(self.root,"topic", name=note.topic)
        note_title = ET.SubElement(new_topic, "note", name=note.title)

        # Add timestamp and text
        ET.SubElement(note_title, "text").text = note.text
        ET.SubElement(note_title, "timestamp").text = note.timestamp

        # Get wikipedia links and add them to the note
        self.add_link_element(note_title, search_terms)

        # Write note to db
        self.tree.write(self.path)

    def add_link_element(self, note, search_terms):
        if len(search_terms) == 0:
            return
        wiki_link = self.query_wikipedia(search_terms)
        if wiki_link:
            ET.SubElement(note, "link").text = wiki_link

    def query_wikipedia(self, search_terms: str):
        session = requests.Session()
        URL = "https://en.wikipedia.org/w/api.php"
        PARAMS = {
            "action": "opensearch",
            "format": "json",
            "namespace": "0",
            "search": search_terms,
            "limit": "1"
        }
        try:
            response = session.get(url=URL, params=PARAMS)
            return response.json()[3][0]
        except:
            return None
                