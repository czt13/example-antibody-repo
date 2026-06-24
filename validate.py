import json
import sys
from jsonschema import validate, ValidationError
from jsonschema.format_validators import FormatChecker

def validate_changed_files(files_to_validate):
    # Load the master schema
    with open("schema.json", "r") as f:
        schema = json.load(f)
    
    errors_found = False

    print(f"Evaluating {len(files_to_validate)} changed file(s)...")

    # Loop through only the files modified in the PR
    for file_path in files_to_validate:
        # Ignore files that aren't JSON just in case
        if not file_path.endswith(".json"):
            continue
            
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Validate against schema
            validate(instance=data, schema=schema, format_checker=FormatChecker())
            print(f"✅ {file_path} passed validation.")
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"❌ {file_path} failed validation: {e.message if hasattr(e, 'message') else e}")
            errors_found = True

    if errors_found:
        sys.exit(1) # Block the PR merge

if __name__ == "__main__":
    # sys.argv[1:] captures all arguments passed to the script (the file paths)
    arguments = sys.argv[1:]
    
    if not arguments:
        print("No files passed for validation. Skipping.")
        sys.exit(0)
        
    validate_changed_files(arguments)
