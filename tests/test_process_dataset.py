from myrtle.training import process_dataset
from transformers import AutoTokenizer


def test_process_dataset():
    # Test case 1: Test with a valid CSV path and tokenizer
    csv_path = "./data/processed/processed_quotes.csv"
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    result = process_dataset(csv_path, tokenizer)
    print(result["train"])
    print(result["train"][0])
