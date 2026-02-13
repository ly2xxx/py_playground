# Quick Start Guide

## Run the POC in 30 seconds

### Step 1: Generate Data
```bash
cd C:\code\support-ticket-clustering
python generate_data.py
```

**Output:** `support_tickets.csv` (100 tickets across 5 days)

---

### Step 2: Run Analysis
```bash
python analyze_tickets.py
```

**Or use the batch file:**
```bash
run_analysis.bat
```

**Output:**
- `cluster_analysis.png` - Visualizations of discovered clusters
- `temporal_analysis.png` - Time patterns and metrics
- `tickets_with_clusters.csv` - Original data + cluster assignments
- Console output with key insights

---

### Step 3: View Results

Open the PNG files in your image viewer:
- `cluster_analysis.png` - See the discovered patterns
- `temporal_analysis.png` - See time trends

Check the console for insights like:
- Slowest cluster to resolve
- Peak hours for ticket volume
- High-priority hotspots
- Customer satisfaction by cluster
- Volume trends over time

---

## What the Analysis Shows

### Unsupervised Discovery
The algorithm automatically found **9 distinct patterns** in the tickets without any manual labeling!

**Example clusters discovered:**
- Cluster 1: Login/authentication issues
- Cluster 2: Password reset problems
- Cluster 4: Payment errors
- Cluster 7: Mobile app bugs
- Cluster 8: Subscription failures

### Actionable Insights
- **Slowest cluster**: Identifies which types take longest to resolve
- **Peak hours**: Shows when to staff more agents
- **Problem clusters**: Highlights low satisfaction areas
- **Trends**: Shows if volume is increasing/decreasing

---

## Next Steps

1. **Try with real data**: Replace `support_tickets.csv` with your own CSV
2. **Adjust parameters**: Edit `analyze_tickets.py` to change cluster count
3. **Add features**: Include custom fields from your tickets
4. **Build classifier**: Use discovered clusters to train auto-routing

---

## Troubleshooting

**If you see threading errors:**
- Use `run_analysis.bat` instead of direct Python
- Or upgrade: `pip install --upgrade threadpoolctl scikit-learn`

**If plots don't show:**
- They're saved as PNG files automatically
- Just open them in Windows Photo Viewer

---

**Questions?** Check `README.md` for full documentation.
