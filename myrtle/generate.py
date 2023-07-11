from gpt4all import GPT4All


def generate():
    model = GPT4All("model.bin", "/.cache/gpt4all/")
    output = model.generate("Happiness is", max_tokens=10)
    return output
