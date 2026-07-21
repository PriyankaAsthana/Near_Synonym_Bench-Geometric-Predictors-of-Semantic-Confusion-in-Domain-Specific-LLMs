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


def probe_forced_v2(pair: dict, model_name: str) -> dict:
    is_qwen = "qwen" in model_name.lower()

    prompt = f"""Choose exactly one term to answer the question.

Term A: {pair['term_a']}
Term B: {pair['term_b']}

Question: {pair['confusion_probe']}

Reply with only Term A or Term B. Nothing else."""

    try:
        kwargs = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 80
        }

        if is_qwen:
            kwargs["extra_body"] = {
                "enable_thinking": False
            }

        response = client.chat.completions.create(**kwargs)
        answer = response.choices[0].message.content.strip()
        answer_lower = answer.lower()

        correct_answer = pair["correct_answer"].lower()
        confused_answer = pair["confused_answer"].lower()
        term_a = pair["term_a"].lower()
        term_b = pair["term_b"].lower()

        found_correct = (
            correct_answer in answer_lower
        )
        found_confused = (
            confused_answer in answer_lower and
            correct_answer not in answer_lower
        )

        if not found_correct and not found_confused:
            if term_a in answer_lower and term_b not in answer_lower:
                if term_a == correct_answer:
                    found_correct = True
                else:
                    found_confused = True
            elif term_b in answer_lower and term_a not in answer_lower:
                if term_b == correct_answer:
                    found_correct = True
                else:
                    found_confused = True

        if found_correct and not found_confused:
            verdict = "correct"
            confusion_score = 0.0
        elif found_confused and not found_correct:
            verdict = "confused"
            confusion_score = 1.0
        elif found_correct and found_confused:
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


def run_probing():
    pairs = load_pairs()
    print(f"Loaded {len(pairs)} concept pairs")
    print(f"Testing {len(MODELS_TO_TEST)} LLM models")
    print(f"Total probes: {len(pairs) * len(MODELS_TO_TEST)}")
    print(f"Qwen thinking disabled\n")

    all_results = []

    for model_name in MODELS_TO_TEST:
        print(f"Probing: {model_name}")

        for pair in tqdm(pairs, desc=model_name):
            result = probe_forced_v2(pair, model_name)
            all_results.append(result)
            time.sleep(2)

    df = pd.DataFrame(all_results)
    os.makedirs("results", exist_ok=True)
    df.to_csv(
        "results/llm_forced_v2_results.csv",
        index=False
    )

    print(f"\nResults saved to results/llm_forced_v2_results.csv")

    print("\n" + "="*60)
    print("FORCED CHOICE V2 RESULTS BY MODEL")
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
    print("ARE LLAMA RESULTS STILL IDENTICAL?")
    print("="*60)

    l8_confused = set(
        df[
            (df["llm_model"] == "llama-3.1-8b-instant") &
            (df["verdict"] == "confused")
        ]["pair_id"].tolist()
    )
    l70_confused = set(
        df[
            (df["llm_model"] == "llama-3.3-70b-versatile") &
            (df["verdict"] == "confused")
        ]["pair_id"].tolist()
    )
    print(f"LLaMA 8B confused pairs:  {len(l8_confused)}")
    print(f"LLaMA 70B confused pairs: {len(l70_confused)}")
    print(f"Overlap: {len(l8_confused & l70_confused)}")

    print("\n" + "="*60)
    print("TOP CONFUSED PAIRS")
    print("="*60)

    avg_confusion = df.groupby(
        ["pair_id", "term_a", "term_b", "domain", "stakes"]
    )["confusion_score"].mean().reset_index()
    top = avg_confusion.sort_values(
        "confusion_score", ascending=False
    ).head(15)

    for _, row in top.iterrows():
        print(f"\n  {row['term_a']} vs {row['term_b']}")
        print(f"    confusion={row['confusion_score']:.3f} | "
              f"domain={row['domain']} | "
              f"stakes={row['stakes']}")

    return df


if __name__ == "__main__":
    df = run_probing()
    print(f"\nPhase 3c complete.")
    print(f"Total probes: {len(df)}")