import osmnx as ox
import pandas as pd

# --- CONFIGURATION TO SHOW ALL DATA ---
# This prevents Python from hiding columns with "..."
pd.set_option('display.max_columns', None) 
# This ensures up to 100 rows are printed
pd.set_option('display.max_rows', 100)
# This prevents text inside a cell from being cut off
pd.set_option('display.max_colwidth', None)
# This makes the output wrap so you can read wide tables
pd.set_option('display.width', 1000)

def view_raw_data():
    print("Downloading data (this might take a moment)...")
    # We use a small query area to keep it fast, or use your city
    G = ox.graph_from_place("Danbury, Connecticut, USA", network_type="drive")
    
    # Convert to tables (This is the raw, uncleaned step)
    nodes, edges = ox.graph_to_gdfs(G)

    print("\n" + "="*50)
    print(f"RAW NODES TABLE (First 100 of {len(nodes)})")
    print("="*50)
    print(nodes.head(100))

    print("\n" + "="*50)
    print(f"RAW EDGES TABLE (First 100 of {len(edges)})")
    print("="*50)
    # columns usually include: osmid, name, highway, oneway, length, geometry...
    print(edges.head(100))

    # --- PRO TIP: EXPORT TO CSV ---
    # It is often MUCH easier to view this in Excel/Google Sheets
    # because the console wraps text and makes it hard to read.
    print("\n" + "="*50)
    print("Exporting to CSV for easier viewing in Excel...")
    
    # We must convert geometry to string temporarily to save to CSV
    # (Pandas can't save the shape objects directly to CSV easily)
    nodes.to_csv("debug_nodes_raw.csv")
    edges.to_csv("debug_edges_raw.csv")
    print("Done. Check your folder for 'debug_nodes_raw.csv' and 'debug_edges_raw.csv'")

if __name__ == "__main__":
    view_raw_data()