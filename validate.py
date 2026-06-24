import os
import json
from jsonschema import validate, ValidationError
# This is the updated, correct import for the format checker:
from jsonschema import FormatChecker

def load_schema(schema_path):
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_json_files(data_dir, schema):
    # Initialize the format checker to validate URLs and email structures
    format_checker = FormatChecker()
    errors_found = False

    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist.")
        return False

    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    # Pass the format_checker into the validation runner
                    validate(instance=data, schema=schema, format_checker=format_checker)
                    print(f"[SUCCESS] {filename} is valid.")
                except json.JSONDecodeError:
                    print(f"[ERROR] {filename} is not a valid JSON syntax file.")
                    errors_found = True
                except ValidationError as e:
                    print(f"[ERROR] {filename} failed schema validation: {e.message}")
                    errors_found = True

    return not errors_found

if __name__ == "__main__":
    schema_file = "schema.json"
    data_directory = "data"
    
    schema_data = load_schema(schema_file)
    if validate_json_files(data_directory, schema_data):
        print("All files validated successfully.")
        exit(0)
    else:
        print("Some files failed validation.")
        exit(1)
