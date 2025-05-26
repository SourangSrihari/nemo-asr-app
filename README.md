# Nemo ASR App (Automatic Speech Recognition)

This project serves a FastAPI application that performs speech-to-text transcription for Hindi .wav audio files using a pretrained NVIDIA NeMo ASR model, fully containerized with Docker.


## Getting Started

You can run this project in **two ways**:

---

### Option A: Run Locally from Dockerfile

#### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- Docker engine running

#### Steps

1. **Clone this repository or navigate to the project folder** 

In the command prompt:

```bash
git clone <your-repo-url>
cd nemo-asr-app
```

2. **Build the Docker Image**

```bash
docker build -t nemo-asr-app .
```

3. **Run the Docker container**

```bash
docker run -p 8000:8000 nemo-asr-app
```

4. **Visit Swagger UI**
 
   Open your browser and go to [http://localhost:8000/docs#/](http://localhost:8000/docs#/)

---

### Option B: Run from Docker Hub(Pull Prebuilt Image)


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

### 💻 Option B: Using `curl` (Windows CMD)

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


