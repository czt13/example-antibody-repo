import os
import json

def compile_database():
    data_dir = "data"
    combined_data = []

    if os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            if filename.endswith(".json"):
                with open(os.path.join(data_dir, filename), "r") as f:
                    try:
                        combined_data.append(json.load(f))
                    except json.JSONDecodeError:
                        print(f"Skipping malformed file: {filename}")

    # Save the combined list to a single master file
    with open("database.json", "w") as f:
        json.dump(combined_data, f, indent=2)
    print("Successfully compiled database.json")

if __name__ == "__main__":
    compile_database()
