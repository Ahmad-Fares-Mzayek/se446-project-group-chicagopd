import sys

# Index of relevant columns (check your CSV header!)
# Schema: ID, Case Number, Date, ..., Arrest(8), ..., District(11)
location_index = 7

for line in sys.stdin:
    line = line.strip()

    # Skip empty lines
    if not line:
        continue

    parts = line.split(',')

    # Sanity Check: Ensure line has enough columns
    if len(parts) <= location_index:
        continue
    #skip the headers line
    if parts[0] == "ID":
        continue

    # Extract fields
    locations = parts[location_index].strip()
    print(f"{locations}\t1")

