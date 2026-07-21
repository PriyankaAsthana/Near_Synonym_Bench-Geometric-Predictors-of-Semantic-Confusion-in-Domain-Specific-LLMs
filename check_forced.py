import pandas as pd

df = pd.read_csv("results/llm_forced_choice_results.csv")

print("QWEN SAMPLE RESPONSES")
print("="*60)
qwen = df[df["llm_model"] == "qwen/qwen3-32b"]
for _, row in qwen.head(10).iterrows():
    print(f"\nPair: {row['term_a']} vs {row['term_b']}")
    print(f"Answer: {row['answer'][:200]}")
    print(f"Verdict: {row['verdict']}")

print("\n\nLLAMA 8B CONFLATED SAMPLE")
print("="*60)
llama8 = df[
    (df["llm_model"] == "llama-3.1-8b-instant") &
    (df["verdict"] == "conflated")
]
for _, row in llama8.head(10).iterrows():
    print(f"\nPair: {row['term_a']} vs {row['term_b']}")
    print(f"Answer: {row['answer']}")

print("\n\nLLAMA 70B CONFLATED SAMPLE")
print("="*60)
llama70 = df[
    (df["llm_model"] == "llama-3.3-70b-versatile") &
    (df["verdict"] == "conflated")
]
for _, row in llama70.head(10).iterrows():
    print(f"\nPair: {row['term_a']} vs {row['term_b']}")
    print(f"Answer: {row['answer']}")

print("\n\nARE LLAMA RESULTS IDENTICAL?")
print("="*60)
llama8_pairs = set(
    df[
        (df["llm_model"] == "llama-3.1-8b-instant") &
        (df["verdict"] == "conflated")
    ]["pair_id"].tolist()
)
llama70_pairs = set(
    df[
        (df["llm_model"] == "llama-3.3-70b-versatile") &
        (df["verdict"] == "conflated")
    ]["pair_id"].tolist()
)
print(f"LLaMA 8B conflated pairs: {len(llama8_pairs)}")
print(f"LLaMA 70B conflated pairs: {len(llama70_pairs)}")
print(f"Overlap: {len(llama8_pairs & llama70_pairs)}")
print(f"Same pairs: {llama8_pairs == llama70_pairs}")