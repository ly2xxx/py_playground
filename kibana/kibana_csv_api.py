"""
Kibana CSV Download - Approach 1: Kibana Reporting API
Uses the Kibana API directly to generate CSV reports without UI interaction.

This is the most robust approach as it bypasses the UI entirely.
Requires authentication if your Kibana instance is secured.
"""

import requests
import time
from pathlib import Path

def download_csv_via_api(
    kibana_url="https://demo.elastic.co",
    index_pattern="kibana_sample_data_*",  # Adjust to your index
    query="*",
    output_dir="./downloads"
):
    """
    Download CSV from Kibana using the Reporting API.
    
    Note: The demo.elastic.co site may not expose the API publicly.
    This approach works best with your own Kibana instance.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Kibana Reporting API endpoint
    # For CSV from saved search: POST /api/reporting/generate/csv_searchsource
    # For CSV from dashboard panel: POST /api/reporting/generate/csv
    
    api_endpoint = f"{kibana_url}/api/reporting/generate/csv_searchsource"
    
    # Headers - Kibana requires these
    headers = {
        "kbn-xsrf": "true",  # Required for Kibana API calls
        "Content-Type": "application/json",
    }
    
    # Request body - defines what to export
    # This is a simplified example; actual structure depends on your data
    payload = {
        "browserTimezone": "UTC",
        "objectType": "search",
        "searchSource": {
            "type": "search",
            "query": {
                "query": query,
                "language": "kuery"
            },
            "index": index_pattern,
            "filter": []
        },
        "columns": [],  # Empty = all columns
        "title": "Exported Data"
    }
    
    print("🚀 Kibana Reporting API Approach")
    print("=" * 50)
    print(f"📊 Target: {kibana_url}")
    print(f"📋 Index: {index_pattern}")
    
    try:
        # Step 1: Request report generation
        print("\n⏳ Requesting CSV report generation...")
        response = requests.post(api_endpoint, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            job_path = result.get("path")
            print(f"✅ Report job created: {job_path}")
            
            # Step 2: Poll for completion
            print("⏳ Waiting for report to complete...")
            download_url = f"{kibana_url}{job_path}"
            
            for attempt in range(30):  # Max 30 attempts (5 minutes)
                time.sleep(10)  # Check every 10 seconds
                
                status_response = requests.get(download_url, headers=headers)
                if status_response.status_code == 200:
                    # Report ready - download it
                    content_type = status_response.headers.get("Content-Type", "")
                    if "text/csv" in content_type or "application/csv" in content_type:
                        filename = output_path / "kibana_export.csv"
                        with open(filename, "wb") as f:
                            f.write(status_response.content)
                        print(f"✅ Downloaded to: {filename}")
                        print(f"📊 Size: {filename.stat().st_size} bytes")
                        return str(filename)
                    
                print(f"   Attempt {attempt + 1}/30 - still processing...")
            
            print("❌ Timeout waiting for report")
            
        elif response.status_code == 401:
            print("❌ Authentication required. Please provide credentials.")
            print("   For secured Kibana, add 'auth' parameter to requests.")
            
        elif response.status_code == 403:
            print("❌ Access forbidden. Check your permissions.")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Kibana.")
        print("   Ensure the URL is correct and accessible.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None


def download_csv_via_elasticsearch(
    es_url="https://demo.elastic.co:9243",  # Elasticsearch endpoint
    index="kibana_sample_data_logs",
    query={"match_all": {}},
    output_dir="./downloads",
    max_rows=10000
):
    """
    Alternative: Query Elasticsearch directly and convert to CSV.
    Bypasses Kibana entirely.
    """
    import json
    import csv
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("\n🔍 Direct Elasticsearch Query Approach")
    print("=" * 50)
    
    # Elasticsearch search endpoint
    search_url = f"{es_url}/{index}/_search"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "query": query,
        "size": max_rows
    }
    
    try:
        print(f"📊 Querying: {index}")
        response = requests.get(search_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            hits = data.get("hits", {}).get("hits", [])
            
            if hits:
                # Extract field names from first hit
                first_doc = hits[0].get("_source", {})
                fieldnames = list(first_doc.keys())
                
                # Write to CSV
                filename = output_path / f"{index}_export.csv"
                with open(filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for hit in hits:
                        writer.writerow(hit.get("_source", {}))
                
                print(f"✅ Exported {len(hits)} rows to: {filename}")
                return str(filename)
            else:
                print("⚠️ No data found in index.")
                
        else:
            print(f"❌ Elasticsearch error: {response.status_code}")
            print(f"   {response.text[:300]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None


if __name__ == "__main__":
    print("=" * 60)
    print("Kibana CSV Export - API Approach")
    print("=" * 60)
    print()
    print("⚠️  Note: The demo.elastic.co site may not expose APIs publicly.")
    print("    This approach works best with your own Kibana/ES instance.")
    print()
    
    # Try the Kibana Reporting API
    result = download_csv_via_api()
    
    if not result:
        print("\n" + "-" * 50)
        print("Trying direct Elasticsearch query as fallback...")
        result = download_csv_via_elasticsearch()
    
    print("\n" + "=" * 60)
    print("Done!")
