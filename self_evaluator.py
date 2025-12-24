# self_evaluator.py
class SelfEvaluator:
    """Evaluates own performance and recovers from failures"""

    def assess_goal_progress(self, conversation_history):
        """Assess if conversation is progressing toward goal"""
        # Simple logic: Check if we collected info and used tools

        info_collected = False
        tool_used = False

        for entry in conversation_history:
            text = entry.get('user', '')

            # Check if info collected
            if any(word in text for word in ['వయస్సు', 'ఆదాయం', 'వృత్తి', 'age', 'income', 'occupation']):
                info_collected = True

            # Check if agent mentioned tools
            agent_text = entry.get('agent', '')
            if any(word in agent_text for word in ['అర్హత', 'సిఫార్సు', 'eligibility', 'recommend']):
                tool_used = True

        if info_collected and tool_used:
            return 1.0  # 100% progress
        elif info_collected:
            return 0.5  # 50% progress
        else:
            return 0.1  # 10% progress
    def evaluate_conversation(self, conversation_history):
        """Evaluate if conversation is progressing toward goal"""

        # Check for stuck patterns
        if self.is_stuck(conversation_history):
            return {
                'issue': 'సంభాషణ స్తంభించింది',
                'action': 'change_approach',
                'new_approach': 'ప్రత్యక్ష ప్రశ్న అడగండి'
            }

        # Check for contradictions
        contradictions = self.find_contradictions(conversation_history)
        if contradictions:
            return {
                'issue': 'విరోధాభాసాలు కనుగొనబడ్డాయి',
                'action': 'clarify_contradictions',
                'contradictions': contradictions
            }

        # Check if goal is being achieved
        goal_progress = self.assess_goal_progress(conversation_history)
        if goal_progress < 0.3:
            return {
                'issue': 'లక్ష్యం దిశలో పురోగతి లేదు',
                'action': 'reassess_goal',
                'suggestion': 'లక్ష్యం మళ్లీ నిర్వచించండి'
            }

        return {'status': 'progressing_well'}

    def is_stuck(self, history):
        """Check if conversation is stuck in loops"""
        if len(history) < 3:
            return False

        last_three = [h.get('agent', '') for h in history[-3:]]
        # Check if agent is repeating same questions
        return len(set(last_three)) == 1

    def find_contradictions(self, history):
        """Find contradictions in user information"""
        contradictions = []
        age_mentions = []
        income_mentions = []

        for entry in history:
            text = entry.get('user', '')
            # Extract ages
            import re
            ages = re.findall(r'(\d+)\s*(సంవత్సరాలు|వయస్సు)', text)
            if ages:
                age_mentions.append(int(ages[0][0]))

            # Extract income
            incomes = re.findall(r'(\d+)\s*(లక్ష|వేలు|ఆదాయం)', text)
            if incomes:
                income_mentions.append(incomes[0][0])

        if len(set(age_mentions)) > 1:
            contradictions.append(f"వయస్సు: {set(age_mentions)}")

        return contradictions