import re

PHONE_REGEX = r"\b\d{10}\b"
LINK_REGEX = r"(http|https|www)"

def is_restricted(text: str):
    if re.search(PHONE_REGEX, text):
        return "📵 Phone numbers are not allowed 🙏"
    if re.search(LINK_REGEX, text):
        return "🔗 Links are not allowed 🙏"
    return None


def generate_ai_reply(user_text, gender, mode, language):
    # very basic mock (replace with real AI later)
    base = {
        "tamil": "😊 epdi iruka?",
        "english": "😊 How are you?",
        "hindi": "😊 Aap kaise ho?",
        "telugu": "😊 Ela unnaru?",
        "tanglish": "😊 epdi iruka?"
    }

    reply = base.get(language, "😊 Hi!")

    if mode == "romantic":
        reply += " 💖 romba sweet-aa iruka"
    elif mode == "caring":
        reply += " 🤍 naan unna care pannuven"
    elif mode == "possessive":
        reply += " 😈 nee enakku mattum thaan"

    if gender == "male":
        reply += " da"
    elif gender == "female":
        reply += " di"

    return reply
