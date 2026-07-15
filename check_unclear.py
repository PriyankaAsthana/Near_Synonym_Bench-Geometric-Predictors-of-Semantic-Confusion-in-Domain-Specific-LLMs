import pandas as pd

df = pd.read_csv("results/llm_confusion_results.csv")

unclear = df[df["verdict"] == "unclear"]
print(f"Total unclear: {len(unclear)}")
print(f"\nSample unclear responses:\n")

for _, row in unclear.head(20).iterrows():
    print(f"Pair: {row['term_a']} vs {row['term_b']}")
    print(f"Model: {row['llm_model']}")
    print(f"Answer: {row['answer']}")
    print(f"Expected correct: {row['used_correct']}")
    print("-"*50)