from keybert import KeyBERT

def extract_key_points(text, num_keywords=10):
    try:
        kw_model = KeyBERT()
        key_phrases = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num_keywords)
        return [phrase[0].capitalize() for phrase in key_phrases] if key_phrases else ["No key points found."]
    except Exception as e:
        return ["Error extracting key points."]
