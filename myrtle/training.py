from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
)
from myrtle.console import console
import random
import math


def group_texts(quotes):
    """
    Group texts in blocks of block_size characters.

    Args:
        quotes (dict): A dictionary containing texts to be grouped.

    Returns:
        dict: A dictionary where texts are grouped into blocks of block_size characters,
            with the 'labels' key set to the same value as the 'input_ids' key.
    """
    block_size = 128

    concatenated = {k: sum(quotes[k], []) for k in quotes.keys()}

    total_length = len(concatenated[list(quotes.keys())[0]])

    if total_length >= block_size:
        total_length = (total_length // block_size) * block_size

    result = {k: [t[i : i + block_size] for i in range(0, total_length, block_size)] for k, t in concatenated.items()}

    result["labels"] = result["input_ids"].copy()

    return result


def process_dataset(csv_path, tokenizer):
    """
    Processes a dataset by loading it from a CSV file, splitting it into train and test sets, tokenizing the data using
    a tokenizer, and grouping the tokenized texts.

    Parameters:
    - csv_path (str): The path to the CSV file containing the dataset.
    - tokenizer (Tokenizer): The tokenizer to be used for tokenizing the data.

    Returns:
    - lm_dataset (Dataset): The processed dataset with tokenized and grouped texts.
    """
    dataset = load_dataset("csv", data_files=csv_path, split="train")

    dataset = dataset.train_test_split(test_size=0.2)

    def preprocess_function(d):
        txt = tokenizer.special_tokens_map["bos_token"] + d["quote"] + tokenizer.special_tokens_map["eos_token"]
        return tokenizer(txt, max_length=100)

    tokenized = dataset.map(
        preprocess_function,
        remove_columns=dataset["train"].column_names,
    )

    lm_dataset = tokenized.map(group_texts, batched=True, num_proc=4)

    return lm_dataset


def finetune(csv_path, acc_token):
    """
    Fine-tunes a language model using a CSV dataset.

    Args:
        csv_path (str): The path to the CSV file containing the dataset.
        token (str): The token for authentication.

    Returns:
        None
    """
    base_model = "gpt2"
    result_model = "myrtle"

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token

    lm_dataset = process_dataset(csv_path, tokenizer)

    model = AutoModelForCausalLM.from_pretrained(base_model)

    tokenizer.push_to_hub(result_model, use_auth_token=acc_token)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        overwrite_output_dir=True,
        output_dir=result_model,
        evaluation_strategy="epoch",
        learning_rate=1.372e-4,
        weight_decay=0.01,
        save_total_limit=10,
        save_strategy="epoch",
        save_steps=1,
        report_to=None,
        seed=random.randint(0, 2**32 - 1),
        logging_steps=5,
        do_eval=True,
        eval_steps=1,
        load_best_model_at_end=True,
        push_to_hub=True,
        push_to_hub_token=acc_token,
        num_train_epochs=5,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=lm_dataset["train"],
        eval_dataset=lm_dataset["test"],
        data_collator=data_collator,
    )
    trainer.train()
    console.log("Starting training...")
    console.log("Training finished!")
    eval_results = trainer.evaluate()
    console.log(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")
