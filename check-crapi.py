import json
import sys
import os.path as path

if len(sys.argv) <= 1:
    print("ERROR:")
    print(f" python {sys.argv[0]} [input file]")
    exit()

input_file = sys.argv[1]
if not path.isfile(input_file):
    print("ERROR: file does not exist")
    exit()

with open(input_file, 'r') as file:
    dlls = json.load(file)

using_keys = []
for dll,functions in dlls.items():
    if functions == "No exports":
        continue

    for fun in functions:
        if fun == "CPGenKey":
            using_keys.append(dll)
            continue

print("=== DLLs including CPGenKey ===")
for dll in using_keys:
    print(f" * {dll}")