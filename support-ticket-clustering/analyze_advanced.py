"""
Phase 2: Advanced Ticket Clustering with Sentence Transformers & BERTopic
Uses state-of-the-art NLP to discover patterns from minimal data
"""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Advanced NLP libraries
from sentence_transformers import SentenceTransformer
from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score
import umap.umap_ as umap

# BERTopic
try:
    from bertopic import BERTopic
    BERTOPIC_AVAILABLE = True
except ImportError:
    BERTOPIC_AVAILABLE = False
    print("[WARNING] BERTopic not installed. Install with: pip install bertopic")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

def load_data(filepath="support_tickets_advanced.csv"):
    """Load minimal ticket data"""
    df = pd.read_csv(filepath)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%d/%m/%Y %H:%M')
    print(f"[OK] Loaded {len(df)} tickets with {len(df.columns)} columns")
    print(f"[INFO] Columns: {', '.join(df.columns.tolist())}")
    return df

def generate_embeddings(texts, model_name='all-MiniLM-L6-v2'):
    """
    Generate semantic embeddings using Sentence Transformers
    all-MiniLM-L6-v2: Fast, 384-dim, good for short texts
    """
    print(f"\n[EMBED] Generating embeddings with {model_name}...")
    print(f"[INFO] Model will download on first run (~90MB)")
    
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True)
    
    print(f"[OK] Generated {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}")
    return embeddings

def cluster_hdbscan(embeddings, min_cluster_size=3):
    """
    HDBSCAN: Density-based clustering that finds arbitrary shapes
    Automatically determines number of clusters
    """
    print(f"\n[CLUSTER] Running HDBSCAN (min_cluster_size={min_cluster_size})...")
    
    clusterer = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=2,
        metric='euclidean',
        cluster_selection_method='eom'
    )
    
    labels = clusterer.fit_predict(embeddings)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    print(f"[RESULT] Discovered {n_clusters} clusters")
    print(f"[INFO] Noise points (unclustered): {n_noise}")
    
    if n_clusters > 1:
        # Only calculate silhouette if we have multiple clusters and not all noise
        valid_mask = labels != -1
        if valid_mask.sum() > 1:
            score = silhouette_score(embeddings[valid_mask], labels[valid_mask])
            print(f"[METRIC] Silhouette score: {score:.3f}")
    
    return labels

def reduce_dimensions(embeddings, n_components=2):
    """
    UMAP: Better than PCA for preserving local structure
    """
    print(f"\n[REDUCE] Reducing to {n_components}D with UMAP...")
    
    reducer = umap.UMAP(
        n_components=n_components,
        n_neighbors=15,
        min_dist=0.1,
        metric='cosine',
        random_state=42
    )
    
    reduced = reducer.fit_transform(embeddings)
    print(f"[OK] Reduced from {embeddings.shape[1]}D to {n_components}D")
    
    return reduced

def bertopic_modeling(texts, embeddings):
    """
    BERTopic: Automatic topic modeling with coherent labels
    """
    if not BERTOPIC_AVAILABLE:
        return None, None
    
    print(f"\n[TOPIC] Running BERTopic modeling...")
    
    topic_model = BERTopic(
        language="english",
        calculate_probabilities=False,
        verbose=False
    )
    
    topics, probs = topic_model.fit_transform(texts, embeddings)
    
    n_topics = len(set(topics)) - (1 if -1 in topics else 0)
    print(f"[RESULT] Discovered {n_topics} topics")
    
    # Get topic info
    topic_info = topic_model.get_topic_info()
    print(f"\n[TOPICS] Top discovered topics:")
    for idx, row in topic_info.head(6).iterrows():
        if row['Topic'] != -1:
            print(f"  Topic {row['Topic']}: {row['Count']} tickets - {row['Name'][:60]}")
    
    return topic_model, topics

def visualize_advanced(df, embeddings_2d, clusters, topics=None):
    """Create advanced visualizations"""
    print("\n[VISUAL] Creating advanced visualizations...")
    
    df['cluster'] = clusters
    df['x'] = embeddings_2d[:, 0]
    df['y'] = embeddings_2d[:, 1]
    if topics is not None:
        df['topic'] = topics
    
    # Figure 1: Cluster + Topic Analysis
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # Plot 1: HDBSCAN Clusters
    scatter1 = axes[0, 0].scatter(
        df['x'], df['y'],
        c=df['cluster'],
        cmap='tab20',
        alpha=0.6,
        s=100,
        edgecolors='black',
        linewidth=0.5
    )
    axes[0, 0].set_title('HDBSCAN Clusters (Density-Based)', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('UMAP Dimension 1')
    axes[0, 0].set_ylabel('UMAP Dimension 2')
    plt.colorbar(scatter1, ax=axes[0, 0], label='Cluster ID')
    
    # Add noise annotation
    n_noise = (df['cluster'] == -1).sum()
    axes[0, 0].text(0.02, 0.98, f"Noise points: {n_noise}", 
                    transform=axes[0, 0].transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: BERTopic Topics (if available)
    if topics is not None:
        scatter2 = axes[0, 1].scatter(
            df['x'], df['y'],
            c=df['topic'],
            cmap='viridis',
            alpha=0.6,
            s=100,
            edgecolors='black',
            linewidth=0.5
        )
        axes[0, 1].set_title('BERTopic Topics (Semantic)', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('UMAP Dimension 1')
        axes[0, 1].set_ylabel('UMAP Dimension 2')
        plt.colorbar(scatter2, ax=axes[0, 1], label='Topic ID')
    else:
        axes[0, 1].text(0.5, 0.5, 'BERTopic not available\npip install bertopic',
                       ha='center', va='center', fontsize=12,
                       transform=axes[0, 1].transAxes)
        axes[0, 1].set_title('BERTopic Topics (Not Installed)', fontsize=14)
    
    # Plot 3: Cluster sizes
    cluster_counts = df[df['cluster'] != -1]['cluster'].value_counts().sort_index()
    if len(cluster_counts) > 0:
        axes[1, 0].bar(cluster_counts.index, cluster_counts.values, color='steelblue', edgecolor='black')
        axes[1, 0].set_title('Tickets per Cluster', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Cluster ID')
        axes[1, 0].set_ylabel('Number of Tickets')
        axes[1, 0].grid(alpha=0.3)
    
    # Plot 4: Time distribution by cluster
    df['date'] = df['created_at'].dt.date
    df['hour'] = df['created_at'].dt.hour
    
    valid_clusters = df[df['cluster'] != -1]
    if len(valid_clusters) > 0:
        hourly_cluster = valid_clusters.pivot_table(
            index='hour',
            columns='cluster',
            values='ticket_id',
            aggfunc='count',
            fill_value=0
        )
        hourly_cluster.plot(kind='area', stacked=True, ax=axes[1, 1], alpha=0.7, colormap='tab20')
        axes[1, 1].set_title('Cluster Distribution by Hour', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Hour of Day')
        axes[1, 1].set_ylabel('Number of Tickets')
        axes[1, 1].legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('advanced_clustering.png', dpi=300, bbox_inches='tight')
    print("  [OK] Saved: advanced_clustering.png")
    
    # Figure 2: Temporal patterns
    fig2, axes2 = plt.subplots(2, 2, figsize=(16, 10))
    
    # Daily volume
    daily = df.groupby('date').size()
    axes2[0, 0].plot(daily.index, daily.values, marker='o', linewidth=2, markersize=8)
    axes2[0, 0].set_title('Daily Ticket Volume', fontsize=14, fontweight='bold')
    axes2[0, 0].set_xlabel('Date')
    axes2[0, 0].set_ylabel('Tickets')
    axes2[0, 0].grid(alpha=0.3)
    axes2[0, 0].tick_params(axis='x', rotation=45)
    
    # Hourly pattern
    hourly = df.groupby('hour').size()
    axes2[0, 1].bar(hourly.index, hourly.values, color='coral', edgecolor='black')
    axes2[0, 1].set_title('Hourly Distribution', fontsize=14, fontweight='bold')
    axes2[0, 1].set_xlabel('Hour of Day')
    axes2[0, 1].set_ylabel('Tickets')
    axes2[0, 1].grid(alpha=0.3)
    
    # Cluster evolution over time
    if len(valid_clusters) > 0:
        cluster_daily = valid_clusters.pivot_table(
            index='date',
            columns='cluster',
            values='ticket_id',
            aggfunc='count',
            fill_value=0
        )
        cluster_daily.plot(kind='line', ax=axes2[1, 0], marker='o', linewidth=2)
        axes2[1, 0].set_title('Cluster Trends Over Time', fontsize=14, fontweight='bold')
        axes2[1, 0].set_xlabel('Date')
        axes2[1, 0].set_ylabel('Tickets')
        axes2[1, 0].legend(title='Cluster', bbox_to_anchor=(1.05, 1))
        axes2[1, 0].grid(alpha=0.3)
        axes2[1, 0].tick_params(axis='x', rotation=45)
    
    # Text length distribution by cluster
    df['text_length'] = df['conversation'].str.len()
    if len(valid_clusters) > 0:
        df[df['cluster'] != -1].boxplot(column='text_length', by='cluster', ax=axes2[1, 1])
        axes2[1, 1].set_title('Text Length by Cluster', fontsize=14, fontweight='bold')
        axes2[1, 1].set_xlabel('Cluster ID')
        axes2[1, 1].set_ylabel('Character Count')
        axes2[1, 1].get_figure().suptitle('')  # Remove auto-title
        axes2[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('temporal_advanced.png', dpi=300, bbox_inches='tight')
    print("  [OK] Saved: temporal_advanced.png")

def generate_insights(df, topic_model=None):
    """Generate insights from advanced clustering"""
    print("\n" + "="*70)
    print("[INSIGHTS] ADVANCED CLUSTERING DISCOVERIES")
    print("="*70)
    
    valid_clusters = df[df['cluster'] != -1]
    
    if len(valid_clusters) == 0:
        print("\n[WARNING] No clusters found - all tickets classified as noise")
        print("[TIP] Try collecting more data or reducing min_cluster_size")
        return
    
    # 1. Cluster characteristics
    print("\n1. [CLUSTERS] Discovered Patterns:")
    for cluster_id in sorted(valid_clusters['cluster'].unique()):
        cluster_tickets = valid_clusters[valid_clusters['cluster'] == cluster_id]
        print(f"\n   Cluster {cluster_id}: {len(cluster_tickets)} tickets")
        print(f"   Sample conversations:")
        for conv in cluster_tickets['conversation'].head(3):
            print(f"   - {conv[:70]}...")
    
    # 2. Temporal insights
    print(f"\n2. [TIME] Temporal Patterns:")
    peak_hour = df['hour'].mode()[0]
    peak_count = (df['hour'] == peak_hour).sum()
    print(f"   Peak hour: {peak_hour}:00 ({peak_count} tickets)")
    
    df['date'] = df['created_at'].dt.date
    daily = df.groupby('date').size()
    print(f"   Date range: {daily.index.min()} to {daily.index.max()}")
    print(f"   Daily avg: {daily.mean():.1f} tickets")
    
    # 3. Cluster stability
    if len(valid_clusters) > 1:
        cluster_spread = valid_clusters.groupby('cluster')['date'].apply(lambda x: (x.max() - x.min()).days)
        print(f"\n3. [STABILITY] Cluster Persistence:")
        for cluster_id, days in cluster_spread.items():
            print(f"   Cluster {cluster_id}: Active for {days} days")
    
    # 4. Topic insights (if BERTopic available)
    if topic_model is not None and 'topic' in df.columns:
        print(f"\n4. [TOPICS] Semantic Topics Discovered:")
        topic_counts = df[df['topic'] != -1]['topic'].value_counts().head(5)
        for topic_id, count in topic_counts.items():
            print(f"   Topic {topic_id}: {count} tickets")
            try:
                top_words = topic_model.get_topic(topic_id)[:5]
                words = [word for word, score in top_words]
                print(f"   Keywords: {', '.join(words)}")
            except:
                pass
    
    # 5. Recommendations
    print(f"\n5. [NEXT] Recommended Actions:")
    print(f"   - Review Cluster 0 samples for common patterns")
    print(f"   - Schedule more support during peak hour ({peak_hour}:00)")
    if (df['cluster'] == -1).sum() > 0:
        print(f"   - Investigate {(df['cluster'] == -1).sum()} unclustered tickets")
    print(f"   - Build classifier to auto-tag new tickets")
    
    print("\n" + "="*70)

def main():
    """Run Phase 2: Advanced Clustering"""
    print("="*70)
    print("PHASE 2: ADVANCED TICKET CLUSTERING")
    print("Sentence Transformers + HDBSCAN + BERTopic + UMAP")
    print("="*70)
    
    # Load data
    df = load_data("support_tickets_advanced.csv")
    
    # Generate embeddings
    embeddings = generate_embeddings(df['conversation'].tolist())
    
    # Cluster with HDBSCAN
    clusters = cluster_hdbscan(embeddings, min_cluster_size=3)
    
    # Reduce to 2D for visualization
    embeddings_2d = reduce_dimensions(embeddings, n_components=2)
    
    # BERTopic modeling (optional)
    topic_model = None
    topics = None
    if BERTOPIC_AVAILABLE:
        topic_model, topics = bertopic_modeling(df['conversation'].tolist(), embeddings)
    
    # Visualize
    visualize_advanced(df, embeddings_2d, clusters, topics)
    
    # Add to dataframe
    df['cluster'] = clusters
    df['x'] = embeddings_2d[:, 0]
    df['y'] = embeddings_2d[:, 1]
    if topics is not None:
        df['topic'] = topics
    
    # Generate insights
    generate_insights(df, topic_model)
    
    # Save results
    df.to_csv('tickets_advanced_clustered.csv', index=False)
    print(f"\n[OK] Saved enriched dataset: tickets_advanced_clustered.csv")
    
    # Save embeddings for future use
    np.save('embeddings.npy', embeddings)
    print(f"[OK] Saved embeddings: embeddings.npy")
    
    print("\n" + "="*70)
    print("[DONE] Phase 2 complete! Check PNG files for visualizations.")
    print("="*70)

if __name__ == "__main__":
    main()
