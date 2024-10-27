import subprocess
import argparse
import threading
import time
from termcolor import colored

# ANSI escape codes for colors and styles
BOLD = '\033[1m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
SEPARATOR = f"{CYAN}{'='*50}{RESET}"
gitHubUser = colored("HAOUATKARIM", "white", attrs=["bold", "underline"])
ENTER = colored(" ENTER ", "white", "on_black", attrs=["bold"])
def kimo_banner():
    print(colored(f"""

            <-.(`-')    _      <-. (`-')              
             __( OO)   (_)        \(OO )_       .->   
            '-'. ,--.  ,-(`-') ,--./  ,-.) (`-')----. 
            |  .'   /  | ( OO) |   `.'   | ( OO).-.  '
            |      /)  |  |  ) |  |'.'|  | ( _) | |  |
            |  .   '  (|  |_/  |  |   |  |  \|  |)|  |
            |  |\   \  |  |'-> |  |   |  |   '  '-'  '
            `--' '--'  `--'    `--'   `--'    `-----' 
                # Github: ==> {gitHubUser}

    """, "cyan"))
kimo_banner()

def print_welcome_message():
    print(f"{BOLD}{GREEN}Welcome to the Optimized RDP IP Checker!{RESET}")
    print(f"{ITALIC}We are now scanning for open RDP ports (3389).{RESET}")
    print(SEPARATOR)

# Global flag to stop scanning current range
stop_scan = False

def print_welcome_message():
    print(f"{BOLD}{GREEN}Welcome to the RDP IP Checker!{RESET}")
    print(f"{ITALIC}We are now scanning for open RDP ports (3389).{RESET}")
    print(SEPARATOR)

def scan_for_rdp(ip_range_file="RDP_Range.txt", output_file="All_RDP.txt"):
    global stop_scan

    print(f"{BLUE}Reading IP ranges from {ip_range_file}...{RESET}")
    with open(ip_range_file, 'r') as f:
        ip_ranges = f.readlines()

    with open(output_file, 'a') as out_f:  # Append to output file
        for ip_range in ip_ranges:
            ip_range = ip_range.strip()
            if ip_range:
                stop_scan = False  # Reset the stop flag for each range
                print(f"{YELLOW}Scanning {ip_range} for RDP... (Press {ENTER} to skip this range){RESET}")
                
                # Run the scanning in a separate thread
                scan_thread = threading.Thread(target=nmap_scan, args=(ip_range, out_f))
                scan_thread.start()
                
                # Listen for ENTER key press to skip the range
                input_thread = threading.Thread(target=listen_for_enter)
                input_thread.start()

                # Wait for scan to complete or user to press ENTER
                scan_thread.join()
                print(f"{GREEN}Finished scanning {ip_range}{RESET}")
                print(SEPARATOR)

    print(f"{BOLD}{GREEN}All done!{RESET} {ITALIC}Check {output_file} for the list of open RDP servers.{RESET}")

def nmap_scan(ip_range, out_f):
    global stop_scan
    result = subprocess.Popen(['nmap', '-p', '3389', '--open', ip_range, '-oG', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Process nmap output
    while True:
        output = result.stdout.readline().decode()
        if result.poll() is not None and not output:
            break
        if output:
            if '3389/open' in output:
                ip = output.split()[1]
                print(f"{GREEN}Valid RDP found: {ip}{RESET}")
                out_f.write(ip + "\n")  # Write valid RDP IPs to file immediately

        if stop_scan:
            result.kill()
            print(f"{RED}Scan skipped for {ip_range}{RESET}")
            break

def listen_for_enter():
    global stop_scan
    input()  # Wait for the user to press ENTER
    stop_scan = True  # Set the flag to stop the current scan

def main():
    # Welcome message
    print_welcome_message()

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Scan IP ranges for open RDP services")
    parser.add_argument('--input', '-i', default="RDP_Range.txt", help="Input file containing IP ranges")
    parser.add_argument('--output', '-o', default="All_RDP.txt", help="Output file to save the found RDP IPs")
    args = parser.parse_args()

    # Scan the ranges for RDP (Port 3389)
    scan_for_rdp(args.input, args.output)

if __name__ == "__main__":
    main()
