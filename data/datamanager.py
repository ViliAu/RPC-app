from datetime import datetime
import xml.etree.ElementTree as ET
from os.path import exists

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
        root_note = self.root.find(f"topic[@name='{topic}']")
        if root_note:
            noteList = []
            for note in root_note.findall('note'):
                noteList.append(f"{note.get('name')}: {note.find('Text').text}")
            return "\n".join(noteList)
        else:
            return None

    def add_note(self, note: Note):
        if note:
            new_topic = self.root.find(f"topic[@name='{note.topic}']")
            if new_topic is None:
                new_topic = ET.SubElement(self.root,"topic", name=note.topic)
            note_title = ET.SubElement(new_topic, "note", name=note.title)
            ET.SubElement(note_title, "Text").text = note.text
            ET.SubElement(note_title, "timestamp").text = note.timestamp
            self.tree.write(self.path)
