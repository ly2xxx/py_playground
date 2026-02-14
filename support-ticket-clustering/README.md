# Customer Support Ticket Clustering - POC

**Unsupervised Machine Learning for Pattern Discovery in Support Tickets**

This project demonstrates how unsupervised ML can automatically discover hidden patterns in customer support data without manual labeling.

---

## 🎯 What This Does

1. **Discovers Hidden Patterns** - Automatically groups similar tickets
2. **Identifies Problem Areas** - Finds clusters with long resolution times
3. **Reveals Time Patterns** - Shows when tickets spike
4. **Measures Satisfaction** - Links clusters to customer ratings
5. **Generates Insights** - Actionable recommendations for support teams

---

## 📦 Quick Start

### 1. Install Dependencies

```bash
cd C:\code\support-ticket-clustering
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

```bash
python generate_data.py
```

This creates `support_tickets.csv` with ~100 tickets across 5 days.

**Data includes:**
- 7 realistic ticket categories (Login, Payment, Bugs, etc.)
- Timestamps, priorities, status
- Resolution times, customer satisfaction scores

### 3. Run Analysis

```bash
python analyze_tickets.py
```

**Output:**
- `cluster_analysis.png` - Visual clusters and distributions
- `temporal_analysis.png` - Time patterns and metrics
- `tickets_with_clusters.csv` - Original data + cluster assignments
- Console insights with actionable recommendations

---

## 📊 What You'll See

### Cluster Analysis (`cluster_analysis.png`)
- **Top-left**: Discovered clusters (unsupervised learning)
- **Top-right**: Actual topics (ground truth comparison)
- **Bottom-left**: Ticket distribution per cluster
- **Bottom-right**: Priority levels by cluster

### Temporal Analysis (`temporal_analysis.png`)
- **Top-left**: Daily ticket volume trends
- **Top-right**: Hourly patterns (peak times)
- **Bottom-left**: Resolution time by cluster (box plots)
- **Bottom-right**: Customer satisfaction by cluster

### Console Insights
```
💡 KEY INSIGHTS DISCOVERED:
1. ⚠️ SLOWEST CLUSTER: Cluster 2
   Average resolution time: 48.3 hours
   
2. 📈 PEAK HOUR: 14:00
   23 tickets (23% of daily volume)
   
3. 🚨 HIGH-PRIORITY HOTSPOT: Cluster 3
   12 critical tickets
   
4. 😞 LOWEST SATISFACTION: Cluster 1
   Average rating: 2.3/5
   
5. 📊 VOLUME TREND: INCREASING
   Day 1: 17 tickets → Day 5: 24 tickets
```

---

## 🔬 Technical Details

### Algorithms Used

**1. TF-IDF Vectorization**
- Converts text to numerical features
- Captures important words/phrases

**2. K-Means Clustering**
- Groups similar tickets automatically
- Optimal cluster count via silhouette score

**3. PCA (Principal Component Analysis)**
- Reduces dimensions for visualization
- Projects high-D data to 2D

### Features Analyzed

- **Text**: Conversation content (TF-IDF embeddings)
- **Temporal**: Created time, hour patterns
- **Categorical**: Priority, status, topic
- **Metrics**: Resolution time, satisfaction

---

## 💡 Real-World Applications

### 1. Auto-Routing
Once clusters are discovered and labeled, build a classifier to route new tickets automatically.

### 2. Resource Planning
Schedule more agents during peak hours identified in analysis.

### 3. Process Improvement
Focus training on clusters with low satisfaction or long resolution times.

### 4. Proactive Monitoring
Alert when a new pattern emerges (anomaly detection).

### 5. SLA Optimization
Set different SLAs per cluster based on complexity.

---

## 🎨 Customization

### Generate More Data

Edit `generate_data.py`:
```python
df = generate_tickets(num_tickets=500, num_days=30)  # 500 tickets, 30 days
```

### Add Your Own Topics

Edit `TICKET_TEMPLATES` in `generate_data.py`:
```python
TICKET_TEMPLATES = {
    "Your Topic": [
        "Example ticket text 1",
        "Example ticket text 2",
    ],
}
```

### Change Cluster Count

Edit `analyze_tickets.py`:
```python
# Force specific number of clusters
df['text_cluster'] = KMeans(n_clusters=8).fit_predict(X)
```

---

## 📈 Next Steps

### Phase 2: Advanced Modeling
- **BERTopic** - State-of-the-art topic modeling
- **Sentence Transformers** - Better text embeddings
- **DBSCAN** - Density-based clustering (finds arbitrary shapes)

### Phase 3: Production
- Real-time clustering API
- Dashboard with live updates
- Integration with ticketing system

### Phase 4: Supervised Learning
- Label discovered clusters
- Train classifier for auto-routing
- Predict resolution time

---

## 🐛 Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"CSV not found"**
```bash
# Generate data first
python generate_data.py
```

**Plots don't show**
- They're saved as PNG files automatically
- Open `cluster_analysis.png` and `temporal_analysis.png`

**Want different patterns?**
- Delete `support_tickets.csv` and run `generate_data.py` again
- Random seed creates different data each time

---

## 📚 Learn More

**Clustering Algorithms:**
- [K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [DBSCAN](https://scikit-learn.org/stable/modules/clustering.html#dbscan)
- [Silhouette Analysis](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html)

**Text Processing:**
- [TF-IDF](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)
- [Sentence Transformers](https://www.sbert.net/)

**Visualization:**
- [PCA](https://scikit-learn.org/stable/modules/decomposition.html#pca)
- [t-SNE](https://scikit-learn.org/stable/modules/manifold.html#t-sne)

---

## 🤝 Contributing

This is a POC! Suggestions welcome:
- More realistic ticket templates
- Additional clustering algorithms
- Better visualizations
- Production deployment guide

---

## ✅ Summary

**What unsupervised ML discovered:**
✅ Hidden ticket patterns without manual labeling
✅ Problem clusters (slow resolution, low satisfaction)
✅ Peak times for staffing optimization
✅ Relationships between clusters and outcomes

**Why it's effective:**
✅ No labeling required (saves time)
✅ Discovers unknown patterns (surprises!)
✅ Scales to millions of tickets
✅ Adapts as patterns change over time

**Next steps:**
✅ Run with your real data
✅ Fine-tune cluster count
✅ Build supervised classifier on top
✅ Deploy to production

---

**Questions?** Open an issue or reach out!

🚀 Happy clustering!
