import re

def extract_action_items(text):
    action_items = []
    sentences = re.split(r'(?<=[.?!])\s+', text)

    action_indicators = [
        "must", "should", "need to", "required to", "have to", "ensure",
        "we need to", "we plan to", "we expect", "our goal is", "it is essential", 
        "it is necessary", "the next step is", "going to", "aim to", "intend to"
    ]

    for sentence in sentences:
        lower_sentence = sentence.lower()
        if any(indicator in lower_sentence for indicator in action_indicators):
            action_items.append(sentence.strip())

    return action_items if action_items else ["No specific action items identified."]
