import json
import time

import boto3
from boto3.dynamodb.conditions import Key
import botocore
from smalluuid import SmallUUID


class NoteModel:
    def __init__(self, table):
        self.table = table

    def save(self, user_id, notebook, text):
        """Write an item to the database."""

        timestamp = int(time.time() * 1000)
        item = {
            "noteId": str(SmallUUID()),
            "userId": user_id,
            "notebook": notebook,
            "text": text,
            "createdAt": timestamp,
            "updatedAt": timestamp,
        }

        self.table.put_item(Item=item)

        return item

    def read(self, note_id):
        """Fetch item from the database."""

        item = self.table.get_item(
            Key={
                "noteId": note_id
            }
        )

        return item["Item"] if "Item" in item else {}

    def update(self, note_id, data):
        """Update item in the database."""

        timestamp = int(time.time() * 1000)
        
        try:
            item = self.table.update_item(
                Key={
                    "noteId": note_id
                },
                UpdateExpression="SET #notebook = :notebook, #note_text = :text, updatedAt = :updatedAt",
                ExpressionAttributeNames={
                    "#notebook": "notebook",
                    "#note_text": "text"
                },
                ExpressionAttributeValues={
                    ":notebook": data["notebook"],
                    ":text": data["text"],
                    ":updatedAt": timestamp,
                },
                # Only update if item already exists in database.
                ConditionExpression="attribute_exists(noteId)",
                ReturnValues="ALL_NEW",
            )
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return {}

        return item["Attributes"] if "Attributes" in item else {}

    def delete(self, note_id):
        """Delete item from the database."""

        item = self.table.delete_item(
            Key={
                "noteId": note_id
            }
        )

        return item["Item"] if "Item" in item else {}

    def search_by_user(self, user_id):
        """Search for items in the database based on user."""

        # Fetch all items from the database by index.
        items = self.table.query(
            IndexName="stoic-notes-dev-userid-noteid-index", # @todo Make this dynamically pull from config
            ExpressionAttributeNames={
                "#note_text": "text"
            },
            ProjectionExpression="userId, noteId, notebook, #note_text",
            KeyConditionExpression=Key("userId").eq(user_id),
            ScanIndexForward=True
        )

        return items["Items"] if "Items" in items else {}

    def search_by_notebook(self, notebook):
        """Search for items in the database based on notebook."""

        # Fetch all items from the database by index.
        items = self.table.query(
            IndexName="stoic-notes-dev-notebook-noteid-index", # @todo Make this dynamically pull from config
            ExpressionAttributeNames={
                "#note_text": "text"
            },
            ProjectionExpression="userId, noteId, notebook, #note_text",
            KeyConditionExpression=Key("notebook").eq(notebook),
            ScanIndexForward=True
        )

        return items["Items"] if "Items" in items else {}
    
