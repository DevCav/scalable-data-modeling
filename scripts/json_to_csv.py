import pandas as pd
import json
import os
import re
import csv

# Define input and output directories
input_dir = "raw_json/"
output_dir = "seeds/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Set max field length for dbt compatibility
MAX_FIELD_LENGTH = 131072  
COLUMN_TO_DROP = "rewards_receipt_item_list"  # Column to remove

def to_snake_case(name):
    """Convert column names to snake_case"""
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)  # Replace special characters with underscores
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()  # Convert CamelCase to snake_case
    name = re.sub(r'_+', '_', name).strip('_')  # Remove extra underscores
    return name

def truncate_long_fields(df, max_length):
    """Truncate any field that exceeds the max_length limit"""
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x[:max_length] if isinstance(x, str) and len(x) > max_length else x)
    return df

# Loop through all JSON files in the directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".json"):  # Process only JSON files
        input_path = os.path.join(input_dir, file_name)

        try:
            with open(input_path, "r") as file:
                first_char = file.read(1)  # Read the first character to check the format
                file.seek(0)  # Reset file pointer

                if first_char == "[":  
                    # JSON is an array → Load normally
                    data = json.load(file)
                else:
                    # JSON is NDJSON → Read line by line
                    data = [json.loads(line) for line in file]

            # Convert JSON data to DataFrame
            df = pd.json_normalize(data)  

            # Convert column names to snake_case
            df.columns = [to_snake_case(col) for col in df.columns]

            # Drop the unwanted column if it exists
            if COLUMN_TO_DROP in df.columns:
                df.drop(columns=[COLUMN_TO_DROP], inplace=True)
                print(f"🚨 Dropped column: {COLUMN_TO_DROP} from {file_name}")

            # Truncate long fields to avoid dbt seed issues
            df = truncate_long_fields(df, MAX_FIELD_LENGTH)

            # Define output CSV filename (same as JSON but with .csv extension)
            output_file_name = file_name.replace(".json", ".csv")
            output_path = os.path.join(output_dir, output_file_name)

            # Save DataFrame to CSV with proper quoting to avoid issues
            df.to_csv(output_path, index=False, quoting=csv.QUOTE_MINIMAL)

            print(f"✅ Processed: {file_name} → {output_file_name}")

        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")

print("🎯 All JSON files have been converted to CSV successfully.")

