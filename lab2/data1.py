import xml.etree.ElementTree as ET
import xml.sax
from Pet import Pet


class XmlDomWriter:
    def __init__(self, filename):
        self.filename = filename

    def write(self, pets_list):
        root = ET.Element("VeterinaryClinic")
        for pet in pets_list:
            pet_elem = ET.SubElement(root, "Pet")
            data = pet.to_dict()

            ET.SubElement(pet_elem, "Name").text = data['name']
            ET.SubElement(pet_elem, "Birthday").text = data['birthday']
            ET.SubElement(pet_elem, "LastVisit").text = data['last_visit_date']
            ET.SubElement(pet_elem, "VetName").text = data['vet_name']
            ET.SubElement(pet_elem, "Diagnosis").text = data['diagnosis']

        tree = ET.ElementTree(root)
        tree.write(self.filename, encoding="utf-8", xml_declaration=True)

        print(f" Данные успешно сохранены в {self.filename} (DOM)")

class PetSaxHandler(xml.sax.ContentHandler):

    def __init__(self):
        super().__init__()
        self.current_data = ""

        self.pets = []
        self.name = ""
        self.birthday = ""
        self.last_visit = ""
        self.vet_name = ""
        self.diagnosis = ""

    def startElement(self, tag, attributes):
        self.current_data = tag

        if tag == "Pet":
            self.name = ""
            self.birthday = ""
            self.last_visit = ""
            self.vet_name = ""
            self.diagnosis = ""

    def endElement(self, tag):
        if tag == "Pet":
            pet = Pet(
                name=self.name,
                birthday=self.birthday,
                last_visit_date=self.last_visit,
                vet_name=self.vet_name,
                diagnosis=self.diagnosis
            )
            self.pets.append(pet)

    def characters(self, content):
        if self.current_data == "Name":
            self.name += content
        elif self.current_data == "Birthday":
            self.birthday += content
        elif self.current_data == "LastVisit":
            self.last_visit += content
        elif self.current_data == "VetName":
            self.vet_name += content
        elif self.current_data == "Diagnosis":
            self.diagnosis += content

    def get_pets(self):
        return self.pets


class XmlSaxReader:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        handler = PetSaxHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)

        try:
            parser.parse(self.filename)
            print(f" Данные успешно загружены из {self.filename} (SAX)")
            return handler.get_pets()
        except FileNotFoundError:
            print(f" Ошибка: Файл {self.filename} не найден.")
            return []
        except Exception as e:
            print(f" Ошибка при чтении файла: {e}")
            return []