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


# TODO: 
# - query more than one field/column at a time
# - if nothing matches both fields return results that match
#   at least one
# - data validation for close but not exact matches


# multifield query process:
# - first look for both
# - second look for either, inform not perfect match
# - third use LIKE to find acceptably close resutls
# - fourth return no results

class QueryResourceType(Action):

    def name(self) -> Text:
        return "query_resource_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection(db_file="./edu_db/resourcesDB")

        slot_value = tracker.get_slot("resource_type")
        slot_name = "Type"

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=slot_name,slot_value=slot_value)
        return_text = DbQueryingMethods.rows_info_as_text(get_query_results)
        dispatcher.utter_message(text=str(return_text))

        return 

class DbQueryingMethods:
    def create_connection(db_file):
        """ 
        create a database connection to the SQLite database
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

        return(rows)

    def rows_info_as_text(rows):
        """
        Return one of the rows (randomly selcted) passed in 
        as a human-readable text. If there are no rows, returns
        text to that effect.
        """
        if len(list(rows)) < 1:
            return "There are no resources matching your query."
        else:
            for row in random.sample(rows, 1):
                return f"Try the {(row[4]).lower()} {row[0]} by {row[1]}. You can find it at {row[2]}."