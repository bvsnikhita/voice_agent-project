# autonomous_planner.py
class AutonomousPlanner:
    """Makes autonomous decisions about next actions"""

    def decide_next_action(self, context):
        """Autonomously decide what to do next"""

        # Decision logic
        if not context.get('user_profile'):
            return {
                'action': 'collect_information',
                'reason': 'యూజర్ ప్రొఫైల్ లేదు',
                'priority': 'high'
            }

        elif context.get('user_profile') and not context.get('eligibility_checked'):
            return {
                'action': 'check_eligibility',
                'reason': 'అర్హత తనిఖీ అవసరం',
                'tool': 'eligibility_checker',
                'priority': 'high'
            }

        elif context.get('eligible_schemes') and not context.get('recommendations_given'):
            return {
                'action': 'recommend_schemes',
                'reason': 'పథకాలు సిఫార్సు చేయాలి',
                'tool': 'scheme_recommender',
                'priority': 'medium'
            }

        else:
            return {
                'action': 'ask_for_next_step',
                'reason': 'తదుపరి చర్య గురించి అడగాలి',
                'priority': 'low'
            }