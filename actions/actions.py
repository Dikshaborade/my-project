# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ActionFeedback(Action):

    def name(self) -> Text:
        return "action_ask_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Can you spare your valuable 2 minutes for providing feedback about your experience at our restaurant last night?")
        dispatcher.utter_message(buttons=[{"title":"YES","payload":"/affirm"},
                                        {"title":"NO","payload":"/deny"}]) 

        return []

class ActionThanks_1(Action):

    def name(self) -> Text:
        return "action_Thanks_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.slots.get('name')
        email = tracker.slots.get('email')
        phone = tracker.slots.get('phone')

        if tracker.slots.get("feedback")==True:
            dispatcher.utter_message(text="Thank you so much please answer following questions.")
        else:
            dispatcher.utter_message(text="Sorry to here that. Would like to here from you soon. Have a nice day.") 

        return []


class Validaterestaurantform(FormValidationAction):
    def name(self) -> Text:
        return "validate_restaurant_survey_form"

    # async def required_slots(
    #     self,
    #     domain_slots: List[Text],
    #     dispatcher: "CollectingDispatcher",
    #     tracker: "Tracker",
    #     domain: "DomainDict",
    # ) -> List[Text]:
    #     updated_slots = domain_slots.copy()
    #     a = tracker.slots.get("email") 
    #     if  a == 'skip':
    #         updated_slots.remove("phone")

    #     return updated_slots
    


    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        """Validate NAME"""

        if tracker.get_intent_of_latest_message() == "inform":
            return {'name': slot_value}
        else:
            dispatcher.utter_message(text="Sorry, I did not understand that. Please enter your name here:")
            return {'name': None}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        """Validate email"""

        if tracker.get_intent_of_latest_message() == "inform":
            email = tracker.slots.get('email')
            # Add optional regex verification here
            return {'email': slot_value}
        else:
            dispatcher.utter_message(text="Sorry, I did not understand that. Please enter your email here:")
            return {'email': None}

    def validate_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        """Validate phone"""

        if tracker.get_intent_of_latest_message() == "inform":
            phone = tracker.slots.get('phone')
            # Add optional regex verification here
            return {'phone': slot_value}
        else:
            dispatcher.utter_message(text="Sorry, I did not understand that. Please enter your phone here:")
            return {'phone': None}

    def validate_feedback(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        """Validate feedback"""

        if tracker.get_intent_of_latest_message() == "affirm":
            return {'feedback': True}
        else:
            return {'feedback': False}