# memory.py - Conversation Memory System
from datetime import datetime


class ConversationMemory:
    """Memory system for storing conversation"""

    def __init__(self):
        self.history = []
        self.user_facts = {}
        self.contradictions = []
        print("💾 కన్వర్సేషన్ మెమరీ సిస్టమ్ సిద్ధంగా ఉంది")

    def add_interaction(self, user_input, agent_response, state):
        """Add interaction to memory"""
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user": user_input,
            "agent": agent_response,
            "state": state
        }
        self.history.append(entry)

        # Extract facts from user input
        self.extract_facts(user_input)

        print(f"💾 మెమరీలో సేవ్ చేయబడింది: {len(self.history)} ఇంటరాక్షన్లు")

    def extract_facts(self, text):
        """Extract facts from Telugu text"""
        import re

        # Extract age
        age_match = re.search(r'(\d+)\s*(సంవత్సరాలు|వయస్సు|యేర్స్)', text)
        if age_match:
            age = int(age_match.group(1))
            self.store_fact("age", age)

        # Extract income
        income_match = re.search(r'(\d+)\s*(లక్ష|వేలు|ఆదాయం)', text)
        if income_match:
            num = int(income_match.group(1))
            unit = income_match.group(2)
            if 'లక్ష' in unit:
                income = num * 100000
            else:
                income = num * 1000
            self.store_fact("income", income)

        # Extract occupation
        occupations = ['రైతు', 'ఉద్యోగి', 'విద్యార్థి', 'వ్యాపారం']
        for occ in occupations:
            if occ in text:
                self.store_fact("occupation", occ)
                break

    def store_fact(self, key, value):
        """Store fact with contradiction check"""
        if key in self.user_facts:
            old_value = self.user_facts[key]
            if old_value != value:
                # CONTRADICTION DETECTED!
                self.contradictions.append({
                    "field": key,
                    "old": old_value,
                    "new": value,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                print(f"⚠️ విరోధాభాసం కనుగొనబడింది: {key} = {old_value} → {value}")

        self.user_facts[key] = value

    def get_contradictions(self):
        """Get all contradictions"""
        return self.contradictions

    def get_user_profile(self):
        """Get user profile from facts"""
        return self.user_facts.copy()

    def get_history(self, last_n=5):
        """Get last n interactions"""
        return self.history[-last_n:] if self.history else []

    def clear(self):
        """Clear memory"""
        self.history = []
        self.user_facts = {}
        self.contradictions = []
        print("🧹 మెమరీ క్లియర్ చేయబడింది")


# Test
if __name__ == "__main__":
    memory = ConversationMemory()
    memory.add_interaction("నా వయస్సు 30 సంవత్సరాలు", "సరే", "ASK_AGE")
    memory.add_interaction("నా ఆదాయం 2 లక్షలు", "సరే", "ASK_INCOME")
    print(f"యూజర్ ప్రొఫైల్: {memory.get_user_profile()}")