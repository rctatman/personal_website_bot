# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3
import random


class QueryResourceType(Action):

    def name(self) -> Text:
        return "query_resource_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = create_connection("../edu_db/resourcesDB")

        slot_value = tracker.get_slot("resource_type")
        slot_name = "Type"

        get_query_results = select_by_slot(conn,slot_name,slot_value)
        dispatcher.utter_message(text=get_query_results)

        return []

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_by_slot(conn, slot_name, slot_value):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM eduresource
                WHERE {slot_name}='{slot_value}'""")

    rows = cur.fetchall()

    if len(list(rows)) < 1:
        return[("There are no resources matching your query.")]
    else:
        for row in random.sample(rows, 1):
            return[print(f"Try the {(row[4]).lower()} {row[0]} by {row[1]}. You can find it at {row[2]}.")]