# RDP IP Range Fetcher & RDP Port Scanner

This repository includes two scripts designed for network reconnaissance and cybersecurity assessment. **RDP IP Range Fetcher** collects IP ranges from major cloud providers (AWS, Azure, and Google Cloud) based on specified regions. **RDP Port Scanner** then scans the collected IP ranges for open RDP ports (port 3389) and provides a list of detected RDP services.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [RDP IP Range Fetcher](#rdp-ip-range-fetcher)
  - [RDP Port Scanner](#rdp-port-scanner)
- [Example Usage](#example-usage)
- [Disclaimer](#disclaimer)

## Overview

### RDP IP Range Fetcher
The **RDP IP Range Fetcher** script retrieves IP ranges from cloud providers (AWS, Azure, Google Cloud) based on specified regions. This functionality enables focused scanning on a subset of IP ranges. Supported regions include `eu`, `ap`, `us`, and more.

### RDP Port Scanner
The **RDP Port Scanner** script scans through the provided IP ranges to detect open RDP ports (port 3389). The scanner is equipped with manual interruption, allowing users to skip the current range by pressing `ENTER`. The tool outputs a list of detected RDP servers to a file for further analysis.

## Prerequisites

- **Python 3.6+** - Required to run the scripts.
- **termcolor Module** - Enables colored console output.
- **nmap** - Used by the RDP Port Scanner for network scanning. Make sure `nmap` is installed and available in your system’s PATH.

> **Note**: This project also uses standard Python libraries (`json`, `argparse`, `subprocess`, `threading`, `time`) that do not require installation.

## Installation

### Step 1: Clone the Repository
Clone this repository to your local system:
   ```bash
   git clone https://github.com/HaouatKarim/RDP-Scanner-v1.0.git
   cd RDP-Scanner-v1.0
   ```

### Step 2: Install Python Dependencies
Install required Python dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Ensure `nmap` is Installed
Ensure that `nmap` is installed. You can install it using:
   ```bash
    # On Debian/Ubuntu
    sudo apt-get install nmap

    # On RedHat/CentOS
    sudo yum install nmap

    # On MacOS
    brew install nmap
```

### Step 1: Clone the Repository
Clone this repository to your local system:
   ```bash
   git clone https://github.com/HaouatKarim/RDP-Scanner-v1.0.git
   cd RDP-Scanner-v1.0
```

## Usage

### RDP IP Range Fetcher
This script fetches IP ranges from cloud providers based on a specified region.

#### Arguments:
- `--region`, `-r`: Specifies the region to focus on (e.g., `eu`, `us`, `ap`, etc.).
- `--output`, `-o`: Specifies the output file name for saving IP ranges (default: `RDP_Range.txt`).

#### Command:
```
python rdp_ip_fetcher.py --region us --output RDP_Range.txt
```

### RDP Port Scanner
The RDP Port Scanner reads IP ranges from a file and scans for open RDP ports (port 3389). During each range scan, you can press `ENTER` to skip the current IP range if needed.

#### Arguments:
- `--input`, `-i`: Specifies the input file with IP ranges to scan (default: `RDP_Range.txt`).
- `--output`, `-o`: Specifies the output file for saving detected RDP IPs (default: `All_RDP.txt`).

#### Command:
```
python rdp_port_scanner.py --input RDP_Range.txt --output All_RDP.txt
```

## Example Usage

### 1. Fetch IP Ranges
```
python rdp_ip_fetcher.py --region us --output RDP_Range.txt
```
This command fetches IP ranges for AWS, Google Cloud, and Azure in the `us` region and saves them to `RDP_Range.txt`.

### 2. Scan for Open RDP Ports
```
python rdp_port_scanner.py --input RDP_Range.txt --output All_RDP.txt
```
This command reads each IP range from `RDP_Range.txt`, scans for open RDP ports, and writes detected IPs to `All_RDP.txt`.


## Disclaimer

This tool is designed solely for educational purposes and authorized security testing. Unauthorized use of this tool to probe, scan, or access any network or system without prior permission from the system owner is strictly prohibited and may be illegal.

The developers and contributors of this tool **are not responsible** for any misuse or any direct or indirect damages caused by the use of this tool. It is your responsibility to ensure compliance with all applicable laws and regulations in your jurisdiction.

**By using this tool, you agree to adhere to ethical hacking standards and obtain explicit permission from the owners of any systems or networks you test.**

**Use responsibly. Unauthorized use is prohibited.**
