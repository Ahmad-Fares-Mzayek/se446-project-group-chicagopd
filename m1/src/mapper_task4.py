import sys

date_index = 2

for line in sys.stdin:
    line = line.strip()
    # skip empty lines 
    if not line:
        continue

    # split lines
    parts = line.split(',')

    #sanity check to ensure lines have enough columns
    if len(parts) <= date_index:
        continue

    #skip headers lines
    if parts[0] == 'ID':
        continue
    #extract fields
    date_time = parts[date_index].strip()
    date = date_time.split(' ')[0]
    year = date.split('/')[2]

    #print output
    print(f"{year}\t1")



   