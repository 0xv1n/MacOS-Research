import subprocess
import os
import argparse
import re

def get_binary_name(file_path):
    return os.path.basename(file_path)

def check_codesign(file_path):
    try:
        output = subprocess.check_output(['codesign', '-d', '--entitlements', '-', file_path], stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return ""

def search_man_pages(binary_name):
    try:
        man_output = subprocess.check_output(['man', binary_name], stderr=subprocess.STDOUT, universal_newlines=True)
        return man_output
    except subprocess.CalledProcessError as e:
        return ""

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('directory', help='')
    args = parser.parse_args()

    directory_to_scan = args.directory
    matched_binaries = []

    for root, _, files in os.walk(directory_to_scan):
        for file in files:
            file_path = os.path.join(root, file)
            binary_name = get_binary_name(file_path)
            codesign_output = check_codesign(file_path)
            if 'com.apple.security.cs.disable-library-validation' in codesign_output:
                man_output = search_man_pages(binary_name)
                matched_lines = [line for line in man_output.split('\n') if re.search(r'\b(library|libraries)\b', line, re.I)]
                if matched_lines:
                    matched_binaries.append((binary_name, file_path, codesign_output, matched_lines))

    if matched_binaries:
        print("Binaries with matched content:")
        for binary_name, file_path, codesign_output, matched_lines in matched_binaries:
            print(f"Binary Name: {binary_name}")
            print(f"File Path: {file_path}")
            print("Output from codesign:")
            print(codesign_output)
            print("Matched Lines from man page:")
            for line in matched_lines:
                print(line)
            print()

if __name__ == "__main__":
    main()
