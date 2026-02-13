"""
Unsupervised ML analysis of customer support tickets
Demonstrates clustering, topic modeling, and pattern discovery
"""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_data(filepath="support_tickets.csv"):
    """Load ticket data"""
    df = pd.read_csv(filepath)
    df['created_at'] = pd.to_datetime(df['created_at'])
    print(f"[OK] Loaded {len(df)} tickets")
    return df

def text_clustering(df, n_clusters=5):
    """Cluster tickets based on conversation text"""
    print("\n[CLUSTERING] Performing text-based clustering...")
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        max_features=100,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    X = vectorizer.fit_transform(df['conversation'])
    
    # Try different cluster numbers and find optimal
    silhouette_scores = []
    K_range = range(3, 10)
    
    for k in K_range:
        kmeans = MiniBatchKMeans(n_clusters=k, random_state=42, n_init=10, batch_size=100)
        labels = kmeans.fit_predict(X)
        score = silhouette_score(X, labels)
        silhouette_scores.append(score)
    
    # Use optimal k
    optimal_k = K_range[np.argmax(silhouette_scores)]
    print(f"[RESULT] Optimal number of clusters: {optimal_k}")
    
    # Final clustering
    kmeans = MiniBatchKMeans(n_clusters=optimal_k, random_state=42, n_init=10, batch_size=100)
    df['text_cluster'] = kmeans.fit_predict(X)
    
    # Get top terms per cluster
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    print("\n[PATTERNS] Discovered Patterns (Top Keywords per Cluster):")
    cluster_names = []
    for i in range(optimal_k):
        top_terms = [terms[ind] for ind in order_centroids[i, :5]]
        cluster_name = " + ".join(top_terms[:2])
        cluster_names.append(cluster_name)
        print(f"  Cluster {i}: {', '.join(top_terms)}")
    
    return df, silhouette_scores, cluster_names

def visualize_clusters(df, cluster_names):
    """Visualize clusters with PCA"""
    print("\n[VISUAL] Creating visualizations...")
    
    # Prepare features for PCA
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    X = vectorizer.fit_transform(df['conversation'])
    
    # PCA for 2D visualization
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X.toarray())
    
    df['pca_x'] = coords[:, 0]
    df['pca_y'] = coords[:, 1]
    
    # Plot 1: Cluster visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Scatter plot by cluster
    scatter = axes[0, 0].scatter(
        df['pca_x'], 
        df['pca_y'], 
        c=df['text_cluster'], 
        cmap='viridis',
        alpha=0.6,
        s=50
    )
    axes[0, 0].set_title('Discovered Ticket Clusters (Unsupervised)', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('PCA Component 1')
    axes[0, 0].set_ylabel('PCA Component 2')
    plt.colorbar(scatter, ax=axes[0, 0], label='Cluster')
    
    # Scatter plot by actual topic (ground truth)
    topic_colors = {topic: i for i, topic in enumerate(df['topic'].unique())}
    colors = df['topic'].map(topic_colors)
    scatter2 = axes[0, 1].scatter(
        df['pca_x'], 
        df['pca_y'], 
        c=colors, 
        cmap='tab10',
        alpha=0.6,
        s=50
    )
    axes[0, 1].set_title('Actual Topics (Ground Truth)', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('PCA Component 1')
    axes[0, 1].set_ylabel('PCA Component 2')
    
    # Cluster size distribution
    cluster_counts = df['text_cluster'].value_counts().sort_index()
    axes[1, 0].bar(range(len(cluster_counts)), cluster_counts.values, color='steelblue')
    axes[1, 0].set_title('Tickets per Discovered Cluster', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Cluster ID')
    axes[1, 0].set_ylabel('Number of Tickets')
    axes[1, 0].set_xticks(range(len(cluster_counts)))
    
    # Priority distribution by cluster
    priority_by_cluster = pd.crosstab(df['text_cluster'], df['priority'], normalize='index')
    priority_by_cluster.plot(kind='bar', stacked=True, ax=axes[1, 1], colormap='RdYlGn_r')
    axes[1, 1].set_title('Priority Distribution by Cluster', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Cluster ID')
    axes[1, 1].set_ylabel('Proportion')
    axes[1, 1].legend(title='Priority', bbox_to_anchor=(1.05, 1))
    axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=0)
    
    plt.tight_layout()
    plt.savefig('cluster_analysis.png', dpi=300, bbox_inches='tight')
    print("  [OK] Saved: cluster_analysis.png")
    
    # Plot 2: Time-based patterns
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # Tickets over time
    df['date'] = df['created_at'].dt.date
    daily_counts = df.groupby('date').size()
    axes[0, 0].plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2)
    axes[0, 0].set_title('Ticket Volume Over Time', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Number of Tickets')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(alpha=0.3)
    
    # Hourly pattern
    df['hour'] = df['created_at'].dt.hour
    hourly_counts = df.groupby('hour').size()
    axes[0, 1].bar(hourly_counts.index, hourly_counts.values, color='coral')
    axes[0, 1].set_title('Tickets by Hour of Day', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Hour')
    axes[0, 1].set_ylabel('Number of Tickets')
    axes[0, 1].grid(alpha=0.3)
    
    # Resolution time by cluster
    resolved = df[df['resolution_time_hours'].notna()]
    if len(resolved) > 0:
        resolved.boxplot(column='resolution_time_hours', by='text_cluster', ax=axes[1, 0])
        axes[1, 0].set_title('Resolution Time by Cluster', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Cluster ID')
        axes[1, 0].set_ylabel('Resolution Time (hours)')
        plt.sca(axes[1, 0])
        plt.xticks(rotation=0)
    
    # Customer satisfaction by cluster
    satisfied = df[df['customer_satisfaction'].notna()]
    if len(satisfied) > 0:
        satisfaction_by_cluster = satisfied.groupby('text_cluster')['customer_satisfaction'].mean()
        axes[1, 1].bar(satisfaction_by_cluster.index, satisfaction_by_cluster.values, color='gold')
        axes[1, 1].set_title('Avg Customer Satisfaction by Cluster', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Cluster ID')
        axes[1, 1].set_ylabel('Satisfaction (1-5)')
        axes[1, 1].set_ylim(0, 5)
        axes[1, 1].axhline(y=3, color='r', linestyle='--', alpha=0.5, label='Neutral')
        axes[1, 1].legend()
        axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('temporal_analysis.png', dpi=300, bbox_inches='tight')
    print("  [OK] Saved: temporal_analysis.png")

def generate_insights(df):
    """Generate actionable insights"""
    print("\n[INSIGHTS] KEY INSIGHTS DISCOVERED:")
    print("=" * 60)
    
    # 1. Most problematic cluster
    if 'resolution_time_hours' in df.columns:
        resolved = df[df['resolution_time_hours'].notna()]
        if len(resolved) > 0:
            avg_resolution = resolved.groupby('text_cluster')['resolution_time_hours'].mean()
            slowest_cluster = avg_resolution.idxmax()
            print(f"\n1. [SLOW] SLOWEST CLUSTER: Cluster {slowest_cluster}")
            print(f"   Average resolution time: {avg_resolution[slowest_cluster]:.1f} hours")
            print(f"   Sample tickets:")
            samples = df[df['text_cluster'] == slowest_cluster]['conversation'].head(3)
            for i, sample in enumerate(samples, 1):
                print(f"   - {sample[:80]}...")
    
    # 2. Peak times
    df['hour'] = df['created_at'].dt.hour
    peak_hour = df['hour'].mode()[0]
    peak_count = (df['hour'] == peak_hour).sum()
    print(f"\n2. [PEAK] PEAK HOUR: {peak_hour}:00")
    print(f"   {peak_count} tickets ({peak_count/len(df)*100:.1f}% of daily volume)")
    
    # 3. High-priority patterns
    high_priority = df[df['priority'].isin(['High', 'Critical'])]
    if len(high_priority) > 0:
        common_cluster = high_priority['text_cluster'].mode()[0]
        print(f"\n3. [URGENT] HIGH-PRIORITY HOTSPOT: Cluster {common_cluster}")
        print(f"   {len(high_priority[high_priority['text_cluster']==common_cluster])} critical tickets")
    
    # 4. Satisfaction patterns
    if 'customer_satisfaction' in df.columns:
        satisfied = df[df['customer_satisfaction'].notna()]
        if len(satisfied) > 0:
            low_sat = satisfied[satisfied['customer_satisfaction'] <= 2]
            if len(low_sat) > 0:
                worst_cluster = low_sat['text_cluster'].mode()[0]
                print(f"\n4. [SAT] LOWEST SATISFACTION: Cluster {worst_cluster}")
                print(f"   Average rating: {satisfied[satisfied['text_cluster']==worst_cluster]['customer_satisfaction'].mean():.2f}/5")
    
    # 5. Volume trends
    df['date'] = df['created_at'].dt.date
    daily_counts = df.groupby('date').size()
    trend = "increasing" if daily_counts.iloc[-1] > daily_counts.iloc[0] else "decreasing"
    print(f"\n5. [TREND] VOLUME TREND: {trend.upper()}")
    print(f"   Day 1: {daily_counts.iloc[0]} tickets -> Day 5: {daily_counts.iloc[-1]} tickets")
    
    print("\n" + "=" * 60)

def main():
    """Run complete analysis"""
    print("=" * 60)
    print("Customer Support Ticket Analysis - POC")
    print("=" * 60)
    
    # Load data
    df = load_data()
    
    # Perform clustering
    df, silhouette_scores, cluster_names = text_clustering(df)
    
    # Visualize
    visualize_clusters(df, cluster_names)
    
    # Generate insights
    generate_insights(df)
    
    # Save enriched dataset
    df.to_csv('tickets_with_clusters.csv', index=False)
    print(f"\n[OK] Saved enriched dataset: tickets_with_clusters.csv")
    
    print("\n" + "=" * 60)
    print("[DONE] Analysis complete! Check the generated PNG files.")
    print("=" * 60)

if __name__ == "__main__":
    main()
