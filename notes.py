import json
from datetime import datetime


class Note:
    def __init__(self, id, title, body, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __str__(self):
        return f"{self.id}: {self.title}\n{self.body}\nСоздано: {self.created_at}\nДополнено: {self.updated_at}\n"


class Notes:
    def __init__(self, filename):
        self.filename = filename
        self.notes = []
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                notes_data = json.load(f)
                for note_data in notes_data:
                    created_at = datetime.fromisoformat(
                        note_data['created_at'])
                    updated_at = datetime.fromisoformat(
                        note_data['updated_at'])
                    note = Note(note_data['id'], note_data['title'],
                                note_data['body'], created_at, updated_at)
                    self.notes.append(note)
        except FileNotFoundError:
            pass
        

    def save(self):
        notes_data = [note.to_dict() for note in self.notes]
        with open(self.filename, 'w') as f:
            json.dump(notes_data, f, default=datetime_to_str, indent=4)

    def add(self, title, body):
        id = len(self.notes) + 1
        note = Note(id, title, body)
        self.notes.append(note)
        self.save()

    def edit(self, id, title=None, body=None):
        note = self.get(id)
        if title is not None:
            note.title = title
        if body is not None:
            note.body = body
        note.updated_at = datetime.now()
        self.save()

    def delete(self, id):
        note = self.get(id)
        self.notes.remove(note)
        self.save()

    def get(self, id):
        for note in self.notes:
            if note.id == id:
                return note
        raise ValueError(f"Note with id={id} not found")

    def list_notes(self):
        for note in self.notes:
            print(note)

    def filter_by_date(self, start_date=None, end_date=None):
        filtered_notes = []
        for note in self.notes:
            if start_date is not None and note.created_at.date() < start_date:
                continue
            if end_date is not None and note.created_at.date() > end_date:
                continue
            filtered_notes.append(note)
        return filtered_notes


def datetime_to_str(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


if __name__ == '__main__':
    notes = Notes('notes.json')

    while True:
        print("Select command:")
        print("1. Add")
        print("2. Edit")
        print("3. Delete")
        print("4. Get")
        print("5. List")
        print("6. Filter by date")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            title = input("Enter title: ")
            body = input("Enter body: ")
            notes.add(title, body)
        elif choice == '2':
            id = int(input("Enter id: "))
            title = input("Enter new title (leave empty to skip): ")
            body = input("Enter new body (leave empty to skip): ")
            notes.edit(id, title, body)
        elif choice == '3':
            id = int(input("Enter id: "))
            notes.delete(id)
        elif choice == '4':
            id = int(input("Enter id: "))
            note = notes.get(id)
            print(note)
        elif choice == '5':
            notes.list_notes()
        elif choice == '6':
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            filtered_notes = notes.filter_by_date(start_date, end_date)
            for note in filtered_notes:
                print(note)
        elif choice == '7':
            break
        else:
            print("Invalid choice")