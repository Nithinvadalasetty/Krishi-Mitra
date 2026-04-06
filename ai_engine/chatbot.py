from ai_engine.disease_advisor import get_advice_and_remedy

def chatbot_reply(message, disease=None):
    msg = message.lower()

    if "remedy" in msg and disease:
        return get_advice_and_remedy(disease)["remedy"]

    if "advice" in msg and disease:
        return get_advice_and_remedy(disease)["advice"]

    return "You can ask me about disease advice or remedies."
