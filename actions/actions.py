from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

class ActionSetLanguage(Action):

    def name(self) -> str:
        return "action_set_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        user_language = tracker.get_slot('user_language')
        
        if user_language == 'fr':
            return [SlotSet("language", "fr")]
        else:
            return [SlotSet("language", "en")]
        
class ActionDefaultFallback(Action):

    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        responses = ["utter_default", "utter_default2"]
        response = random.choice(responses)
        
        dispatcher.utter_message(template=response)
        
        return []

class ActionGreet(Action):
    def name(self) -> str:
        return "action_greet"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        user_language = tracker.get_slot('language')
        if user_language == 'fr':
            dispatcher.utter_message(text="Salut! Comment ça va?")
        else:
            dispatcher.utter_message(text="Hey! How are you?")
        return []
    
class ActionGoodbye(Action):
        def name(self) -> str:
            return "action_goodbye"
        
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: dict) -> list:    
            user_language = tracker.get_slot('language')    
            if user_language == 'fr':
                dispatcher.utter_message(text="Au revoir! A bientôt!")
            else:
                dispatcher.utter_message(text="Goodbye! See you soon!")
            return []