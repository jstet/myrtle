from profanity_check import predict_prob
from myrtle.console import console

# making sure gpt2 does not return anything antisemitic
# i also dont want it to generate religious texts
# multiple quotes he model was trained on are from harry potter or hunger games
dont_include = ["jew", "jews", "god", "jesus", "christian", "harry", "Katniss"]


def get_random_inpt(df):
    row = df.sample().iloc[0]
    inpt = row["quote"]
    inpt = inpt.split()[0:2]
    return " ".join(inpt)


def generate(generator, df) -> str:
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        inpt = get_random_inpt(df)
        generated_text = generator(inpt)[0]["generated_text"]
        proc_text = generated_text.lower()
        offensiveness_score = predict_prob([generated_text])[0]
        if (
            offensiveness_score < 0.5
            and all(word not in proc_text for word in dont_include)
            and not any(char.isdigit() for char in proc_text)
        ):
            return generated_text
        else:
            console.log(generated_text)
        attempts += 1
    return "Myrtle wanted to say something inappropriate."
