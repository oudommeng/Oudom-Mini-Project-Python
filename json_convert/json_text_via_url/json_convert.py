import json
import requests
import os


def json_to_text(json_data, ensure_ascii=False):
    """
    Convert JSON data to a formatted text string with proper Unicode support.
    
    Args:
        json_data (str): A JSON formatted string.
        ensure_ascii (bool): When False, non-ASCII characters (like Khmer) are output as-is
        
    Returns:
        str: A formatted text representation of the JSON data.
    """
    try:
        parsed_data = json.loads(json_data)
        # Using ensure_ascii=False preserves non-ASCII characters like Khmer
        return json.dumps(parsed_data, indent=4, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Invalid JSON data: {e}"


def extract_full_transcript(json_data):
    """
    Extract and join all transcript segments from the JSON data.
    
    Args:
        json_data (str): A JSON formatted string.
        
    Returns:
        str: The full transcript text.
    """
    try:
        data = json.loads(json_data)
        full_transcript = " ".join(segment["transcript"]
                                   for segment in data["segments"])
        return full_transcript
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error extracting transcript: {e}"


def load_from_localhost(url="http://localhost:8000/data", token=None):
    """
    Fetch JSON data from a localhost URL with optional token authentication
    
    Args:
        url (str): The localhost URL to fetch data from
        token (str): Authentication token
        
    Returns:
        str: JSON string response or error message
    """
    try:
        headers = {}
        if token:
            # Add token as Bearer authentication
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"


def save_transcript_to_file(transcript, file_path):
    """
    Save the transcript text to a file with UTF-8 encoding.
    
    Args:
        transcript (str): The transcript text to save
        file_path (str): Path where the file should be saved
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the transcript to file with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        return True
    except Exception as e:
        print(f"Error saving transcript: {e}")
        return False


# Example usage
if __name__ == "__main__":
    # Your authentication token
    auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjAxSzMwNTZUNEY0RkczWVNCQTZTR0haUzVCIiwidXNlcm5hbWUiOiJvdWRvbSIsImVtYWlsIjoib3Vkb21AMTIzLmNvbSIsImlhdCI6MTc1NTU3NzA1OCwiZXhwIjoxNzU2MTgxODU4fQ.eIUZy_acXn971P3XHgg_ycIo0q3kektUeeWXD-pNG7o"

    # Your data path
    dataurl = "/output/0f162db5-2a09-48e1-8d18-ebe2ac89dda8_output/0f162db5-2a09-48e1-8d18-ebe2ac89dda8.json"

    # Construct proper URL (don't use string formatting in URL)
    localhost_url = f"http://localhost:8000{dataurl}"

    # Load JSON data from localhost with token
    json_data = load_from_localhost(localhost_url, token=auth_token)

    # Extract ID from URL for the output filename
    file_id = dataurl.split("/")[-1].replace(".json", "")

    # Extract the full transcript
    full_transcript = extract_full_transcript(json_data)

    # Save the transcript to a file in the json_to_text folder
    output_path = os.path.join("json_to_text", f"{file_id}_output.txt")
    if save_transcript_to_file(full_transcript, output_path):
        print(f"Transcript saved to {output_path}")

    # Convert and print formatted JSON
    formatted_text = json_to_text(json_data)
    print(formatted_text)
