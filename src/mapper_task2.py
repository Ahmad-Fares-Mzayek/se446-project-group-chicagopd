import sys

# Index of relevant columns (check your CSV header!)
# Schema: ID, Case Number, Date, ..., Arrest(8), ..., District(11)
crimetype_index = 5

for line in sys.stdin:
    line = line.strip()

    # Skip empty lines
    if not line:
        continue

    parts = line.split(',')

    # Sanity Check: Ensure line has enough columns
    if len(parts) <= crimetype_index:
        continue
    #skip the headers line
    if parts[0] == "ID":
        continue

    # Extract fields
    crimetypes = parts[crimetype_index].strip()
    print(f"{crimetypes}\t1")

