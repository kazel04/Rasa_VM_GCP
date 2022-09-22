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
        if (tracker.slots.get("review") is True) & (tracker.slots.get("start_questionnaire") is True): #when actions files have been changed, restart action server! Otherwise will load outdated action slots paths
            updated_slots.append("readcheck2") #used readcheck2 instead of drive ^is for GOOD VA, good vision
            updated_slots.append("cookcheck")
            updated_slots.append("walkcheck")
            updated_slots.append("moneycheck")
            updated_slots.append("cleancheck")
            updated_slots.append("drivecheck")
            if tracker.slots.get("readcheck2") is True:
                updated_slots.append("read_ability")
            elif tracker.slots.get("cookcheck") is True:
                updated_slots.append("cook_ability") 
            elif tracker.slots.get("walkcheck") is True:
                updated_slots.append("walk_ability")
            elif tracker.slots.get("moneycheck") is True:
                updated_slots.append("money_ability")
            elif tracker.slots.get("cleancheck") is True:
             updated_slots.append("clean_ability")
            if tracker.slots.get("drivecheck") is True: #the format is breaking my heart but it works comapared to elif
                updated_slots.append("drive_ability")
                updated_slots.append("goodend")
            elif tracker.slots.get("drivecheck") is False: #button test checks out
                updated_slots.append("goodend")
        elif (tracker.slots.get("review") is False) & (tracker.slots.get("start_questionnaire") is True): #if negative and positive intent
            updated_slots.append("symptomtype")
            if tracker.slots.get("symptomtype") is True: #BOV
                updated_slots.append("acutevschronic") #acute vs chronic
                if tracker.slots.get("acutevschronic") is True: #acute
                    updated_slots.append("unknownend")
                if tracker.slots.get("acutevschronic") is False: #chronic
                    updated_slots.append("eye_check") #works now
                    updated_slots.append("dropvsslow") #this is for sudden drop or dk vs slowly affecting
                    if tracker.slots.get("dropvsslow") is True:
                        updated_slots.append("unknownend")
                    elif tracker.slots.get("dropvsslow") is False:
                        updated_slots.append("intermittentvsalways") #check if this works without validation
                        updated_slots.append("readcheck") # just used normal readcheck
                        updated_slots.append("cookcheck")
                        updated_slots.append("walkcheck")
                        updated_slots.append("moneycheck")
                        updated_slots.append("cleancheck")
                        updated_slots.append("drivecheck")
                        updated_slots.append("goodend")
                        if tracker.slots.get("drivecheck") is True:
                            updated_slots.remove("goodend")
                            updated_slots.append("driveend") # driving affected end
                        elif (tracker.slots.get("readcheck") is True) or (tracker.slots.get("walkcheck") is True) or (tracker.slots.get("moneycheck") is True) or (tracker.slots.get("cleancheck") is True):
                            updated_slots.remove("goodend")
                            updated_slots.append("activityend") # other activities affected end
            elif tracker.slots.get("symptomtype") is False: #Non-BOV
                updated_slots.append("unknownend")
        elif (tracker.slots.get("review") is True) & (tracker.slots.get("start_questionnaire") is False): # start of all nega VA, this is for good intent but bad VA
            updated_slots.append("surroundingstest")#surroundings test start
            updated_slots.append("drove_previously") # this is asking if they currently drive!
            if tracker.slots.get("drove_previously") is True: #driving tree start
                updated_slots.append("vocational_driving")
            elif tracker.slots.get("drove_previously") is False:
                updated_slots.append("difficulty_driving_because_vision")
            if (tracker.slots.get("vocational_driving") is True) or (tracker.slots.get("vocational_driving") is False) or (tracker.slots.get("difficulty_driving_because_vision") is True) or (tracker.slots.get("difficulty_driving_because_vision") is False): #vocational or personal driving and whether or not stopped cos of vision, link to 6 activity qn check
                updated_slots.append("readcheck2") 
                updated_slots.append("cookcheck")
                updated_slots.append("walkcheck")
                updated_slots.append("moneycheck")
                updated_slots.append("cleancheck")
                updated_slots.append("drivecheck") # if one is triggered, immediately 
                updated_slots.append("goodend") #tentative ending!!!
            if (tracker.slots.get("readcheck2") is True) or (tracker.slots.get("walkcheck") is True) or (tracker.slots.get("moneycheck") is True) or (tracker.slots.get("cleancheck") is True) or (tracker.slots.get("cleancheck") is True):
                updated_slots.remove("goodend")
                updated_slots.append("cataractsurgery") # cataracts surgery qn slot 
                updated_slots.append("cataractseedocend") #directly added (for personal driving or not driving)
        if (tracker.slots.get("cataractsurgery") is False) & (tracker.slots.get("vocational_driving") is True):
            updated_slots.remove("cataractseedocend")
            updated_slots.append("glassesdriving")
            if tracker.slots.get("glassesdriving") is True: 
                updated_slots.append("glassestest")
                if tracker.slots.get("glassestest") is True: 
                    updated_slots.append("cataractseedocend")
                elif tracker.slots.get("glassestest") is False: 
                        updated_slots.append("retestend")
            elif tracker.slots.get("glassesdriving") is False: 
                updated_slots.append("cataractseedocend")
        elif (tracker.slots.get("review") is False) & (tracker.slots.get("start_questionnaire") is False): #negative VA, negative intent
            updated_slots.append("symptomtype")
            if tracker.slots.get("symptomtype") is True: #BOV
                updated_slots.append("acutevschronic") #acute vs chronic
                if tracker.slots.get("acutevschronic") is True: #acute
                    updated_slots.append("unknownend")
                if tracker.slots.get("acutevschronic") is False: #chronic
                    updated_slots.append("eye_check") #works now
                    updated_slots.append("dropvsslow") #this is for sudden drop or dk vs slowly affecting
                    if tracker.slots.get("dropvsslow") is True: #only thing that is diff from positive VA nega intent
                        updated_slots.append("drove_previously") # this is asking if they currently drive!
            if tracker.slots.get("drove_previously") is True: #driving tree start (same as prev driving tree!)
                updated_slots.append("vocational_driving")
            elif tracker.slots.get("drove_previously") is False:
                updated_slots.append("difficulty_driving_because_vision")
            if (tracker.slots.get("vocational_driving") is True) or (tracker.slots.get("vocational_driving") is False) or (tracker.slots.get("difficulty_driving_because_vision") is True) or (tracker.slots.get("difficulty_driving_because_vision") is False): #vocational or personal driving and whether or not stopped cos of vision, link to 6 activity qn check
                updated_slots.append("readcheck2") 
                updated_slots.append("cookcheck")
                updated_slots.append("walkcheck")
                updated_slots.append("moneycheck")
                updated_slots.append("cleancheck")
                updated_slots.append("drivecheck") # if one is triggered, immediately 
                updated_slots.append("goodend") #tentative ending!!!
            if (tracker.slots.get("readcheck2") is True) or (tracker.slots.get("walkcheck") is True) or (tracker.slots.get("moneycheck") is True) or (tracker.slots.get("cleancheck") is True) or (tracker.slots.get("cleancheck") is True):
                updated_slots.remove("goodend")
                updated_slots.append("cataractsurgery") # cataracts surgery qn slot 
                updated_slots.append("cataractseedocend") #directly added
        if (tracker.slots.get("cataractsurgery") is False) & (tracker.slots.get("vocational_driving") is True):
            updated_slots.remove("cataractseedocend")
            updated_slots.append("glassesdriving")
            if tracker.slots.get("glassesdriving") is True: 
                updated_slots.append("glassestest")
                if tracker.slots.get("glassestest") is True: 
                    updated_slots.append("cataractseedocend")
                elif tracker.slots.get("glassestest") is False: 
                        updated_slots.append("retestend")
            elif tracker.slots.get("glassesdriving") is False: 
                updated_slots.append("cataractseedocend")


            

        return updated_slots

        # if tracker.slots.get("review") is True:
        #     # If the user is an existing customer,
        #     # do not request the `email_address` slot
        #     return updated_slots
        # else:
        #     updated_slots.append("drive")
        #     updated_slots.append("vocational_driving")
        #     updated_slots.append("driving_lorry_van_truck")
        #     updated_slots.append("difficulty_driving_because_vision")
        #     updated_slots.append("drove_previously")
        #     updated_slots.append("stop_less_than_month_ago")
        #     updated_slots.append("stopped_driving_because_of_eyesight")
        #     updated_slots.append("difficulty_with_daily_activities")
        #     updated_slots.append("difficulty_reading_with_glasses")
        #     updated_slots.append("things_you_enjoy")
        #     updated_slots.append("eyesight_affecting_your_mentioned_activity")
        #     return updated_slots
        # if tracker.slots.get("drive") is True:
        #     updated_slots.remove("drove_previously")
        #     updated_slots.remove("stop_less_than_month_ago")
        #     updated_slots.remove("stopped_driving_because_of_eyesight")
        # elif tracker.slots.get("drive") is False:
        #     updated_slots.remove("vocational_driving")
        #     updated_slots.remove("driving_lorry_van_truck")
        #     updated_slots.remove("difficulty_driving_because_vision")


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
            "diabetes": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "review": [
                self.from_intent(intent="goodvision", value=True), #use buttons to directly set to payloads that are in those intents 
                self.from_intent(intent="negativevision", value=False),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "readcheck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "cookcheck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "walkcheck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "moneycheck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
           "cleancheck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
           "drivecheck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "readcheck2": [
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
            "eye_check": [
                self.from_text(),
            ],
            "read_ability": [
                self.from_text(),
            ],
            "cook_ability": [
                self.from_text(),
            ],
            "walk_ability": [
                self.from_text(),
            ],
           "money_ability": [
                self.from_text(),
            ],
            "drive_ability": [
                self.from_text(),
            ],
            "goodend": [
                self.from_text(),
            ],
            "unknownend": [
                self.from_text(),
            ],
            "activityend": [
                self.from_text(),
            ],
            "retestend": [
                self.from_text(),
            ],
            "symptomtype": [
                self.from_intent(intent="blurredvision", value=True), #use buttons to directly set True, fals and other terminal values
                self.from_intent(intent="othersymptoms", value=False),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "acutevschronic": [
                self.from_intent(intent="acute", value=True), #use buttons to directly set True, fals and other terminal values
                self.from_intent(intent="chronic", value=False),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "dropvsslow": [
                self.from_intent(intent="suddendropdk", value=True), #use buttons to directly set True, fals and other terminal values
                self.from_intent(intent="slowaffect", value=False),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "intermittentvsalways": [
                self.from_intent(intent="intermittent", value=True), #use buttons to directly set True, fals and other terminal values
                self.from_intent(intent="always", value=False),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "intermittentreadcheck": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "surroundingstest": [
                self.from_intent(intent="bothsurroundingsok", value=True), #use buttons to directly set True, fals and other terminal values
                self.from_intent(intent="surroundingsbad", value=False),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "drive": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "cataractsurgery": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "cataractseedocend": [
                self.from_text(),
            ],
            "glassesdriving": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "glassestest": [
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
    def validate_readcheck(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"readcheck": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"readcheck": False}
    def validate_cookcheck(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"cookcheck": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"cookcheck": False}
    def validate_readcheck2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"readcheck2": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"readcheck2": False}
    def validate_walkcheck(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"walkcheck": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"walkcheck": False}
    def validate_moneycheck(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"moneycheck": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"moneycheck": False}
    def validate_cleancheck(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"cleancheck": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"cleancheck": False}
    def validate_drivecheck(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"drivecheck": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"drivecheck": False}
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
    def validate_symptomtype(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"symptomtype": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"symptomtype": False}
    def validate_acutevschronic(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"acutevschronic": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"acutevschronic": False}
    def validate_dropvsslow(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Yes":
            return {"dropvsslow": True}
        else:
            # dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"dropvsslow": False}

