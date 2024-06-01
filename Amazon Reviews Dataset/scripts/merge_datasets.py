import json
import os
import hashlib

# Define the directory containing the JSON files
root = os.path.dirname(os.path.abspath(__file__))
directory = os.path.abspath(os.path.join(root, '..', 'data'))
output_file = 'Amazon_All_Categories.jsonl'
duplicates_file = 'Amazon_Duplicates.jsonl'  # New file for duplicates

# Initialize total record count
total_records = 0
total_records_before = 0
total_duplicates = 0  # Counter for duplicates

# Initialize set to store unique hashes of review JSON objects
unique_hashes = set()

# Open the output file for writing
with open(output_file, 'w') as merged_file, open(duplicates_file, 'w') as duplicates:
    # Iterate over all json files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.jsonl'):
            category = os.path.splitext(filename)[0]  # Use filename (without extension) as category
            file_path = os.path.join(directory, filename)

            # Initialize category-specific record counts
            category_records_before = 0
            category_records_after = 0
            category_duplicates = 0  # Counter for duplicates in the current category

            with open(file_path, 'r') as file:
                # Read each line as a JSON object
                for line in file:
                    category_records_before += 1
                    total_records_before += 1

                    data = json.loads(line.strip())

                    # Hash the entire review JSON object
                    data_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

                    # Check if the hash already exists, if so, write to duplicates file
                    if data_hash in unique_hashes:
                        # Add the category to the JSON object before writing to duplicates file
                        data['product_category'] = category
                        duplicates.write(json.dumps(data) + '\n')
                        total_duplicates += 1
                        category_duplicates += 1
                        continue

                    # Add the hash to the set
                    unique_hashes.add(data_hash)

                    # Add the category to the JSON object
                    data['product_category'] = category
                    # Write the modified JSON object to the output file
                    merged_file.write(json.dumps(data) + '\n')
                    category_records_after += 1
                    total_records += 1

            print(f"Category '{category}' - Reviews before: {category_records_before}, after removing duplicates: {category_records_after}, duplicates: {category_duplicates}")

print(f"Files merged successfully into {output_file}")
print(f"Total reviews before removing duplicates: {total_records_before}")
print(f"Total reviews after removing duplicates: {total_records}")
print(f"Total duplicates saved to {duplicates_file}: {total_duplicates}")
