import csv
import uuid
import os

def load_data_from_csv(file_name="user_data.csv"):
    """Load data from the CSV file and remove all double quotes."""
    data = []
    file_path = os.path.join(os.getcwd(), file_name)

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip the header row

            for row in csvreader:
                # Clean up each field in the row by removing any double quotes and extra spaces
                cleaned_row = [item.replace('"', '').strip() for item in row]

                # Check if the row has exactly 3 fields (name, email, age)
                if len(cleaned_row) == 3:
                    user_id = str(uuid.uuid4())  # Generate a unique UUID for each user
                    name = cleaned_row[0]
                    email = cleaned_row[1]
                    age = cleaned_row[2]
                    data.append((user_id, name, email, age))
                else:
                    print(f"Skipping invalid row: {row}")  # For rows that don't match expected format

        print(f"Data loaded successfully from {file_path}")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    
    return data
