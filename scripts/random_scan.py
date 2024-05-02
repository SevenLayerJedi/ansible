import random
import subprocess

def read_cidr_blocks(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def random_nmap_scan(cidr_blocks, n=10):
    # Select 10 random CIDR blocks
    selected_blocks = random.sample(cidr_blocks, min(n, len(cidr_blocks)))
    #
    # Run nmap for each selected CIDR block
    for cidr_block in selected_blocks:
        cidr_block_output = cidr_block.replace('/', '_')
        command = f"nmap -sC -sV --script=banner -oA /opt/nmap/test/{cidr_block_output} -vvvv {cidr_block} | lolcat"
        #
        # Execute the command
        print(f"Running: {command}")
        subprocess.run(command, shell=True)

# Example usage
filename = 'colorado_ips_cidr.txt'  # Adjust this to your input file's path
cidr_blocks = read_cidr_blocks(filename)
random_nmap_scan(cidr_blocks)
