import os
import subprocess
import config
from scripts.map import read_csv, plot_connections

def list_pcapng_files(pcap_dir):
    # Return a list of .pcapng files in the specified directory.
    if not os.path.exists(pcap_dir):
        print(f"Directory '{pcap_dir}' does not exist. Please create it and add .pcapng files.")
        return []
    files = [f for f in os.listdir(pcap_dir) if f.lower().endswith(".pcapng")]
    if not files:
        print(f"No .pcapng files found in '{pcap_dir}'. Please add files and try again.")
    return files

def prompt_user_selection(file_list):
    # Prompt user to select a file from the list.
    print("Select a .pcapng file to process:")
    for idx, fname in enumerate(file_list, 1):
        print(f"  {idx}: {fname}")
    while True:
        choice = input("Enter a number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(file_list):
            return file_list[int(choice) - 1]
        print("Invalid selection. Please enter a valid number.")

def run_tshark(input_pcapng, temp_csv):
    # Run tshark and write raw CSV output to a temporary file.
    tshark_cmd = [
        config.TSHARK_PATH,
        "-r", input_pcapng,
        "-Y", config.TSHARK_DISPLAY_FILTER,
        "-T", "fields",
        "-E", "header=y",
        "-E", "separator=,"
    ]
    for field in config.TSHARK_FIELDS:
        tshark_cmd.extend(["-e", field])
    print(f"\nRunning: {' '.join(tshark_cmd)}\n")
    with open(temp_csv, "w", newline="") as out_f:
        subprocess.run(tshark_cmd, stdout=out_f, check=True)

def deduplicate_csv(temp_csv, output_csv):
    # Remove duplicate rows from the CSV, preserving the header.
    seen = set()
    with open(temp_csv, "r", newline="") as inp, open(output_csv, "w", newline="") as out:
        header = inp.readline()
        out.write(header)
        for line in inp:
            if line not in seen:
                out.write(line)
                seen.add(line)
    os.remove(temp_csv)  # Clean up temp file

def main():
    pcap_dir = "pcaps"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # --- Step 1: PCAPNG to CSV ---
    pcaps = list_pcapng_files(pcap_dir)
    if not pcaps:
        return

    pcap_file = prompt_user_selection(pcaps)
    input_path = os.path.join(pcap_dir, pcap_file)
    base_file = os.path.splitext(pcap_file)[0]
    output_csv = f"{base_file}.csv"
    output_path = os.path.join(output_dir, output_csv)
    temp_csv = os.path.join(output_dir, f"{base_file}.tmp.csv")

    run_tshark(input_path, temp_csv)
    deduplicate_csv(temp_csv, output_path)
    print(f"Done! Wrote deduplicated CSV to {output_path}")

    # --- Step 2: CSV to HTML Map ---
    rows = read_csv(output_path)
    output_html = os.path.join(output_dir, f"{base_file}.html")
    plot_connections(rows, output_html=output_html)

    # --- Step 3: Cleanup CSV --- Commenting out for debug
    # os.remove(output_path)
    # print(f"Deleted {output_csv}")

if __name__ == "__main__":
    main()