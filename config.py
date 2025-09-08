# Path to the tshark executable.
# If tshark is in your system PATH, you can just use "tshark".
# Otherwise, provide the full path, e.g.: "C:\\Program Files\\Wireshark\\tshark.exe"
TSHARK_PATH = "tshark"

# Wireshark display filter to select which packets to process.
# Adjust this to change which packets are included in the output.
TSHARK_DISPLAY_FILTER = 'ip && (ip.geoip.src_country || ip.geoip.dst_country)'

# List of fields to extract from each packet.
# Each string must match a valid tshark field name.
TSHARK_FIELDS = [
    "ip.src",                 # Source IP address
    "ip.dst",                 # Destination IP address
    "ip.geoip.src_country",   # Source country (based on GeoIP)
    "ip.geoip.dst_country",   # Destination country (based on GeoIP)
    "ip.geoip.src_lat",       # Source latitude (GeoIP)
    "ip.geoip.src_lon",       # Source longitude (GeoIP)
    "ip.geoip.dst_lat",       # Destination latitude (GeoIP)
    "ip.geoip.dst_lon"        # Destination longitude (GeoIP)
]