from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
from profanity_check import predict_prob


def generate(model, inpt) -> str:
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(model)
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=60,
        no_repeat_ngram_size=3,
        repetition_penalty=1.2,
        eos_token_id=int(tokenizer.convert_tokens_to_ids(".")),
        top_p=0.9,
        temperature=0.5,
        top_k=50,
    )
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        generated_text = generator(inpt)[0]["generated_text"]
        offensiveness_score = predict_prob([generated_text])[0]
        if offensiveness_score < 0.5:  # Adjust the threshold as needed
            return generated_text
        attempts += 1
    return "Unable to generate non-offensive text within the given attempt limit"
