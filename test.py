import requests
import json
from datetime import datetime

def create_index(json_data, process_log_path):
    index_result = "error"

    try:
        deserialized = json.loads(json_data)
        deserialized["name"] = IndexName
        json_data = json.dumps(deserialized)

        url = f"https://{ServiceName}.search.windows.net/indexes/{IndexName}?api-version=2019-05-06"
        headers = {
            "Content-Type": "application/json",
            "api-key": ApiKey
        }

        response = requests.put(url, headers=headers, data=json_data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        index_result = "success"
    except requests.exceptions.RequestException as ex:
        with ex.response as error_response:
            error_message = f"AzureIndexer/CreateIndex| Error Msg={error_response.text}| DateTime: {datetime.now().strftime('%m-%d-%Y %I %M')}"
            logging_write_single_log(error_message, process_log_path)

    return index_result

def logging_write_single_log(message, file_path):
    with open(file_path, "a") as log_file:
        log_file.write(message + "\n")

# Example usage
ServiceName = "your_service_name"
IndexName = "your_index_name"
ApiKey = "your_api_key"
json_data = '{"name": "your_index_name", "other_property": "other_value"}'
process_log_path = "path/to/your/log/file.log"

result = create_index(json_data, process_log_path)
print(result)
