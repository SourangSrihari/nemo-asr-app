import requests
import os

# Define the file path
audio_path = "audio_file.wav"

# Check if file exists
if not os.path.exists(audio_path):
    print(f"Error: Audio file '{audio_path}' not found in the current directory.")
else:
    print(f"Sending file: {audio_path}")

    try:
        # Send POST request to FastAPI server
        response = requests.post(
            "http://localhost:8000/transcribe",
            files={"file": open(audio_path, "rb")}
        )

        # Check response status
        print(f"Status Code: {response.status_code}")

        # Print response content
        if response.status_code == 200:
            print("Transcription Result:")
            print(response.json())
        else:
            print("Error occurred:")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("Could not connect to FastAPI server. Is the Docker container running?")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
