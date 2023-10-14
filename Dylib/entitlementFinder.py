import subprocess
import os
import argparse

# Set a default path if you want, else specify as arg
# Usage: entitlementFinder.py /usr/bin
directory_to_scan = '/path/to/your/directory'
results = {}

def check_codesign(file_path):
    try:
        output = subprocess.check_output(['codesign', '-d', '--entitlements', '-', file_path], stderr=subprocess.STDOUT, universal_newlines=True)
        if 'com.apple.security.cs.disable-library-validation' in output:
            results[file_path] = output
    except subprocess.CalledProcessError as e:
        pass

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('directory', help='')
    args = parser.parse_args()

    directory_to_scan = args.directory

    for root, _, files in os.walk(directory_to_scan):
        for file in files:
            file_path = os.path.join(root, file)
            check_codesign(file_path)

    for file_path, output in results.items():
        print(f"File: {file_path}")
        print(output)

if __name__ == "__main__":
    main()
