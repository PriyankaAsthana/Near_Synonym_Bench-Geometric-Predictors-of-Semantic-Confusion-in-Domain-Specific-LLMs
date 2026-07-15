import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr, spearmanr
import pandas as pd
from tqdm import tqdm
import os

MODELS = [
    "all-MiniLM-L6-v2",
    "all-mpnet-base-v2",
    "paraphrase-multilingual-MiniLM-L12-v2",
    "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"
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

def compute_geometry(term_a, term_b, model):
    embeddings = model.encode([term_a, term_b])
    vec_a = embeddings[0]
    vec_b = embeddings[1]
    
    cosine_sim = 1 - cosine(vec_a, vec_b)
    
    l2_dist = float(np.linalg.norm(vec_a - vec_b))
    
    norm_a = vec_a / np.linalg.norm(vec_a)
    norm_b = vec_b / np.linalg.norm(vec_b)
    angular_dist = float(np.arccos(
        np.clip(np.dot(norm_a, norm_b), -1.0, 1.0)
    ))
    
    dim = len(vec_a)
    index = faiss.IndexFlatL2(dim)
    index.add(np.array([vec_a]).astype("float32"))
    distances, indices = index.search(
        np.array([vec_b]).astype("float32"), 1
    )
    is_nearest_neighbour = bool(indices[0][0] == 0)
    
    return {
        "cosine_similarity": round(float(cosine_sim), 6),
        "l2_distance": round(l2_dist, 6),
        "angular_distance": round(angular_dist, 6),
        "is_nearest_neighbour": is_nearest_neighbour,
        "embedding_dim": dim
    }

def run_geometry_analysis():
    pairs = load_pairs()
    print(f"Loaded {len(pairs)} concept pairs")
    
    all_results = []
    
    for model_name in MODELS:
        print(f"\nProcessing model: {model_name}")
        model = SentenceTransformer(model_name)
        
        for pair in tqdm(pairs, desc=model_name):
            geometry = compute_geometry(
                pair["term_a"],
                pair["term_b"],
                model
            )
            
            result = {
                "pair_id": pair["id"],
                "domain": pair["domain"],
                "term_a": pair["term_a"],
                "term_b": pair["term_b"],
                "stakes": pair["stakes"],
                "model": model_name,
                **geometry
            }
            all_results.append(result)
    
    df = pd.DataFrame(all_results)
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/geometry_results.csv", index=False)
    print(f"\nGeometry results saved to results/geometry_results.csv")
    
    print("\n" + "="*60)
    print("GEOMETRY SUMMARY BY MODEL")
    print("="*60)
    
    for model_name in MODELS:
        subset = df[df["model"] == model_name]
        print(f"\n{model_name}")
        print(f"  Mean cosine similarity:  {subset['cosine_similarity'].mean():.4f}")
        print(f"  Mean L2 distance:        {subset['l2_distance'].mean():.4f}")
        print(f"  Mean angular distance:   {subset['angular_distance'].mean():.4f}")
        print(f"  Nearest neighbour pairs: {subset['is_nearest_neighbour'].sum()}/{len(subset)}")
    
    print("\n" + "="*60)
    print("TOP 10 MOST GEOMETRICALLY CONFUSED PAIRS (all-mpnet)")
    print("="*60)
    
    mpnet = df[df["model"] == "all-mpnet-base-v2"].copy()
    mpnet_sorted = mpnet.sort_values(
        "cosine_similarity", ascending=False
    ).head(10)
    
    for _, row in mpnet_sorted.iterrows():
        print(f"  {row['term_a']} vs {row['term_b']}")
        print(f"    cosine={row['cosine_similarity']:.4f} | "
              f"domain={row['domain']} | stakes={row['stakes']}")
    
    print("\n" + "="*60)
    print("GEOMETRY BY DOMAIN")
    print("="*60)
    
    for domain in ["medical", "cultural_heritage", "emergency_resource"]:
        subset = df[df["domain"] == domain]
        print(f"\n{domain}")
        print(f"  Mean cosine similarity: "
              f"{subset['cosine_similarity'].mean():.4f}")
        print(f"  Max cosine similarity:  "
              f"{subset['cosine_similarity'].max():.4f}")
        print(f"  Min cosine similarity:  "
              f"{subset['cosine_similarity'].min():.4f}")
    
    return df

if __name__ == "__main__":
    df = run_geometry_analysis()
    print("\nPhase 2 complete.")
    print(f"Total measurements: {len(df)}")
    print(f"  ({len(MODELS)} models x 120 pairs = {len(MODELS)*120} expected)")