import json
import time
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODELS_TO_TEST = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "qwen/qwen3-32b"
]

def load_pairs(path="data/concept_pairs.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pairs = []
    for domain, items in data.items():
        for item in items:
            item["domain"] = domain
            pairs.append(item)
    return pairs


def probe_model(pair: dict, model_name: str) -> dict:
    prompt = f"""Answer the following medical or domain-specific question 
in one sentence. Be precise and use the exact correct technical term.

Question: {pair['confusion_probe']}

Answer in one sentence:"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=100
        )
        answer = response.choices[0].message.content.strip().lower()

        correct = pair["correct_answer"].lower()
        confused = pair["confused_answer"].lower()

        used_correct = correct in answer
        used_confused = confused in answer
        used_both = used_correct and used_confused

        if used_both:
            confusion_score = 0.5
            verdict = "conflated"
        elif used_correct:
            confusion_score = 0.0
            verdict = "correct"
        elif used_confused:
            confusion_score = 1.0
            verdict = "confused"
        else:
            confusion_score = 0.5
            verdict = "unclear"

        return {
            "pair_id": pair["id"],
            "domain": pair["domain"],
            "term_a": pair["term_a"],
            "term_b": pair["term_b"],
            "stakes": pair["stakes"],
            "llm_model": model_name,
            "answer": response.choices[0].message.content.strip(),
            "used_correct": used_correct,
            "used_confused": used_confused,
            "confusion_score": confusion_score,
            "verdict": verdict
        }

    except Exception as e:
        print(f"Error on {pair['id']} with {model_name}: {e}")
        time.sleep(10)
        return {
            "pair_id": pair["id"],
            "domain": pair["domain"],
            "term_a": pair["term_a"],
            "term_b": pair["term_b"],
            "stakes": pair["stakes"],
            "llm_model": model_name,
            "answer": "ERROR",
            "used_correct": False,
            "used_confused": False,
            "confusion_score": 0.5,
            "verdict": "error"
        }


def run_probing():
    pairs = load_pairs()
    print(f"Loaded {len(pairs)} concept pairs")
    print(f"Testing {len(MODELS_TO_TEST)} LLM models")
    print(f"Total probes: {len(pairs) * len(MODELS_TO_TEST)}")

    all_results = []

    for model_name in MODELS_TO_TEST:
        print(f"\nProbing model: {model_name}")

        for pair in tqdm(pairs, desc=model_name):
            result = probe_model(pair, model_name)
            all_results.append(result)
            time.sleep(2)

    df = pd.DataFrame(all_results)
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/llm_confusion_results.csv", index=False)
    print(f"\nResults saved to results/llm_confusion_results.csv")

    print("\n" + "="*60)
    print("CONFUSION RATE BY MODEL")
    print("="*60)

    for model_name in MODELS_TO_TEST:
        subset = df[df["llm_model"] == model_name]
        confused = subset[subset["verdict"] == "confused"]
        correct = subset[subset["verdict"] == "correct"]
        unclear = subset[subset["verdict"] == "unclear"]

        print(f"\n{model_name}")
        print(f"  Correct:   {len(correct)}/{len(subset)} "
              f"({len(correct)/len(subset)*100:.1f}%)")
        print(f"  Confused:  {len(confused)}/{len(subset)} "
              f"({len(confused)/len(subset)*100:.1f}%)")
        print(f"  Unclear:   {len(unclear)}/{len(subset)} "
              f"({len(unclear)/len(subset)*100:.1f}%)")

    print("\n" + "="*60)
    print("CONFUSION RATE BY DOMAIN")
    print("="*60)

    for domain in ["medical", "cultural_heritage", "emergency_resource"]:
        subset = df[df["domain"] == domain]
        confused = subset[subset["verdict"] == "confused"]
        print(f"\n{domain}")
        print(f"  Confusion rate: "
              f"{len(confused)/len(subset)*100:.1f}%")

    print("\n" + "="*60)
    print("TOP 10 MOST CONFUSED PAIRS ACROSS ALL MODELS")
    print("="*60)

    avg_confusion = df.groupby(
        ["pair_id", "term_a", "term_b", "domain", "stakes"]
    )["confusion_score"].mean().reset_index()
    avg_confusion = avg_confusion.sort_values(
        "confusion_score", ascending=False
    ).head(10)

    for _, row in avg_confusion.iterrows():
        print(f"\n  {row['term_a']} vs {row['term_b']}")
        print(f"    avg confusion={row['confusion_score']:.3f} | "
              f"domain={row['domain']} | stakes={row['stakes']}")

    print("\n" + "="*60)
    print("HIGH STAKES CONFUSION")
    print("="*60)

    high_stakes = df[df["stakes"] == "high"]
    confused_high = high_stakes[high_stakes["verdict"] == "confused"]
    print(f"\nHigh stakes pairs confused: "
          f"{len(confused_high)}/{len(high_stakes)} "
          f"({len(confused_high)/len(high_stakes)*100:.1f}%)")

    return df


if __name__ == "__main__":
    df = run_probing()
    print("\nPhase 3 complete.")
    print(f"Total probes run: {len(df)}")