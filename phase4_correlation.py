import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import json
import os

geometry_df = pd.read_csv("results/geometry_results.csv")
confusion_df = pd.read_csv("results/llm_confusion_rescored.csv")

avg_geometry = geometry_df.groupby(
    ["pair_id", "domain", "stakes"]
)["cosine_similarity"].mean().reset_index()
avg_geometry.columns = [
    "pair_id", "domain", "stakes", "mean_cosine"
]

avg_confusion = confusion_df.groupby(
    ["pair_id", "term_a", "term_b", "domain", "stakes"]
)["confusion_score"].mean().reset_index()
avg_confusion.columns = [
    "pair_id", "term_a", "term_b", "domain",
    "stakes", "mean_confusion"
]

merged = pd.merge(avg_geometry, avg_confusion, on="pair_id")

os.makedirs("results", exist_ok=True)
merged.to_csv("results/geometry_confusion_merged.csv", index=False)

print("="*60)
print("PHASE 4 — GEOMETRIC PREDICTION OF LLM CONFUSION")
print("="*60)

pearson_r, pearson_p = pearsonr(
    merged["mean_cosine"],
    merged["mean_confusion"]
)
spearman_r, spearman_p = spearmanr(
    merged["mean_cosine"],
    merged["mean_confusion"]
)

print(f"\nOVERALL CORRELATION (n={len(merged)})")
print(f"  Pearson  r={pearson_r:.4f}  p={pearson_p:.4f}")
print(f"  Spearman r={spearman_r:.4f}  p={spearman_p:.4f}")

if pearson_p < 0.05:
    print(f"  → STATISTICALLY SIGNIFICANT (p<0.05)")
else:
    print(f"  → NOT significant (p={pearson_p:.4f})")

print("\n" + "="*60)
print("CORRELATION BY DOMAIN")
print("="*60)

for domain in ["medical", "cultural_heritage", "emergency_resource"]:
    subset = merged[merged["domain_x"] == domain]
    if len(subset) < 5:
        continue
    p_r, p_p = pearsonr(
        subset["mean_cosine"],
        subset["mean_confusion"]
    )
    s_r, s_p = spearmanr(
        subset["mean_cosine"],
        subset["mean_confusion"]
    )
    print(f"\n{domain} (n={len(subset)})")
    print(f"  Pearson  r={p_r:.4f}  p={p_p:.4f} "
          f"{'*' if p_p < 0.05 else ''}")
    print(f"  Spearman r={s_r:.4f}  p={s_p:.4f} "
          f"{'*' if s_p < 0.05 else ''}")

print("\n" + "="*60)
print("CORRELATION BY STAKES LEVEL")
print("="*60)

for stakes in ["high", "medium", "low"]:
    subset = merged[merged["stakes_x"] == stakes]
    if len(subset) < 5:
        continue
    p_r, p_p = pearsonr(
        subset["mean_cosine"],
        subset["mean_confusion"]
    )
    print(f"\n{stakes} stakes (n={len(subset)})")
    print(f"  Pearson  r={p_r:.4f}  p={p_p:.4f} "
          f"{'SIGNIFICANT *' if p_p < 0.05 else ''}")

print("\n" + "="*60)
print("HIGH COSINE = HIGH CONFUSION? TOP RISK PAIRS")
print("="*60)

high_risk = merged[
    merged["mean_cosine"] > 0.75
].sort_values("mean_confusion", ascending=False)

print(f"\nPairs with cosine > 0.75: {len(high_risk)}")
print(f"Their mean confusion score: "
      f"{high_risk['mean_confusion'].mean():.4f}")
print(f"vs low cosine pairs mean confusion: "
      f"{merged[merged['mean_cosine'] <= 0.75]['mean_confusion'].mean():.4f}")

print("\nTop risk pairs (high cosine AND high confusion):")
top_risk = high_risk[
    high_risk["mean_confusion"] > 0.3
]
for _, row in top_risk.iterrows():
    print(f"  {row['term_a']} vs {row['term_b']}")
    print(f"    cosine={row['mean_cosine']:.4f} | "
          f"confusion={row['mean_confusion']:.4f} | "
          f"stakes={row['stakes_x']}")

print("\n" + "="*60)
print("BIOBERT GEOMETRY CORRELATION")
print("="*60)

bio_geometry = geometry_df[
    geometry_df["model"].str.contains("BioBERT")
].groupby("pair_id")["cosine_similarity"].mean().reset_index()
bio_geometry.columns = ["pair_id", "bio_cosine"]

bio_merged = pd.merge(bio_geometry, avg_confusion, on="pair_id")

bio_p_r, bio_p_p = pearsonr(
    bio_merged["bio_cosine"],
    bio_merged["mean_confusion"]
)
bio_s_r, bio_s_p = spearmanr(
    bio_merged["bio_cosine"],
    bio_merged["mean_confusion"]
)

print(f"\nBioBERT geometry vs LLM confusion (n={len(bio_merged)})")
print(f"  Pearson  r={bio_p_r:.4f}  p={bio_p_p:.4f} "
      f"{'SIGNIFICANT *' if bio_p_p < 0.05 else ''}")
print(f"  Spearman r={bio_s_r:.4f}  p={bio_s_p:.4f} "
      f"{'SIGNIFICANT *' if bio_s_p < 0.05 else ''}")

general_geometry = geometry_df[
    geometry_df["model"] == "all-mpnet-base-v2"
].groupby("pair_id")["cosine_similarity"].mean().reset_index()
general_geometry.columns = ["pair_id", "general_cosine"]

gen_merged = pd.merge(general_geometry, avg_confusion, on="pair_id")

gen_p_r, gen_p_p = pearsonr(
    gen_merged["general_cosine"],
    gen_merged["mean_confusion"]
)

print(f"\nMPNet geometry vs LLM confusion (n={len(gen_merged)})")
print(f"  Pearson  r={gen_p_r:.4f}  p={gen_p_p:.4f} "
      f"{'SIGNIFICANT *' if gen_p_p < 0.05 else ''}")

print("\n" + "="*60)
print("SUMMARY FOR PAPER")
print("="*60)
print(f"\nKey finding 1: Overall Pearson r={pearson_r:.4f} "
      f"(p={pearson_p:.4f})")
print(f"Key finding 2: BioBERT Pearson r={bio_p_r:.4f} "
      f"(p={bio_p_p:.4f})")
print(f"Key finding 3: MPNet Pearson r={gen_p_r:.4f} "
      f"(p={gen_p_p:.4f})")
print(f"\nHigh cosine pairs (>0.75) mean confusion: "
      f"{high_risk['mean_confusion'].mean():.4f}")
print(f"Low cosine pairs (<=0.75) mean confusion:  "
      f"{merged[merged['mean_cosine'] <= 0.75]['mean_confusion'].mean():.4f}")