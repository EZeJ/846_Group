def load_ages(path):
    import csv
    ages = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header_skipped = False
        for row in reader:
            if not header_skipped:
                # Skip header if present
                if row and row[0].strip().lower() == "age":
                    header_skipped = True
                    continue
                header_skipped = True  # No header, treat first row as data
            if not row or not row[0].strip():
                continue  # skip blank lines
            try:
                age = int(row[0])
            except ValueError:
                continue  # skip non-integer
            except IndexError:
                continue  # skip malformed rows
            if 0 <= age <= 120:
                ages.append(age)
    return ages