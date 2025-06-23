from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    word_count = len(text.split())

    if word_count < 50:
        num_sentences = 2
    elif word_count < 150:
        num_sentences = 3
    elif word_count < 300:
        num_sentences = 5
    else:
        num_sentences = 6

    summary_sentences = summarizer(parser.document, num_sentences)

    polished_summary = []
    for sentence in summary_sentences:
        sentence = str(sentence).strip()
        if sentence and not sentence.endswith('.'):
            sentence += '.'
        polished_summary.append(sentence.capitalize())

    return " ".join(polished_summary)
