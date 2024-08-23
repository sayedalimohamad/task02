import pymongo
import json
import sys


# cleaning the data
# find the indexes of the errors and remove them
# then save the cleaned data to a new JSON file
# the new JSON file will be used to insert the data to the database
def remove_error_data():
    # Read the JSON data from the file
    with open("data/articles.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    # Find the indices of the errors
    error_indices = [
        i for i, article in enumerate(data) if not isinstance(article, dict)
    ]
    # Remove the data at the error indices, starting from the end to avoid index shifting issues
    for index in sorted(error_indices, reverse=True):
        del data[index]
    # Write the updated data back to the JSON file
    with open(f"data/articles_{len(data)}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    # Return the length of the cleaned data
    return len(data)


# end cleaning data

data_length = remove_error_data()

# Load and insert JSON data
json_file_path = f"data/articles_{data_length}.json"

try:
    connect = pymongo.MongoClient("mongodb://localhost:27017/")
    db = connect["almayadeen"]
    collection = db["articles"]
except pymongo.errors.ConnectionFailure:
    print("Failed to connect to MongoDB server")
    sys.exit(1)

try:
    with open(json_file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
        collection.insert_many(data)
    print(
        f"Initial data is 10000 articles after cleaning the data we have {data_length} is inserted to database"
    )
    print("Data inserted successfully")
except FileNotFoundError:
    print(f"File not found: {json_file_path}")
    sys.exit(1)
except UnicodeDecodeError as e:
    print(f"Unicode decode error: {e}")
    sys.exit(1)
