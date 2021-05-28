# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import collections

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3
import random
from fuzzywuzzy import process


# TODO: 
# - query more than one field/column at a time
# - if nothing matches both fields return results that match
#   at least one
# - data validation for close but not exact matches


# multifield query process:
# - first match each slot to closest item in that column
# actual complex queries
# - look for either, find union, 
# if none inform not perfect match

class QueryResourceType(Action):

    def name(self) -> Text:
        return "query_resource_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Runs a query using only the type column, fuzzy matching against the
        resource_type slot. Outputs an utterance to the user w/ the relevent 
        information for one of the returned rows.
        """
        conn = DbQueryingMethods.create_connection(db_file="./edu_db/resourcesDB")

        slot_value = tracker.get_slot("resource_type")
        slot_name = "Type"
        
        # adding fuzzy matching, fingers crossed
        slot_value = DbQueryingMethods.get_closest_value(conn=conn,
            slot_name=slot_name,slot_value=slot_value)[0]

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=slot_name,slot_value=slot_value)
        return_text = DbQueryingMethods.rows_info_as_text(get_query_results)
        dispatcher.utter_message(text=str(return_text))

        return 

class QueryResource(Action):

    def name(self) -> Text:
        return "query_resource"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        """
        Runs a query using both the topic & type columns (fuzzy matching against the
        relevent slots). Finds a match for both if possible, otherwise a match for the
        type only, topic only in that order. Output is an utterance directly to the
        user with a randomly selected matching row.
        """
        conn = DbQueryingMethods.create_connection(db_file="./edu_db/resourcesDB")

        # get matching entries for resource type
        resource_type_value = tracker.get_slot("resource_type")
        # make sure we don't pass None to our fuzzy matcher
        if resource_type_value == None:
            resource_type_value = " "
        resource_type_name = "Type"
        resource_type_value = DbQueryingMethods.get_closest_value(conn=conn,
            slot_name=resource_type_name,slot_value=resource_type_value)[0]
        query_results_type = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=resource_type_name,slot_value=resource_type_value)

        # get matching for resource topic
        resource_topic_value = tracker.get_slot("resource_topic")
        # make sure we don't pass None to our fuzzy matcher
        if resource_topic_value == None:
            resource_topic_value = " "
        resource_topic_name = "Topic"
        resource_topic_value = DbQueryingMethods.get_closest_value(conn=conn,    
            slot_name=resource_topic_name,slot_value=resource_topic_value)[0]
        query_results_topic = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=resource_topic_name,slot_value=resource_topic_value)

        # intersection of two queries
        topic_set = collections.Counter(query_results_topic)
        type_set =  collections.Counter(query_results_type)

        query_results_overlap = list((topic_set & type_set).elements())

        # apology for not having the right info
        apology = "I couldn't find exactly what you wanted, but you might like this."

        # return info for both, or topic match or type match or nothing
        if len(query_results_overlap)>0:
            return_text = DbQueryingMethods.rows_info_as_text(query_results_overlap)
        elif len(list(query_results_topic))>0:
            return_text = apology + DbQueryingMethods.rows_info_as_text(query_results_topic)
        elif len(list(query_results_type))>0:
            return_text = apology + DbQueryingMethods.rows_info_as_text(query_results_type)
        else:
            return_text = DbQueryingMethods.rows_info_as_text(query_results_overlap)
        
        # print results for user
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

    def get_closest_value(conn, slot_name, slot_value):
        """ Given a database column & text input, find the closest 
        match for the input in the column.
        """
        # get a list of all distinct values from our target column
        fuzzy_match_cur = conn.cursor()
        fuzzy_match_cur.execute(f"""SELECT DISTINCT {slot_name} 
                                FROM eduresources""")
        column_values = fuzzy_match_cur.fetchall()

        top_match = process.extractOne(slot_value, column_values)

        return(top_match[0])

    def select_by_slot(conn, slot_name, slot_value):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM eduresources
                    WHERE {slot_name}="{slot_value}"''')

        # return an array
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