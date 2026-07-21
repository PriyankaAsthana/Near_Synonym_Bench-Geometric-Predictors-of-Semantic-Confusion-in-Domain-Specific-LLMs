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


def probe_forced_choice(pair: dict, model_name: str) -> dict:
    prompt = f"""You are a precise domain expert. Answer the question 
below by choosing EXACTLY ONE of the two terms provided. 
Do not explain. Do not hedge. Output only the chosen term.

Term A: {pair['term_a']}
Term B: {pair['term_b']}

Question: {pair['confusion_probe']}

You must respond with either "{pair['term_a']}" or 
"{pair['term_b']}" and nothing else."""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=30
        )
        answer = response.choices[0].message.content.strip()
        answer_lower = answer.lower()

        correct = pair["correct_answer"].lower()
        confused = pair["confused_answer"].lower()

        term_a = pair["term_a"].lower()
        term_b = pair["term_b"].lower()

        chose_correct = (
            correct in answer_lower or
            term_a in answer_lower
        )
        chose_confused = (
            confused in answer_lower or
            term_b in answer_lower
        )

        if chose_correct and not chose_confused:
            verdict = "correct"
            confusion_score = 0.0
        elif chose_confused and not chose_correct:
            verdict = "confused"
            confusion_score = 1.0
        elif chose_correct and chose_confused:
            verdict = "conflated"
            confusion_score = 0.5
        else:
            verdict = "unclear"
            confusion_score = 0.5

        return {
            "pair_id": pair["id"],
            "domain": pair["domain"],
            "term_a": pair["term_a"],
            "term_b": pair["term_b"],
            "stakes": pair["stakes"],
            "correct_answer": pair["correct_answer"],
            "confused_answer": pair["confused_answer"],
            "llm_model": model_name,
            "answer": answer,
            "verdict": verdict,
            "confusion_score": confusion_score
        }

    except Exception as e:
        print(f"\nError on {pair['id']} with {model_name}: {e}")
        time.sleep(10)
        return {
            "pair_id": pair["id"],
            "domain": pair["domain"],
            "term_a": pair["term_a"],
            "term_b": pair["term_b"],
            "stakes": pair["stakes"],
            "correct_answer": pair["correct_answer"],
            "confused_answer": pair["confused_answer"],
            "llm_model": model_name,
            "answer": "ERROR",
            "verdict": "error",
            "confusion_score": 0.5
        }


def run_forced_choice_probing():
    pairs = load_pairs()
    print(f"Loaded {len(pairs)} concept pairs")
    print(f"Testing {len(MODELS_TO_TEST)} LLM models")
    print(f"Total probes: {len(pairs) * len(MODELS_TO_TEST)}")
    print(f"Estimated time: ~15 minutes\n")

    all_results = []

    for model_name in MODELS_TO_TEST:
        print(f"Probing: {model_name}")

        for pair in tqdm(pairs, desc=model_name):
            result = probe_forced_choice(pair, model_name)
            all_results.append(result)
            time.sleep(2)

    df = pd.DataFrame(all_results)
    os.makedirs("results", exist_ok=True)
    df.to_csv(
        "results/llm_forced_choice_results.csv",
        index=False
    )

    print(f"\nResults saved to "
          f"results/llm_forced_choice_results.csv")

    print("\n" + "="*60)
    print("FORCED CHOICE CONFUSION RATE BY MODEL")
    print("="*60)

    for model_name in MODELS_TO_TEST:
        subset = df[df["llm_model"] == model_name]
        correct = subset[subset["verdict"] == "correct"]
        confused = subset[subset["verdict"] == "confused"]
        conflated = subset[subset["verdict"] == "conflated"]
        unclear = subset[subset["verdict"] == "unclear"]

        print(f"\n{model_name}")
        print(f"  Correct:   {len(correct)}/{len(subset)} "
              f"({len(correct)/len(subset)*100:.1f}%)")
        print(f"  Confused:  {len(confused)}/{len(subset)} "
              f"({len(confused)/len(subset)*100:.1f}%)")
        print(f"  Conflated: {len(conflated)}/{len(subset)} "
              f"({len(conflated)/len(subset)*100:.1f}%)")
        print(f"  Unclear:   {len(unclear)}/{len(subset)} "
              f"({len(unclear)/len(subset)*100:.1f}%)")

    print("\n" + "="*60)
    print("CONFUSION RATE BY DOMAIN")
    print("="*60)

    for domain in [
        "medical", "cultural_heritage", "emergency_resource"
    ]:
        subset = df[df["domain"] == domain]
        confused = subset[subset["verdict"] == "confused"]
        correct = subset[subset["verdict"] == "correct"]
        print(f"\n{domain}")
        print(f"  Accuracy:       "
              f"{len(correct)/len(subset)*100:.1f}%")
        print(f"  Confusion rate: "
              f"{len(confused)/len(subset)*100:.1f}%")

    print("\n" + "="*60)
    print("CONFUSION RATE BY STAKES")
    print("="*60)

    for stakes in ["high", "medium", "low"]:
        subset = df[df["stakes"] == stakes]
        confused = subset[subset["verdict"] == "confused"]
        print(f"\n{stakes} stakes")
        print(f"  Confusion rate: "
              f"{len(confused)/len(subset)*100:.1f}%")

    print("\n" + "="*60)
    print("TOP 15 MOST CONFUSED PAIRS")
    print("="*60)

    avg_confusion = df.groupby(
        ["pair_id", "term_a", "term_b", "domain", "stakes"]
    )["confusion_score"].mean().reset_index()
    avg_confusion = avg_confusion.sort_values(
        "confusion_score", ascending=False
    ).head(15)

    for _, row in avg_confusion.iterrows():
        print(f"\n  {row['term_a']} vs {row['term_b']}")
        print(f"    confusion={row['confusion_score']:.3f} | "
              f"domain={row['domain']} | "
              f"stakes={row['stakes']}")

    print("\n" + "="*60)
    print("HIGH STAKES CONFUSION SUMMARY")
    print("="*60)

    high_stakes = df[df["stakes"] == "high"]
    confused_high = high_stakes[
        high_stakes["verdict"] == "confused"
    ]
    correct_high = high_stakes[
        high_stakes["verdict"] == "correct"
    ]
    print(f"\nHigh stakes accuracy:       "
          f"{len(correct_high)/len(high_stakes)*100:.1f}%")
    print(f"High stakes confusion rate: "
          f"{len(confused_high)/len(high_stakes)*100:.1f}%")

    return df


if __name__ == "__main__":
    df = run_forced_choice_probing()
    print(f"\nPhase 3b complete.")
    print(f"Total forced-choice probes: {len(df)}")
    print(f"Evasion eliminated: 0 by design")