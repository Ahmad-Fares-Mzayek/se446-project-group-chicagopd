import sys

# Index of relevant columns (check your CSV header!)
# Schema: ID, Case Number, Date, ..., Arrest(8), ..., District(11)
arrest_index = 8

for line in sys.stdin:
    line = line.strip()

    # Skip empty lines
    if not line:
        continue

    parts = line.split(',')

    # Sanity Check: Ensure line has enough columns
    if len(parts) <= arrest_index:
        continue
    #skip the headers line
    if parts[0] == "ID":
        continue

    # Extract fields
    arrest_status = parts[arrest_index].strip().lower()
    if (arrest_status=="true"):
        print("Arrested\t1")
    else:
        print("Not Arrested\t1")

