from typing import Any, Text, Dict, List, Union
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import FormValidationAction, Tracker

class ValidateSimpleEyeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_eye_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("review") is True & tracker.slots.get("VANumber") is False:
            # If no problem reported but worse VA score
            updated_slots.append("surroundings")
            updated_slots.append("difficulty_with_daily_activities")
            updated_slots.append("difficulty_reading_with_glasses")
            updated_slots.append("things_you_enjoy")
            updated_slots.append("eyesight_affecting_your_mentioned_activity")
            updated_slots.append("drive")
            updated_slots.append("vocational_driving")
            updated_slots.append("driving_lorry_van_truck")
            updated_slots.append("difficulty_driving_because_vision")
            updated_slots.append("drove_previously")
            updated_slots.append("stop_less_than_month_ago")
            updated_slots.append("stopped_driving_because_of_eyesight")

            return updated_slots    
        else:
            updated_slots.append("drive")
            updated_slots.append("vocational_driving")
            updated_slots.append("driving_lorry_van_truck")
            updated_slots.append("difficulty_driving_because_vision")
            updated_slots.append("drove_previously")
            updated_slots.append("stop_less_than_month_ago")
            updated_slots.append("stopped_driving_because_of_eyesight")
            updated_slots.append("difficulty_with_daily_activities")
            updated_slots.append("difficulty_reading_with_glasses")
            updated_slots.append("things_you_enjoy")
            updated_slots.append("eyesight_affecting_your_mentioned_activity")
            return updated_slots
        if tracker.slots.get("drive") is True:
            updated_slots.remove("drove_previously")
            updated_slots.remove("stop_less_than_month_ago")
            updated_slots.remove("stopped_driving_because_of_eyesight")
        elif tracker.slots.get("drive") is False:
            updated_slots.remove("vocational_driving")
            updated_slots.remove("driving_lorry_van_truck")
            updated_slots.remove("difficulty_driving_because_vision")


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "start_questionnaire": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),

            ],
            "age": [
                self.from_entity(entity="numbers"),
                self.from_text()
            ],
            #need to add mapping for VAnumber!
            "VANumber": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "review": [
                self.from_intent(intent="mood_great", value=True), #changed the intents from affirm and deny to positive and negative intents instead
                self.from_intent(intent="mood_unhappy", value=False),
            ],
            "drive": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "vocational_driving": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "driving_lorry_van_truck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "difficulty_driving_because_vision": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "drove_previously": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],

            "stop_less_than_month_ago": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "stopped_driving_because_of_eyesight": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "difficulty_with_daily_activities": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "difficulty_reading_with_glasses": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "eyesight_affecting_your_mentioned_activity": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],

        }
    def validate_start_questionnaire(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"start_questionnaire": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"start_questionnaire": False}
    def validate_diabetes(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"diabetes": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"diabetes": False}
    def validate_review(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"review": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"review": False}
    def validate_drive(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"drive": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"drive": False}
    def validate_vocational_driving(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"vocational_driving": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"vocational_driving": False}
    def validate_driving_lorry_van_truck(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"driving_lorry_van_truck": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"driving_lorry_van_truck": False}
    def validate_difficulty_driving_because_vision(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"difficulty_driving_because_vision": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"difficulty_driving_because_vision": False}
    def validate_drove_previously(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"drove_previously": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"drove_previously": False}
    def validate_stop_less_than_month_ago(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"stop_less_than_month_ago": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"stop_less_than_month_ago": False}
    def validate_stopped_driving_because_of_eyesight(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"stopped_driving_because_of_eyesight": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"stopped_driving_because_of_eyesight": False}

    def validate_difficulty_with_daily_activities(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"difficulty_with_daily_activities": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"difficulty_with_daily_activities": False}

    def validate_difficulty_reading_with_glasses(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"difficulty_reading_with_glasses": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"difficulty_reading_with_glasses": False}
    def validate_eyesight_affecting_your_mentioned_activity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"eyesight_affecting_your_mentioned_activity": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"eyesight_affecting_your_mentioned_activity": False}

