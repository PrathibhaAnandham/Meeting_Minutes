from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load T5-small model and tokenizer once
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

def summarize_text(text, max_length=150, min_length=30):
    # Prepare the input
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate summary
    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decode and return summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
