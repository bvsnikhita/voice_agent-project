Telugu Government Scheme Voice Assistant
A voice-based AI system that helps Telugu-speaking citizens find eligible government schemes through natural conversation.

 Features
Telugu Voice Interface - Speak naturally, get spoken responses

Smart Eligibility Check - Matches your profile with few government schemes

Personalized Recommendations - Suggests schemes based on your occupation, age, and income

Conversation Memory - Remembers your details and previous interactions

State Machine Logic - Intelligent, step-by-step guidance

How It Works
Example Conversation:
text
Agent: నమస్కారం! మీరు ఏ పథకం గురించి తెలుసుకోవాలనుకుంటున్నారు?
You: నేను రైతుని
Agent: మీ వయస్సు ఎంత?
You: 45 ఏళ్ళు  
Agent: మీ వార్షిక ఆదాయం ఎంత?
You: 3 లక్షలు
Agent: మీకు 3 పథకాలు అర్హత ఉన్నాయి: PM Kisan, Ayushman Bhava,...

 Architecture
Core Modules:
agent.py - Main state machine and conversation logic

speech.py - Telugu voice recognition and synthesis

tools.py - Eligibility checking and recommendations

memory.py - User profile and conversation history

State Flow:
text
START → ASK_OCCUPATION → ASK_AGE → ASK_INCOME → CHECK_ELIGIBILITY → RECOMMEND → END

 Technical Highlights
Modular Design - Each component is independent and testable

Error Handling - Graceful handling of unclear inputs and contradictions

Scalable - Easy to add new schemes or modify logic

Offline Capable - Minimal external dependencies

📁 Project Structure
text
telugu-voice-agent/
├── agent.py              # Main agent with state machine

├── speech.py             # Voice processing

├── tools.py              # Scheme checking & recommendations

├── memory.py             # Conversation history

|__planner.py

└── README.md

Target Users
Farmers looking for agricultural schemes

Students seeking scholarships

Business Owners exploring loan programs

Senior Citizens checking pension benefits

Anyone preferring voice over text input

 Supported Schemes
PM Kisan Samman Nidhi - Farmer income support

Ayushman Bhava - Health insurance

pradhana manthri aawas yojhana

 Contributing
Fork the repository

Add new schemes to tools.py

Improve voice recognition in speech.py

Submit a pull request

