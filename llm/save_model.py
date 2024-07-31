from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM
import os
import argparse

parser = argparse.ArgumentParser(description="Save model to local")
parser.add_argument("--model_id", type=str, required=True, help="Hugging face model id")
parser.add_argument(
    "--model_path", type=str, default="./llm/app", help="Local path to save the model"
)
args = parser.parse_args()


def main():
    """Main module to save the model"""
    model_id = args.model_id
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_id)

    # save model and tokenizer
    model.save_pretrained(os.path.join(args.model_path, "model"))
    tokenizer.save_pretrained(os.path.join(args.model_path, "tokenizer"))


if __name__ == "__main__":
    main()
