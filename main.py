import os  # For file and directory operations
import subprocess  # To run external commands (tshark)
import config  # Import settings from config.py

# Function: Get a list of .pcapng files from the given directory
def list_pcapng_files(pcap_dir):
    # Check if the directory exists
    if not os.path.exists(pcap_dir):
        print(f"Directory '{pcap_dir}' does not exist. Please create it and add .pcapng files.")
        return []
    # Filter for files ending with .pcapng (case-insensitive)
    files = [f for f in os.listdir(pcap_dir) if f.lower().endswith(".pcapng")]
    if not files:
        print(f"No .pcapng files found in '{pcap_dir}'. Please add files and try again.")
    return files

# Function: Prompt the user to select a file from the list
def prompt_user_selection(file_list):
    print("Select a .pcapng file to process:")
    # Print each file with a corresponding number
    for idx, fname in enumerate(file_list, 1):
        print(f"  {idx}: {fname}")
    # Loop until a valid selection is made
    while True:
        choice = input("Enter a number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(file_list):
            return file_list[int(choice) - 1]
        print("Invalid selection. Please enter a valid number.")

# Function: Run tshark on the selected file and write output to CSV
def run_tshark(input_pcapng, output_csv):
    # Build the tshark command with fields from config.py
    tshark_cmd = [
        config.TSHARK_PATH,
        "-r", input_pcapng,
        "-Y", config.TSHARK_DISPLAY_FILTER,
        "-T", "fields",
        "-E", "header=y",
        "-E", "separator=,"
    ]
    # Add each field to the tshark command
    for field in config.TSHARK_FIELDS:
        tshark_cmd.extend(["-e", field])
    # Show the full command being run for debugging
    print(f"\nRunning: {' '.join(tshark_cmd)}\n")
    # Open the output file and run tshark, writing its output to the file
    with open(output_csv, "w", newline="") as out_f:
        subprocess.run(tshark_cmd, stdout=out_f, check=True)
    print(f"Done! Wrote CSV to {output_csv}")

# Main program function
def main():
    pcap_dir = "pcaps"     # Directory containing .pcapng files
    output_dir = "outputs" # Directory to save CSV outputs
    os.makedirs(output_dir, exist_ok=True) # Make sure outputs/ exists

    # Get list of .pcapng files
    pcaps = list_pcapng_files(pcap_dir)
    if not pcaps:
        return  # Exit if no files found

    # Ask user to select a file
    pcap_file = prompt_user_selection(pcaps)
    input_path = os.path.join(pcap_dir, pcap_file)  # Full path to selected file
    output_file = os.path.splitext(pcap_file)[0] + ".csv"  # Output filename (same base name, .csv extension)
    output_path = os.path.join(output_dir, output_file)     # Full path for output

    # Run tshark and output CSV
    run_tshark(input_path, output_path)

# Run the main program when executed directly
if __name__ == "__main__":
    main()