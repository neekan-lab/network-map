# Network Map

This project maps source and destination GeoIP data taken from Wireshark packet captures using folium.

It filters out any broadcast, multicast or anycast traffic and keeps only the unicast.
![firefox_SfZFW7xQEh](https://github.com/user-attachments/assets/fce8fb9c-6f56-4032-ab05-cb390f49ea1c)

# Requirements

Python (https://www.python.org/downloads/)

Wireshark (https://www.wireshark.org/download.html)
-  To capture your packet traffic to a .pcapng file, these will go into the network-map/pcaps/ folder.

Maxmind's GeoIP (https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/)
-  For this you will need to make an account and sign in to obtain our 3 GeoIP database .mmdb files
  
Folium
-  You can download this with 'pip install folium' in the same powershell you're running the command in.

# Installation

Step 1: Installing the files
-  Ensure you're on the main branch, click the green <> Code button and 'Download ZIP'
-  You can extract this wherever you like

Step 2: Setting up Wireshark with Maxmind's GeoIP database
- Download Wireshark, the link is in the requirements section.

- Download the maxmind's geoip database (https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/)
- You will need to create an account and sign in to do this, once that's done you'll get a .zip with 3 files:
    -  GeoLite2-ASN.mmdb
    -  GeoLite2-City.mmdb
    -  GeoLite2-Country.mmdb
- We need to place these files within Wiresharks maxmind db directory. By default, Wireshark looks in:
    -  C:\ProgramData\GeoIP
    -  C:\GeoIP
- Make sure those three .mmdb files are in one of those folders.
- Next, we need to enable geolocation on Wireshark, open it up, press the 'Edit' tab, and click 'Preferences'.
- You'll see a tab called 'Name Resolution', click it and scroll to the bottom.
- There will be a checkbox named 'Enable IP geolocation', make sure its checked.
- You can now go back to Wireshark, and test it out to make sure its working:

![Wireshark_eacXhtDOwt](https://github.com/user-attachments/assets/39abc994-6413-458f-b080-cd78b6788ada)

- Now you can capture network traffic and move onto the next step!

Step 3: Running the program and installing folium

- Now that we have our project files, Wireshark and GeoIP fully installed, we're going to run our program!

- First, open your network-map directory. This is where you'll place your .pcapng file and receive your folium .html output.
- Record and place a .pcapng file into network-map/pcaps.
- Open Windows Powershell, and navigate to your project-root-dir, mine for example is in F:\Projects\network-map\.
- This where we install folium. Do this with 'pip install folium'

-  Now navigate to your project directory:
-  PS C:\Users\berge> F:
-  PS F:\> cd "F:\Projects\networkMap"
-  PS F:\Projects\networkMap>

-  Now we'll activate the main.py script.

-  PS F:\Projects\networkMap> py main.py

-  You'll see a prompt of it asking which .pcapng file to choose, pick a number.

-  Select a .pcapng file to process:
-  1: example.pcapng
-  2: test1.pcapng
-  Enter a number: 1

-  Running: tshark -r pcaps\example.pcapng -Y ip && (ip.geoip.src_country || ip.geoip.dst_country) -T fields -E header=y -E separator=, -e ip.src -e ip.dst -e ip.geoip.src_country -e ip.geoip.dst_country -e ip.geoip.src_lat -e ip.geoip.src_lon -e ip.geoip.dst_lat -e ip.geoip.dst_lon

-  Done! Wrote deduplicated CSV to outputs\example.csv
-  Plotted 6 nodes and 28 lines
-  Map saved to outputs\example.html
-  PS F:\Projects\networkMap>

-  You can now look in your network-map/outputs/ folder and see our folium .html output.
-  Open this file to see a network map of our .pcapng file.

