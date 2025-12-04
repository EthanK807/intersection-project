import osmnx as ox
import pandas as pd
from db_config import get_db_engine # Import our shared connection tool

def fill_missing_speeds(row):
# If we already have a speed keep it
    if pd.notna(row['maxspeed']):
        return row['maxspeed']
    
    # Otherwise, look at the highway type to guess the speed
    highway_type = str(row['highway'])
    
    if 'motorway' in highway_type or 'trunk' in highway_type:
        return '65 mph'
    elif 'primary' in highway_type or 'secondary' in highway_type:
        return '45 mph'
    elif 'tertiary' in highway_type:
        return '35 mph'
    elif 'residential' in highway_type or 'living_street' in highway_type:
        return '25 mph'
    else:
        # In case weird roads like unclassified or service roads
        return '30 mph'


def import_city_to_sql(city_name):

    # 1. Download the data
    print(f"Downloading {city_name}...")
    G = ox.graph_from_place(city_name, network_type="drive")
    
    # 2. Convert to tables
    nodes, edges = ox.graph_to_gdfs(G)
    
    # 3. Clean Nodes
    nodes['node_id'] = nodes.osmid
    
    # Select specific columns
    nodes_clean = nodes[['node_id', 'x', 'y', 'street_count', 'highway']]
    
    # 4. Clean Edges
    # Convert the complex curve object (LineString) into text (WKT)
    edges['geometry_wkt'] = edges['geometry'].apply(lambda x: x.wkt if x else None)
    edges['maxspeed'] = edges.apply(fill_missing_speeds, axis=1)
    
    # Handle missing values (NaN) with defaults
    edges['lanes'] = edges['lanes'].fillna('1').astype(str)
    edges['name'] = edges['name'].fillna('Unnamed').astype(str)

    # 5. Fix Lists (OSM sometimes gives lists for names, we need strings)
    def clean_val(val):
        return ", ".join([str(v) for v in val]) if isinstance(val, list) else str(val)
    
    edges['name'] = edges['name'].apply(clean_val)
    edges['maxspeed'] = edges['maxspeed'].apply(clean_val)
    edges['osmid'] = edges['osmid'].apply(clean_val)
    edges['name'] = edges['name'].apply(clean_val)

    
    # Rename columns to match your SQL schema
    edges_clean = edges.reset_index()[['u', 'v', 'name', 'maxspeed', 'lanes', 'length', 'geometry_wkt']]
    edges_clean.rename(columns={'u': 'u_node', 'v': 'v_node', 'length': 'length_meters'}, inplace=True)

    # 6. Send to SQL
    engine = get_db_engine()
    # 'replace' drops the old table and makes a new one automatically
    nodes_clean.to_sql('intersections', engine, if_exists='replace', index=False)
    edges_clean.to_sql('streets', engine, if_exists='replace', index=False)
    print("Import complete.")