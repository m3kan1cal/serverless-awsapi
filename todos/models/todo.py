import time
from smalluuid import SmallUUID

class ToDoModel:
    def __init__(self, table, text):
        self.table = table
        self.text = text

    def save(self):
        """Save a model to the database."""

        timestamp = int(time.time() * 1000)
        item = {
            "id": str(SmallUUID()),
            "text": self.text,
            "checked": False,
            "createdAt": timestamp,
            "updatedAt": timestamp,
        }

        # Write the item to the database.
        self.table.put_item(Item=item)

        return item
