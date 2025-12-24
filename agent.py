# agent.py - MAIN AGENT SYSTEM
from speech import TeluguVoice
from tools import Tool1_EligibilityChecker, Tool2_SchemeRecommender
from memory import ConversationMemory


class TeluguGovernmentAgent:
    """Main agent with state machine"""

    def __init__(self):
        # Initialize components
        self.voice = TeluguVoice()
        self.tool1 = Tool1_EligibilityChecker()
        self.tool2 = Tool2_SchemeRecommender()
        self.memory = ConversationMemory()

        # State machine
        self.state = "START"
        self.states = {
            "START": self.handle_start,
            "ASK_OCCUPATION": self.handle_ask_occupation,
            "ASK_AGE": self.handle_ask_age,
            "ASK_INCOME": self.handle_ask_income,
            "CHECK_ELIGIBILITY": self.handle_check_eligibility,
            "RECOMMEND": self.handle_recommend,
            "END": self.handle_end
        }

        # Telugu responses
        self.responses = {
            "greeting": "నమస్కారం! నేను ప్రభుత్వ పథకాల సహాయకుడిని. మీరు ఏ పథకం గురించి తెలుసుకోవాలనుకుంటున్నారు?",
            "ask_occupation": "మీ వృత్తి ఏమిటి? (రైతు, ఉద్యోగి, వ్యాపారి)",
            "ask_age": "మీ వయస్సు ఎంత?",
            "ask_income": "మీ వార్షిక ఆదాయం ఎంత?",
            "processing": "మీ సమాచారం తనిఖీ చేస్తున్నాను...",
            "contradiction": "క్షమించండి, మునుపు మీరు '{old}' అన్నారు, ఇప్పుడు '{new}' అంటున్నారు. ఏది నిజం?",
            "error": "దోషం జరిగింది. దయచేసి మళ్లీ ప్రయత్నించండి.",
            "thank_you": "ధన్యవాదాలు! మళ్లీ కలుద్దాం."
        }

        print("🤖 తెలుగు ప్రభుత్వ పథకాల ఏజెంట్ సిద్ధంగా ఉంది")

    def handle_start(self, user_input):
        """Handle START state"""
        self.voice.speak(self.responses["greeting"])
        self.state = "ASK_OCCUPATION"
        return self.responses["ask_occupation"]

    def handle_ask_occupation(self, user_input):
        """Handle occupation question"""
        # Store in memory
        self.memory.add_interaction(user_input, "Occupation asked", self.state)

        # Check for contradictions
        contradictions = self.memory.get_contradictions()
        if contradictions:
            for cont in contradictions:
                if cont["field"] == "occupation":
                    return self.responses["contradiction"].format(
                        old=cont["old"], new=cont["new"]
                    )

        self.state = "ASK_AGE"
        return self.responses["ask_age"]

    def handle_ask_age(self, user_input):
        """Handle age question"""
        self.memory.add_interaction(user_input, "Age asked", self.state)

        # Check contradictions
        contradictions = self.memory.get_contradictions()
        if contradictions:
            for cont in contradictions:
                if cont["field"] == "age":
                    return self.responses["contradiction"].format(
                        old=cont["old"], new=cont["new"]
                    )

        self.state = "ASK_INCOME"
        return self.responses["ask_income"]

    def handle_ask_income(self, user_input):
        """Handle income question"""
        self.memory.add_interaction(user_input, "Income asked", self.state)

        # Now we have all info, move to checking
        self.state = "CHECK_ELIGIBILITY"
        return self.responses["processing"]

    def handle_check_eligibility(self, user_input):
        """USE TOOL 1: Check eligibility"""
        user_profile = self.memory.get_user_profile()

        # TOOL 1 CALL
        eligible_schemes = self.tool1.check(user_profile)

        if eligible_schemes:
            self.eligible_schemes = eligible_schemes
            self.state = "RECOMMEND"
            return f"మీకు {len(eligible_schemes)} పథకాలు అర్హత ఉన్నాయి"
        else:
            self.state = "END"
            return "క్షమించండి, మీరు ఏ పథకానికీ అర్హులు కాదు."

    def handle_recommend(self, user_input):
        """USE TOOL 2: Recommend schemes"""
        user_profile = self.memory.get_user_profile()

        # TOOL 2 CALL
        recommendations = self.tool2.recommend(self.eligible_schemes, user_profile)

        # Build response
        response = "మీకు సిఫార్సు చేస్తున్న పథకాలు:\n\n"
        for i, rec in enumerate(recommendations, 1):
            scheme = rec["scheme"]
            response += f"{i}. {scheme['name']}\n"
            response += f"   లాభాలు: {scheme['benefits']}\n"
            response += f"   ప్రాధాన్యత: {rec['priority']}\n\n"

        self.state = "END"
        return response

    def handle_end(self, user_input):
        """Handle end of conversation"""
        return self.responses["thank_you"]

    def process(self, user_input):
        """Main processing function - STATE MACHINE"""
        if self.state in self.states:
            response = self.states[self.state](user_input)
            return response
        else:
            return self.responses["error"]

    def run_voice_conversation(self):
        """Run complete voice conversation"""
        print("\n" + "=" * 60)
        print("తెలుగు ప్రభుత్వ పథకాల ఏజెంట్")
        print("=" * 60)

        # Start with greeting
        response = self.handle_start("")
        self.voice.speak(response)

        conversation_active = True

        while conversation_active and self.state != "END":
            # Listen to user
            user_input = self.voice.listen()

            if not user_input:
                continue

            # Check for exit
            if any(word in user_input for word in ["ధన్యవాదాలు", "బై", "పూర్తి"]):
                self.voice.speak(self.responses["thank_you"])
                break

            # Process input
            response = self.process(user_input)

            # Speak response
            self.voice.speak(response)

        print("\n" + "=" * 60)
        print("సంభాషణ పూర్తయింది")
        print("=" * 60)

    def run_text_demo(self):
        """Demo with text input (for testing)"""
        print("\n" + "=" * 60)
        print("టెక్స్ట్ డెమో (మైక్రోఫోన్ లేకపోతే)")
        print("=" * 60)

        # Test conversation
        test_inputs = [
            "నమస్కారం",
            "నేను రైతుని",
            "నా వయస్సు 35 సంవత్సరాలు",
            "నా ఆదాయం 50000",
            "ధన్యవాదాలు"
        ]

        print("\n🔧 ఏజెంట్ ప్రారంభం...")
        response = self.handle_start("")
        print(f"🤖: {response}")

        for user_input in test_inputs:
            print(f"\n👤: {user_input}")

            if "ధన్యవాదాలు" in user_input:
                print("🤖: ధన్యవాదాలు!")
                break

            response = self.process(user_input)
            print(f"🤖: {response}")

            if self.state == "END":
                break


# Main function
def main():
    """Main function to run the agent"""
    try:
        agent = TeluguGovernmentAgent()

        # Ask user for mode
        print("\nమోడ్ ఎంచుకోండి:")
        print("1. వాయిస్ మోడ్ (మైక్రోఫోన్ అవసరం)")
        print("2. టెక్స్ట్ డెమో మోడ్")

        choice = input("ఎంపిక (1 లేదా 2): ")

        if choice == "1":
            agent.run_voice_conversation()
        else:
            agent.run_text_demo()

    except Exception as e:
        print(f"❌ దోషం: {e}")
        print("టెక్స్ట్ డెమో తో ప్రారంభిస్తున్నాను...")
        agent = TeluguGovernmentAgent()
        agent.run_text_demo()


if __name__ == "__main__":
    main()