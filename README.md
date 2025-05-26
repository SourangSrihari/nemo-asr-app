# Nemo ASR App (Automatic Speech Recognition)

This project serves a FastAPI application that performs speech-to-text transcription for Hindi .wav audio files using a pretrained NVIDIA NeMo ASR model, fully containerized with Docker.


## Getting Started

You can run this project in **two ways**:


#### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- Docker engine running

### Option A: Run from Docker Hub(Pull Prebuilt Image) - Recommended


#### Steps

1. **Pull the Image from Docker Hub** 

```bash
docker pull sourang2000/nemo-asr-app
```

2. **Run the Image**

```bash
docker run -p 8000:8000 sourang2000/nemo-asr-app
```

3. **Visit Swagger UI**
 
   Open your browser and go to [http://localhost:8000/docs#/](http://localhost:8000/docs#/)

### Option B: Run Locally from Dockerfile



#### Steps

1. **Clone this repository or navigate to the project folder** 

In the command prompt:

```bash
git clone https://github.com/SourangSrihari/nemo-asr-app.git
cd nemo-asr-app
```

2. **Download Required Model Files**

GitHub restricts files larger than 100MB. Please manually download the following files required for model inference:

- **Download from Google Drive**: [Additional_files Folder](https://drive.google.com/drive/folders/1O-rYXH8ybVzGkNNwlrQ1euHWR7WZhg6l?usp=sharing)

- `asr_model.onnx`
- `stt_hi_conformer_ctc_medium.nemo`

Place both files inside the root of your cloned `nemo-asr-app` project folder **before** building the Docker image.



3. **Build the Docker Image**

```bash
docker build -t nemo-asr-app .
```

4. **Run the Docker container**

```bash
docker run -p 8000:8000 nemo-asr-app
```

5. **Visit Swagger UI**
 
   Open your browser and go to [http://localhost:8000/docs#/](http://localhost:8000/docs#/)

---





## Transcription Endpoint: `/transcribe`

**Note**: Ensure that you run the image before transcribing the audio files

### Audio File Requirements
- **Format**: `.wav`  
- **Length**: 5–10 seconds  
- **Sample Rate**: 16kHz (automatic resampling supported)

---

### Option A: Using Swagger UI
1. Navigate to Swagger UI using [http://localhost:8000/docs#/](http://localhost:8000/docs#/)
2. Click on the `POST /transcribe` endpoint
3. Click "Try it out"
4. Upload your `.wav` file in the **file** field  
5. Click **Execute**
You will receive a JSON response containing the transcription, token IDs, and confidence metrics under the fields `transcription`, `predicted_ids`, and `confidence_summary`.

#### Sample JSON Response Format

```bash
{
  "transcription": "मेरा नाम राम है ...",
  "predicted_ids": [...],
  "confidence_summary": {
    "average_confidence": -0.02,
    "low_confidence_tokens": 0,
    "total_tokens": 166
  }
}
```

---

### Option B: Using `curl` (Windows CMD)

In another command prompt, run the following command:

```bash
curl -X POST http://localhost:8000/transcribe -H "accept: application/json" -F "file=@\"C:\\full\\path\\to\\your\\audio.wav\""
  ```
-  Make sure to replace C:\\full\\path\\to\\your\\audio.wav with the absolute path to your .wav file
-  The output should appear in the command prompt itself



  ## Design Considerations

- The model has been converted to **ONNX** for lightweight and fast inference.
- The **FastAPI** application includes audio preprocessing (resampling, silence trimming, CMVN).
- Only **.wav** files are accepted for robustness.
- The container image uses a **Python slim base** for reduced size.
- Runtime dependencies are installed via **requirements.txt**.


## Repository Notes

### Model Files Disclaimer

> **Note:** The model files `asr_model.onnx` and `stt_hi_conformer_ctc_medium.nemo` are **excluded** from this GitHub repository because they exceed GitHub's 100MB file size limit.

- These files are essential for ASR model inference and are **automatically bundled** inside the Docker image.

- If you are **building the image locally**, make sure the files are present in your project directory **before running**:

```bash
docker build -t nemo-asr-app .
```

- If using the prebuilt image from Docker Hub `(sourang2000/nemo-asr-app)`, no additional setup is required — the files are already included.


## Sample Input & Output

You can find a test `.wav` audio clip and a sample JSON output in the [`sample_data`](./sample_data/) folder.

- [`sample_audio.wav`](./sample_data/sample_audio.wav) — Test file for `/transcribe`
- [`sample_response.json`](./sample_data/sample_response.json) — Sample response from the API



## Video Demonstration

Watch a short walkthrough of the application in action, including setup and a transcription example.

**Google Drive Link**: [App_Demo (Demo.mp4)](https://drive.google.com/drive/folders/14U7l9Ahs1CbCfYrlceQNLeW3PcTq5DNY?usp=sharing)
