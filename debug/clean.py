import json

with open('mal_data.jsonl', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

print(f"Read {len(lines)} lines from mal_data.jsonl")

data = []
for i, line in enumerate(lines, start=1):
    line = line.strip()
    if line:
        try:
            obj = json.loads(line)
            data.append(obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding line {i}: {e}")
    else:
        print(f"Skipping empty line {i}")

print(f"Parsed {len(data)} JSON objects")

with open('clean.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)

print(f"✅ Cleaned {len(data)} records into clean.json")
