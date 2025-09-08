import folium

def read_csv(csv_path):
    
    # Read the CSV file at csv_path and return a list of row dicts.
    # Each row is a dictionary mapping column names to values.

    import csv
    rows = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

def get_lat_lon(row, prefix):
    
    # Extract latitude and longitude for a node (source or destination) from a CSV row.
    # Use fallback coordinates for private/local IPs if missing.
    
    lat_key = f'ip.geoip.{prefix}_lat'
    lon_key = f'ip.geoip.{prefix}_lon'
    ip_key = f'ip.{prefix}'
    try:
        lat = float(row[lat_key]) if row[lat_key] else None
        lon = float(row[lon_key]) if row[lon_key] else None
        if lat is not None and lon is not None:
            return lat, lon
        # Assign dummy coords for local IPs
        ip = row.get(ip_key, "")
        if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172.16.") or ip.startswith("172.31."):
            return (33.0, -63.0)
    except (KeyError, ValueError):
        pass
    return None

def plot_connections(rows, output_html):

     # Plot network connections on a folium map:
     # - Draws a dark blue line for each connection.
     # - Draws a red circle for each node (source or destination).
     # - Tooltip on each node shows its IP and country.
     # - Saves the map to output_html.
      
    latlons = []          # List of all node coordinates
    node_info = dict()    # Maps (lat,lon) to label for tooltip

    # Parse rows to collect node and connection info
    for row in rows:
        src = get_lat_lon(row, "src")
        dst = get_lat_lon(row, "dst")
        src_ip = row.get("ip.src", "")
        dst_ip = row.get("ip.dst", "")
        src_country = row.get("ip.geoip.src_country", "")
        dst_country = row.get("ip.geoip.dst_country", "")
        if src:
            latlons.append(src)
            node_info[src] = f"Source IP: {src_ip} ({src_country})"
        if dst:
            latlons.append(dst)
            node_info[dst] = f"Dest IP: {dst_ip} ({dst_country})"

    # Determine map center as the average of all nodes
    map_center = [0, 0]
    if latlons:
        avg_lat = sum(lat for lat, _ in latlons) / len(latlons)
        avg_lon = sum(lon for _, lon in latlons) / len(latlons)
        map_center = [avg_lat, avg_lon]

    # Create the folium map
    m = folium.Map(location=map_center, zoom_start=2, tiles="OpenStreetMap")

    # Draw all connection lines first (under nodes)
    connection_count = 0
    for row in rows:
        src = get_lat_lon(row, "src")
        dst = get_lat_lon(row, "dst")
        if src and dst:
            folium.PolyLine([src, dst], color="blue", weight=2, opacity=0.7).add_to(m)
            connection_count += 1

    # Draw all nodes as red circles
    for node, label in node_info.items():
        folium.CircleMarker(
            node,
            radius=10,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            tooltip=label  # Tooltip on hover (always available)
        ).add_to(m)

    print(f"Plotted {len(node_info)} nodes and {connection_count} lines")
    m.save(output_html)
    print(f"Map saved to {output_html}")