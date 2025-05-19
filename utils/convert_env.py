#!/usr/bin/env python3
import sys
import os

def clean_line(line: str) -> str:
    # Log original line
    print(f"🔍 Original: {line.strip()}")

    if not line.startswith("export "):
        print("⏭️ Skipping non-export line.")
        return None

    # Remove 'export ' prefix
    line = line[len("export "):]

    # Remove single quotes
    line = line.replace("'", "")

    # Final cleaned line
    print(f"✅ Cleaned:  {line.strip()}")
    return line.strip()

def convert_env_file(input_path, output_path):
    if not os.path.isfile(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        print(f"\n🚀 Converting '{input_path}' to '{output_path}'...\n")
        for line in infile:
            cleaned = clean_line(line)
            if cleaned:
                outfile.write(cleaned + "\n")

    print(f"\n🎉 Done! Output saved to '{output_path}'\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❗ Usage: python convert_env.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_env_file(input_file, output_file)