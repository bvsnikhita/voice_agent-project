# tools.py - Two Required Tools
import json


class Tool1_EligibilityChecker:
    """TOOL 1: Check eligibility for schemes"""

    def __init__(self):
        self.schemes = self.load_schemes()
        print("🔧 టూల్ 1: అర్హత తనిఖీదారు సిద్ధంగా ఉంది")

    def load_schemes(self):
        """Load Telugu government schemes"""
        return [
            {
                "id": "pm_kisan",
                "name": "PM కిసాన్ సమ్మాన్ నిధి",
                "min_age": 18,
                "max_income": 100000,
                "occupation": "రైతు",
                "benefits": "సంవత్సరానికి ₹6000"
            },
            {
                "id": "pm_awas",
                "name": "ప్రధానమంత్రి ఆవాస్ యోజన",
                "min_age": 21,
                "max_income": 300000,
                "occupation": "any",
                "benefits": "గృహలోన్ సబ్సిడీ"
            },
            {
                "id": "ayushman",
                "name": "ఆయుష్మాన్ భారత్",
                "min_age": 21,
                "max_income": 500000,
                "occupation": "any",
                "benefits": "₹5 లక్షల ఆరోగ్య బీమా"
            }
        ]

    def check(self, user_profile):
        """Check which schemes user is eligible for"""
        eligible = []

        for scheme in self.schemes:
            if self.is_eligible(scheme, user_profile):
                eligible.append(scheme)

        print(f"✅ {len(eligible)} పథకాలు అర్హత ఉన్నాయి")
        return eligible

    def is_eligible(self, scheme, user_profile):
        """Check eligibility for one scheme"""
        # Age check
        if "min_age" in scheme:
            if user_profile.get("age", 0) < scheme["min_age"]:
                return False

        # Income check
        if "max_income" in scheme:
            if user_profile.get("income", 0) > scheme["max_income"]:
                return False

        # Occupation check
        if scheme["occupation"] != "any":
            if user_profile.get("occupation") != scheme["occupation"]:
                return False

        return True


class Tool2_SchemeRecommender:
    """TOOL 2: Recommend best schemes"""

    def __init__(self):
        print("🔧 టూల్ 2: పథకాలు సిఫార్సుదారు సిద్ధంగా ఉంది")

    def recommend(self, eligible_schemes, user_profile):
        """Recommend top 3 schemes"""
        recommendations = []

        for scheme in eligible_schemes:
            score = 0

            # Priority for farmers for PM Kisan
            if scheme["id"] == "pm_kisan" and user_profile.get("occupation") == "రైతు":
                score += 10

            # Priority for low income
            if user_profile.get("income", 0) < 50000:
                score += 5

            # Priority for specific age groups
            age = user_profile.get("age", 0)
            if age > 60 and scheme["id"] == "pm_awas":
                score += 3

            recommendations.append({
                "scheme": scheme,
                "score": score,
                "priority": self.get_priority(score)
            })

        # Sort by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)

        print(f"📊 {len(recommendations)} సిఫార్సులు")
        return recommendations[:3]  # Top 3

    def get_priority(self, score):
        """Get priority level in Telugu"""
        if score >= 10:
            return "అత్యధిక ప్రాధాన్యత"
        elif score >= 5:
            return "మధ్యస్థ ప్రాధాన్యత"
        else:
            return "సాధారణ ప్రాధాన్యత"


# Test
if __name__ == "__main__":
    checker = Tool1_EligibilityChecker()
    recommender = Tool2_SchemeRecommender()

    test_profile = {"age": 35, "income": 50000, "occupation": "రైతు"}

    eligible = checker.check(test_profile)
    if eligible:
        recommendations = recommender.recommend(eligible, test_profile)
        print(f"సిఫార్సులు: {recommendations}")