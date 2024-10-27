import requests
import json
import argparse
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

def banner():
    print(colored("""

        .-. .-')              _   .-')                  
        \  ( OO )            ( '.( OO )_                
        ,--. ,--.    ,-.-')   ,--.   ,--.)  .-'),-----. 
        |  .'   /    |  |OO)  |   `.'   |  ( OO'  .-.  '
        |      /,    |  |  \  |         |  /   |  | |  |
        |     ' _)   |  |(_/  |  |'.'|  |  \_) |  |\|  |
        |  .   \    ,|  |_.'  |  |   |  |    \ |  | |  |
        |  |\   \  (_|  |     |  |   |  |     `'  '-'  '
        `--' '--'    `--'     `--'   `--'       `-----' 
               -[ # Github: HAOUATKARIM # ]-

    """, "cyan"))

banner()

# Define regions choices
REGION_CHOICES = ['eu', 'ap', 'us', 'mx', 'me', 'ca', 'cn', 'sa', 'af', 'st', 'th', 'ov', 'uc', 'il']

def print_welcome_message():
    print(f"{BOLD}{GREEN}Welcome to the RDP IP Range Fetcher!{RESET}")
    print(f"{ITALIC}Let's collect some IP ranges and prepare for scanning!{RESET}")
    print(SEPARATOR)

def fetch_aws_ranges(region=None):
    print(f"{BLUE}Fetching AWS IP ranges...{RESET}")
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    data = response.json()

    if region:
        aws_ranges = [prefix['ip_prefix'] for prefix in data['prefixes'] if prefix['service'] == 'AMAZON' and prefix['region'].startswith(region)]
        print(f"{GREEN}Filtered AWS ranges for region '{region}': {len(aws_ranges)}{RESET}")
    else:
        aws_ranges = [prefix['ip_prefix'] for prefix in data['prefixes'] if prefix['service'] == 'AMAZON']
        print(f"{GREEN}Total AWS ranges fetched: {len(aws_ranges)}{RESET}")
    
    return aws_ranges

def fetch_google_ranges(region=None):
    print(f"{BLUE}Fetching Google Cloud IP ranges...{RESET}")
    url = "https://www.gstatic.com/ipranges/cloud.json"
    response = requests.get(url)
    data = response.json()

    if region:
        google_ranges = [prefix['ipv4Prefix'] for prefix in data['prefixes'] if 'ipv4Prefix' in prefix and prefix['scope'].startswith(region)]
        print(f"{GREEN}Filtered Google Cloud ranges for region '{region}': {len(google_ranges)}{RESET}")
    else:
        google_ranges = [prefix['ipv4Prefix'] for prefix in data['prefixes']]
        print(f"{GREEN}Total Google Cloud ranges fetched: {len(google_ranges)}{RESET}")
    
    return google_ranges

def fetch_azure_ranges(region=None):
    print(f"{BLUE}Fetching Azure IP ranges...{RESET}")
    with open('azureRanges.json', 'r') as f:
        data = json.load(f)

    azure_ranges = []
    for value in data['values']:
        prefixes = value['properties']['addressPrefixes']
        if region:
            if value['properties']['region'].startswith(region):
                azure_ranges.extend(prefixes)
        else:
            azure_ranges.extend(prefixes)
    
    print(f"{GREEN}Total Azure ranges fetched: {len(azure_ranges)}{RESET}")
    return azure_ranges

def save_to_file(ranges, output_file):
    print(f"{YELLOW}Saving IP ranges to {output_file}...{RESET}")
    with open(output_file, 'w') as f:
        for ip_range in ranges:
            f.write(ip_range + "\n")
    print(f"{GREEN}All ranges saved to {output_file} successfully!{RESET}")
    print(SEPARATOR)

def main():
    # Welcome message
    print_welcome_message()

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Fetch IP Ranges from AWS, Azure, Google")
    parser.add_argument('--region', '-r', choices=REGION_CHOICES, help="Specify the region to filter (eu, ap, us, etc.)")
    parser.add_argument('--output', '-o', default="RDP_Range.txt", help="Specify the output file name")
    args = parser.parse_args()

    # Step 1: Fetch IP ranges from AWS, Google, and Azure
    aws_ranges = fetch_aws_ranges(args.region)
    google_ranges = fetch_google_ranges(args.region)
    azure_ranges = fetch_azure_ranges(args.region)

    # Combine all ranges
    all_ranges = aws_ranges + google_ranges + azure_ranges

    # Step 2: Save ranges to a file
    save_to_file(all_ranges, args.output)

    print(f"{BOLD}{GREEN}Success!{RESET} {ITALIC}You are now ready to scan for RDP services!{RESET}")

if __name__ == "__main__":
    main()
