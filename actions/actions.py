from rasa_sdk import Action, Tracker # type: ignore
from rasa_sdk.executor import CollectingDispatcher # type: ignore
from rasa_sdk.events import SlotSet # type: ignore
from rasa.shared.nlu.training_data.loading import load_data # type: ignore
from rasa.shared.nlu.training_data.training_data import TrainingData # type: ignore
from preprocess import find_most_similar_intent, detect_language
import random

class ActionSetLanguage(Action):

    def name(self) -> str:
        return "action_set_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        user_language = tracker.get_slot('user_language')
        
        if user_language == 'fr':
            dispatcher.utter_message(text="La langue a été définie sur le français.")
            return [SlotSet("language", "fr")]
        else:
            dispatcher.utter_message(text="The language has been set to English.")
            return [SlotSet("language", "en")]
        
class ActionFindMostSimilarIntent(Action):

    def name(self) -> str:
        return "action_find_most_similar_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        input_text = tracker.latest_message.get('text')
        lang = detect_language(input_text)

        #test
        print(f"Detected language: {lang}")
        dispatcher.utter_message(text=f"Detected language: {lang}")

        nlu_data_paths = {
            "en": "data/nlu_en.yml",
            "fr": "data/nlu_fr.yml"
        }
        training_data = load_data(nlu_data_paths[lang])
        most_similar_intent, similarity = find_most_similar_intent(input_text, training_data, lang)
        similarity_threshold = 0.75
        if similarity >= similarity_threshold:
            if lang == 'fr':
                dispatcher.utter_message(text=f"Intent le plus similaire: {most_similar_intent} avec une similarité de {similarity}")
            else:
                dispatcher.utter_message(text=f"Most similar intent: {most_similar_intent} with similarity {similarity}")
        else:
            fallback_action = ActionDefaultFallback()
            return fallback_action.run(dispatcher, tracker, domain)
    
        return []

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