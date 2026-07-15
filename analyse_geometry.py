import pandas as pd
import numpy as np

df = pd.read_csv("results/geometry_results.csv")

print("="*60)
print("COSINE SIMILARITY BY MODEL AND DOMAIN")
print("="*60)

pivot = df.groupby(["model", "domain"])["cosine_similarity"].agg(
    ["mean", "max", "min", "std"]
).round(4)
print(pivot)

print("\n" + "="*60)
print("MEDICAL DOMAIN — MODEL COMPARISON")
print("="*60)

medical = df[df["domain"] == "medical"]
for model in df["model"].unique():
    subset = medical[medical["model"] == model]
    print(f"\n{model}")
    print(f"  Mean cosine: {subset['cosine_similarity'].mean():.4f}")
    print(f"  Max cosine:  {subset['cosine_similarity'].max():.4f}")
    print(f"  High-stakes mean: {subset[subset['stakes']=='high']['cosine_similarity'].mean():.4f}")

print("\n" + "="*60)
print("TOP 10 HIGHEST RISK PAIRS (highest cosine, all models avg)")
print("="*60)

avg_cosine = df.groupby(
    ["pair_id", "term_a", "term_b", "domain", "stakes"]
)["cosine_similarity"].mean().reset_index()
avg_cosine = avg_cosine.sort_values(
    "cosine_similarity", ascending=False
).head(10)

for _, row in avg_cosine.iterrows():
    print(f"\n  {row['term_a']} vs {row['term_b']}")
    print(f"    avg cosine={row['cosine_similarity']:.4f} | "
          f"domain={row['domain']} | stakes={row['stakes']}")

print("\n" + "="*60)
print("BIOBERT vs MINIML ON MEDICAL PAIRS")
print("="*60)

bio = df[
    (df["model"].str.contains("BioBERT")) & 
    (df["domain"] == "medical")
]["cosine_similarity"].mean()

mini = df[
    (df["model"] == "all-MiniLM-L6-v2") & 
    (df["domain"] == "medical")
]["cosine_similarity"].mean()

mpnet = df[
    (df["model"] == "all-mpnet-base-v2") & 
    (df["domain"] == "medical")
]["cosine_similarity"].mean()

print(f"\nBioBERT mean cosine on medical pairs:  {bio:.4f}")
print(f"MiniLM mean cosine on medical pairs:   {mini:.4f}")
print(f"MPNet mean cosine on medical pairs:    {mpnet:.4f}")
print(f"\nBioBERT reduction vs MiniLM:  {((mini-bio)/mini*100):.1f}%")
print(f"BioBERT reduction vs MPNet:   {((mpnet-bio)/mpnet*100):.1f}%")

print("\n" + "="*60)
print("STAKES ANALYSIS — HIGH STAKES CONFUSION RISK")
print("="*60)

high_stakes = df[df["stakes"] == "high"]
for model in df["model"].unique():
    subset = high_stakes[high_stakes["model"] == model]
    print(f"\n{model}")
    print(f"  High-stakes mean cosine: "
          f"{subset['cosine_similarity'].mean():.4f}")
    high_risk = subset[
        subset["cosine_similarity"] > 0.75
    ]
    print(f"  Pairs with cosine > 0.75: "
          f"{len(high_risk)}/{len(subset)}")