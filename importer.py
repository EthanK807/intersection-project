import osmnx as ox
import pandas as pd
from db_config import get_db_engine # Import our shared connection tool

def import_city_to_sql(city_name):
    # 1. Download the data
    print(f"Downloading {city_name}...")
    G = ox.graph_from_place(city_name, network_type="drive")
    
    # 2. Convert to tables
    nodes, edges = ox.graph_to_gdfs(G)
    
    # 3. Clean Nodes
    # We strip out the geometry object and just keep lat/lon
    nodes['latitude'] = nodes.geometry.y
    nodes['longitude'] = nodes.geometry.x
    nodes['node_id'] = nodes.index
    
    # Select specific columns
    nodes_clean = nodes[['node_id', 'latitude', 'longitude', 'street_count']]
    
    # 4. Clean Edges
    # Convert the complex curve object (LineString) into text (WKT)
    edges['geometry_wkt'] = edges['geometry'].apply(lambda x: x.wkt if x else None)
    
    # Handle missing values (NaN) with defaults
    edges['maxspeed'] = edges['maxspeed'].fillna('25 mph').astype(str)
    edges['lanes'] = edges['lanes'].fillna('1').astype(str)
    edges['name'] = edges['name'].fillna('Unnamed').astype(str)

    # 5. Fix Lists (OSM sometimes gives lists for names, we need strings)
    def clean_val(val):
        return ", ".join([str(v) for v in val]) if isinstance(val, list) else str(val)
    
    edges['name'] = edges['name'].apply(clean_val)
    edges['maxspeed'] = edges['maxspeed'].apply(clean_val)
    
    # Rename columns to match your SQL schema
    edges_clean = edges.reset_index()[['u', 'v', 'name', 'maxspeed', 'lanes', 'length', 'geometry_wkt']]
    edges_clean.rename(columns={'u': 'u_node', 'v': 'v_node', 'length': 'length_meters'}, inplace=True)

    # 6. Send to SQL
    engine = get_db_engine()
    # 'replace' drops the old table and makes a new one automatically
    nodes_clean.to_sql('intersections', engine, if_exists='replace', index=False)
    edges_clean.to_sql('streets', engine, if_exists='replace', index=False)
    print("Import complete.")