# Phase 2: Advanced Modeling

**State-of-the-art NLP for discovering hidden patterns from minimal data**

## What's New in Phase 2

### Advanced Techniques

1. **Sentence Transformers** - Neural semantic embeddings (384-dim vectors)
2. **HDBSCAN** - Density-based clustering (finds arbitrary shapes, auto-determines cluster count)
3. **UMAP** - Superior dimensionality reduction (preserves local + global structure)
4. **BERTopic** - Automatic topic modeling with coherent labels

### Why Phase 2?

**Phase 1** used TF-IDF + K-Means:
- ✅ Fast, simple, interpretable
- ❌ Bag-of-words (ignores context)
- ❌ Assumes spherical clusters
- ❌ Requires manual cluster count

**Phase 2** uses deep learning:
- ✅ **Semantic understanding** - "payment failed" similar to "transaction error"
- ✅ **Arbitrary cluster shapes** - handles real-world data better
- ✅ **Auto cluster count** - no guessing optimal K
- ✅ **Better with limited data** - learns from pre-trained models

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_advanced.txt
```

**Note:** First run will download ~90MB model (all-MiniLM-L6-v2)

### 2. Prepare Your Data

CSV format with **minimum 3 columns**:
```
ticket_id,created_at,conversation
TKT-1000,08/02/2026 09:53,Password reset not working
TKT-1001,11/02/2026 15:53,Can I get a refund?
```

**Required:**
- `ticket_id`: Unique identifier
- `created_at`: Timestamp (DD/MM/YYYY HH:MM format)
- `conversation`: Ticket text (any length)

**No other fields needed!** The algorithm extracts patterns from text alone.

### 3. Run Analysis

```bash
cd C:\code\support-ticket-clustering
python analyze_advanced.py
```

**Runtime:** ~1-2 minutes for 100 tickets (depends on CPU)

---

## Output Files

### Visualizations

**1. `advanced_clustering.png`**
- HDBSCAN clusters (density-based)
- BERTopic topics (semantic themes)
- Cluster size distribution
- Temporal patterns by cluster

**2. `temporal_advanced.png`**
- Daily ticket volume
- Hourly distribution
- Cluster trends over time
- Text length analysis

### Data Files

**3. `tickets_advanced_clustered.csv`**
- Original data + cluster assignments
- Topic IDs (if BERTopic installed)
- 2D coordinates (x, y for plotting)

**4. `embeddings.npy`**
- 384-dimensional semantic vectors
- Reusable for future analysis
- Can build classifiers on top

---

## How It Works

### Step 1: Semantic Embeddings

```python
# Converts text to 384-dim vectors that capture meaning
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(conversations)
```

**Example:**
- "Password expired" → [0.23, -0.45, 0.67, ...]
- "Password not working" → [0.25, -0.43, 0.69, ...] (similar!)
- "Need refund" → [-0.12, 0.88, -0.34, ...] (different)

### Step 2: Density-Based Clustering

```python
# HDBSCAN finds clusters of any shape
clusterer = HDBSCAN(min_cluster_size=3)
clusters = clusterer.fit_predict(embeddings)
```

**Advantages:**
- Finds dense regions automatically
- Marks outliers as "noise" (cluster = -1)
- No need to specify number of clusters

### Step 3: Dimensionality Reduction

```python
# UMAP: 384D → 2D while preserving structure
reducer = UMAP(n_components=2)
coords_2d = reducer.fit_transform(embeddings)
```

**Why UMAP > PCA:**
- Preserves local neighborhoods
- Non-linear (handles complex patterns)
- Better for visualization

### Step 4: Topic Modeling (Optional)

```python
# BERTopic: Auto-labels topics with keywords
topic_model = BERTopic()
topics = topic_model.fit_transform(texts, embeddings)
```

**Example output:**
- Topic 0: "password, reset, expired, link"
- Topic 1: "payment, failed, card, charge"

---

## Sample Results

### Console Output

```
[OK] Loaded 100 tickets with 3 columns
[EMBED] Generating embeddings with all-MiniLM-L6-v2...
[OK] Generated 100 embeddings of dimension 384
[CLUSTER] Running HDBSCAN (min_cluster_size=3)...
[RESULT] Discovered 8 clusters
[INFO] Noise points (unclustered): 12
[METRIC] Silhouette score: 0.342

[INSIGHTS] ADVANCED CLUSTERING DISCOVERIES
================================================
Cluster 0: 23 tickets - Password/authentication issues
Cluster 1: 18 tickets - Payment failures
Cluster 2: 15 tickets - Dashboard/UI bugs
...
```

### Discovered Patterns

Even with **only 3 columns**, Phase 2 finds:
- ✅ Semantic groupings ("can't login" + "password wrong" = same cluster)
- ✅ Time patterns (login issues spike at 9am)
- ✅ Outliers (unusual tickets marked as noise)
- ✅ Topic keywords (auto-generated labels)

---

## Customization

### Adjust Cluster Sensitivity

**Find more clusters:**
```python
clusters = cluster_hdbscan(embeddings, min_cluster_size=2)  # Smaller groups
```

**Find fewer clusters:**
```python
clusters = cluster_hdbscan(embeddings, min_cluster_size=5)  # Larger groups
```

### Use Different Embedding Model

**For longer texts:**
```python
embeddings = generate_embeddings(texts, model_name='all-mpnet-base-v2')  # 768-dim, slower, better
```

**For multilingual:**
```python
embeddings = generate_embeddings(texts, model_name='paraphrase-multilingual-MiniLM-L12-v2')
```

### Skip BERTopic (Faster)

If BERTopic is slow or not needed:
```bash
pip uninstall bertopic
```
Script will automatically skip topic modeling.

---

## Comparison: Phase 1 vs Phase 2

| Feature | Phase 1 (TF-IDF) | Phase 2 (Transformers) |
|---------|------------------|------------------------|
| **Embeddings** | TF-IDF (sparse) | Neural (384-dim dense) |
| **Clustering** | K-Means | HDBSCAN |
| **Dimensionality** | PCA | UMAP |
| **Cluster count** | Manual (K) | Automatic |
| **Semantic understanding** | ❌ No | ✅ Yes |
| **Speed** | ⚡ Very fast | 🐌 Slower (1st run) |
| **Dependencies** | Minimal | Sentence Transformers |
| **Best for** | Quick prototypes | Production quality |

**When to use Phase 1:**
- Quick experiments
- Large datasets (>10k tickets)
- No GPU available

**When to use Phase 2:**
- Better accuracy needed
- Semantic similarity matters
- Limited data (<1000 tickets)

---

## Troubleshooting

### "Model not found" error
```bash
# Clear cache and re-download
rm -rf ~/.cache/torch/sentence_transformers
python analyze_advanced.py
```

### Memory issues
```python
# Use smaller model
embeddings = generate_embeddings(texts, model_name='all-MiniLM-L6-v2')  # 384-dim
# Instead of:
# model_name='all-mpnet-base-v2'  # 768-dim
```

### HDBSCAN finds no clusters
```python
# Reduce min_cluster_size
clusters = cluster_hdbscan(embeddings, min_cluster_size=2)
```

### BERTopic errors
```bash
# Optional - skip if problematic
pip uninstall bertopic
```

---

## Next Steps

### Phase 3: Production Deployment

1. **Build Classifier**
   - Train supervised model on discovered clusters
   - Auto-tag new tickets in real-time

2. **API Endpoint**
   - Flask/FastAPI service
   - POST ticket → GET cluster + topic

3. **Dashboard**
   - Streamlit/Dash for live monitoring
   - Alert on emerging patterns

4. **Continuous Learning**
   - Retrain weekly with new tickets
   - Detect concept drift

### Example: Build Classifier

```python
from sklearn.svm import SVC

# Load saved embeddings and clusters
embeddings = np.load('embeddings.npy')
df = pd.read_csv('tickets_advanced_clustered.csv')

# Train classifier on discovered patterns
X = embeddings
y = df['cluster']
classifier = SVC().fit(X, y)

# Predict new ticket
new_ticket = "Payment not working"
new_embedding = model.encode([new_ticket])
predicted_cluster = classifier.predict(new_embedding)
```

---

## Advanced Tips

### Save Model for Reuse

```python
# Save for faster subsequent runs
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('my_model/')

# Later:
model = SentenceTransformer('my_model/')
```

### Batch Processing

```python
# For large datasets
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
```

### GPU Acceleration

```bash
pip install torch torchvision
# Model automatically uses CUDA if available
```

---

## References

- **Sentence Transformers:** https://www.sbert.net/
- **HDBSCAN:** https://hdbscan.readthedocs.io/
- **UMAP:** https://umap-learn.readthedocs.io/
- **BERTopic:** https://maartengr.github.io/BERTopic/

---

## Summary

**Phase 2 gives you:**
- ✅ Better clusters from minimal data
- ✅ Semantic understanding (not just keywords)
- ✅ Automatic pattern discovery
- ✅ Production-ready embeddings

**Perfect for:**
- Real-world support tickets
- Limited labeled data
- Discovering unknown patterns
- Building intelligent routing

**Try it now:**
```bash
python analyze_advanced.py
```

🚀 **Let the neural networks find patterns you didn't know existed!**
