# Network Map

This project maps source and destination GeoIP data from Wireshark packet captures onto an interactive world map using Folium.

It filters out broadcast, multicast, and anycast traffic, keeping only unicast connections.

![firefox_SfZFW7xQEh](https://github.com/user-attachments/assets/3ac5b23c-4687-4649-aaac-dd1ab5769ca0)

# Quick Start
1. Capture network traffic in Wireshark and save as ```.pcapng```.

2. Place the file into the ```pcaps/``` folder.

3. Run the program:
	```
	py main.py
	```
4. Select your capture when prompted.

5. The script will write a CSV and an ```.html``` map into the ```outputs/``` folder.

6. Open the ```.html``` file in a browser to view the interactive world map.

# Configuration

The only current configuration supported is changing the location of the destination IP (your local ip capture).
To do so, you need to edit this variable in ```config.py```:

```
# Dummy coords for local ips
# Add a location of your choice to represent your home traffic in (latitude, longitude)
local = (45.4,-75.7)
```

# Requirements

-  Windows
-  Python: https://www.python.org/downloads/
-  Wireshark: https://www.wireshark.org/download.html
    -  Used to capture traffic into ```.pcapng files.``` Place captures in the ```network-map/pcaps/``` folder.
-  MaxMind GeoIP: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/
    -  Requires a free account to download. You will receive a ```.zip``` containing:
        -  ```GeoLite2-ASN.mmdb```
        -  ```GeoLite2-City.mmdb```
        -  ```GeoLite2-Country.mmdb```
-  Folium: install with
	```
	pip install folium
	```

# Installation

### Step 1: Download the project

-  On the main branch, click the green "Code" button and choose "Download ZIP".

-  Extract the archive anywhere on your system.

### Step 2: Configure Wireshark with MaxMind databases

-  Download and install Wireshark.

-  Download the MaxMind GeoIP databases (requires creating a free account).

-  Place the three ```.mmdb``` files into one of Wireshark’s default database directories:

    - ```C:\ProgramData\GeoIP```

    - ```C:\GeoIP```

-  Open Wireshark, go to Edit → Preferences → Name Resolution.

-  Enable the checkbox "Enable IP geolocation".

-  At this point Wireshark should resolve IPs into geolocation data.

### Step 3: Run the program

-  Place your ```.pcapng``` capture file into the ```pcaps/``` folder.

-  Open PowerShell and navigate to your project directory, for example:
	```
	PS C:\Users\YourName> F:
	PS F:> cd "F:\Projects\networkMap"
	```
- If you haven't downloaded folium yet, now is the time to do so:
	```
	pip install folium
	```
- Run the script:
	```
	py main.py
	```

- Choose a ```.pcapng``` file when prompted:

	```
	Select a .pcapng file to process:
	1: example.pcapng
	2: test1.pcapng
	Enter a number: 1
	```

-  The script will:

    -  Run tshark with GeoIP fields enabled

    -  Write a deduplicated CSV into the ```outputs/``` folder

    -  Generate a Folium world map and save it as an ```.html``` file in ```outputs/```

-  Example output:
	```
	Done! Wrote deduplicated CSV to outputs\example.csv
	Plotted 6 nodes and 28 lines
	Map saved to outputs\example.html
	```

-  Open the ```.html``` file in a browser to view your interactive map.






