import pandas as pd
import json
import os

df = pd.read_csv("results/llm_confusion_results.csv")

SYNONYM_MAP = {
    "cardiac arrest": [
        "cardiopulmonary arrest", "cpa", "cardiac standstill",
        "heart stopped", "no pulse", "pulseless"
    ],
    "heart attack": [
        "myocardial infarction", "mi", "coronary", "ami"
    ],
    "transient ischaemic attack": [
        "tia", "mini stroke", "mini-stroke", 
        "transient ischemic", "transient stroke"
    ],
    "stroke": [
        "cerebrovascular accident", "cva", "brain attack",
        "cerebral infarction", "brain stroke"
    ],
    "hypoglycemia": [
        "low blood sugar", "low glucose", "hypoglycaemia",
        "blood sugar low", "glucose low"
    ],
    "hypotension": [
        "low blood pressure", "bp low", "blood pressure dropped",
        "hypotensive"
    ],
    "sepsis": [
        "septicemia", "septicaemia", "blood poisoning",
        "systemic infection", "septic shock"
    ],
    "infection": [
        "bacterial infection", "viral infection", "infected",
        "pathogen", "microorganism"
    ],
    "anaphylaxis": [
        "anaphylactic shock", "anaphylactic", "severe allergic",
        "systemic allergic"
    ],
    "type 1 diabetes": [
        "type one diabetes", "t1d", "t1dm", "juvenile diabetes",
        "insulin dependent"
    ],
    "type 2 diabetes": [
        "type two diabetes", "t2d", "t2dm", "adult onset",
        "non-insulin dependent"
    ],
    "tachycardia": [
        "rapid heart rate", "fast heart rate", "elevated heart rate",
        "high heart rate", "svt", "rapid pulse"
    ],
    "bradycardia": [
        "slow heart rate", "low heart rate", "slow pulse"
    ],
    "ischaemia": [
        "ischemia", "reduced blood flow", "insufficient blood",
        "poor perfusion"
    ],
    "infarction": [
        "tissue death", "necrosis", "dead tissue",
        "myocardial infarction", "infarct"
    ],
    "embolism": [
        "pulmonary embolism", "pe", "clot in lung",
        "travelling clot", "embolic"
    ],
    "thrombosis": [
        "blood clot", "deep vein thrombosis", "dvt",
        "clot formation", "thrombus"
    ],
    "palliative care": [
        "comfort care", "supportive care", "symptom management",
        "pain management"
    ],
    "hospice care": [
        "end of life care", "terminal care", "dying care"
    ],
    "moksha": [
        "liberation", "mukti", "spiritual liberation",
        "final liberation", "ultimate liberation"
    ],
    "nirvana": [
        "enlightenment", "awakening", "buddhist liberation"
    ],
    "aarti": [
        "lamp ceremony", "arti", "deepak ceremony",
        "diya ceremony"
    ],
    "stupa": [
        "buddhist monument", "dome shaped monument",
        "reliquary", "dagoba"
    ],
    "ghat": [
        "river steps", "bathing steps", "stepped embankment"
    ],
    "raga": [
        "melodic framework", "melodic mode", "musical scale",
        "raag"
    ],
    "tala": [
        "rhythmic cycle", "time cycle", "beat cycle", "taal"
    ],
    "dharma": [
        "duty", "righteous duty", "sacred duty", "moral duty"
    ],
    "karma": [
        "cause and effect", "actions and consequences"
    ],
    "blood shortage": [
        "acute shortage", "supply shortage", "temporary shortage"
    ],
    "blood scarcity": [
        "chronic scarcity", "systemic scarcity", "long term shortage"
    ],
    "universal donor": [
        "o negative", "o-negative", "type o negative"
    ],
    "universal recipient": [
        "ab positive", "ab-positive", "type ab"
    ],
    "haemorrhage": [
        "hemorrhage", "bleeding", "blood loss", "haemorrhaging"
    ],
    "haematoma": [
        "hematoma", "blood collection", "blood pooling"
    ],
    "defibrillation": [
        "defibrillate", "shock", "aed", "electric shock",
        "unsynchronised shock"
    ],
    "cardioversion": [
        "synchronised shock", "synchronized cardioversion",
        "electrical cardioversion"
    ],
    "triage": [
        "patient sorting", "casualty sorting", "prioritisation"
    ],
    "voluntary donation": [
        "altruistic donation", "non-directed donation",
        "community donation"
    ],
    "directed donation": [
        "specific donation", "designated donation",
        "named donation"
    ],
    "token reservation": [
        "unit reservation", "blood reservation", "locking mechanism"
    ],
    "donor deferral": [
        "temporary deferral", "postponed donation",
        "deferred donor"
    ],
    "donor rejection": [
        "permanent exclusion", "permanently excluded",
        "lifetime ban"
    ]
}


def check_synonyms(answer_lower, term, synonym_map):
    if term.lower() in answer_lower:
        return True
    synonyms = synonym_map.get(term.lower(), [])
    for syn in synonyms:
        if syn.lower() in answer_lower:
            return True
    return False


def rescore_row(row, synonym_map):
    if row["verdict"] != "unclear":
        return row

    answer_lower = str(row["answer"]).lower()
    correct = str(row["term_a"]).lower()
    confused = str(row["term_b"]).lower()

    found_correct = check_synonyms(answer_lower, correct, synonym_map)
    found_confused = check_synonyms(answer_lower, confused, synonym_map)

    if found_correct and found_confused:
        row["verdict"] = "conflated"
        row["confusion_score"] = 0.5
        row["used_correct"] = True
        row["used_confused"] = True
    elif found_correct:
        row["verdict"] = "correct"
        row["confusion_score"] = 0.0
        row["used_correct"] = True
    elif found_confused:
        row["verdict"] = "confused"
        row["confusion_score"] = 1.0
        row["used_confused"] = True
    else:
        row["verdict"] = "evasion"
        row["confusion_score"] = 0.3

    return row


df_rescored = df.apply(
    lambda row: rescore_row(row, SYNONYM_MAP), axis=1
)

os.makedirs("results", exist_ok=True)
df_rescored.to_csv(
    "results/llm_confusion_rescored.csv", index=False
)

print("RESCORED RESULTS")
print("="*60)

for model in df_rescored["llm_model"].unique():
    subset = df_rescored[df_rescored["llm_model"] == model]
    correct = subset[subset["verdict"] == "correct"]
    confused = subset[subset["verdict"] == "confused"]
    evasion = subset[subset["verdict"] == "evasion"]
    conflated = subset[subset["verdict"] == "conflated"]
    unclear = subset[subset["verdict"] == "unclear"]

    print(f"\n{model}")
    print(f"  Correct:   {len(correct)}/{len(subset)} "
          f"({len(correct)/len(subset)*100:.1f}%)")
    print(f"  Confused:  {len(confused)}/{len(subset)} "
          f"({len(confused)/len(subset)*100:.1f}%)")
    print(f"  Evasion:   {len(evasion)}/{len(subset)} "
          f"({len(evasion)/len(subset)*100:.1f}%)")
    print(f"  Conflated: {len(conflated)}/{len(subset)} "
          f"({len(conflated)/len(subset)*100:.1f}%)")
    print(f"  Unclear:   {len(unclear)}/{len(subset)} "
          f"({len(unclear)/len(subset)*100:.1f}%)")

print("\n" + "="*60)
print("TOP 10 MOST CONFUSED PAIRS AFTER RESCORING")
print("="*60)

avg_confusion = df_rescored.groupby(
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
print("VERDICT DISTRIBUTION COMPARISON")
print("="*60)

print("\nBEFORE rescoring:")
print(df["verdict"].value_counts())
print("\nAFTER rescoring:")
print(df_rescored["verdict"].value_counts())

print("\nRescored results saved to "
      "results/llm_confusion_rescored.csv")