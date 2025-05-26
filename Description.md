# Description.md — ASR Deployment Summary

This document summarizes the key accomplishments, challenges, and known limitations of building the Hindi Automatic Speech Recognition (ASR) web service using FastAPI, ONNX, and NVIDIA NeMo, containerized with Docker.

---

## Features Successfully Implemented

- FastAPI server with a `/transcribe` endpoint for uploading `.wav` files
- Accepts audio in any sample rate and resamples to 16kHz internally
- Audio preprocessing pipeline including silence trimming and CMVN normalization
- ONNX-based inference using pretrained NeMo ASR model
- Returns transcription, token ID sequence, and confidence summary in JSON
- Dockerized application with a clean Dockerfile using a Python slim base
- Image published on Docker Hub (`sourang2000/nemo-asr-app`)
- Endpoints tested via both Swagger UI and `curl`
- Comprehensive `README.md` with build/run instructions

---

## Issues Encountered During Development

1. **Pip Timeout Errors** during Docker builds:
   - Large wheel downloads (e.g., PyTorch, NeMo) failed due to default timeout due to unstable internet connection and storage expensive nature of files.
   - **Fix:** Increased pip timeout using `--default-timeout=300`.

2. **`ModelFilter` ImportError from `huggingface_hub`:**
   - Mismatch between NeMo version and newer `huggingface_hub` version.
   - **Fix:** Pinned `huggingface_hub==0.23.2` with `nemo_toolkit[asr]==1.23.0` to ensure compatibility.

3. **Build Image Repetition Issues:**
   - Rebockerignore` and reduced context size for efficiency.uilding large Docker images on every change was time-consuming.
   - **Fix:** Used `.d

4. **ONNX Input Shape Mismatch:**
   - `Required inputs (['length']) are missing from input feed (['audio_signal'])`. This was due to Expected shape was `(batch, channel, time)` but got `(batch, time)`
   - **Fix:** Resolved by reshaping to `(1, 1, time_steps)` with np.expand_dims

5. **GitHub Push Failure Due to File Size**
 
   - Model files `asr_model.onnx` and `stt_hi_conformer_ctc_medium.nemo` exceeded GitHub’s 100MB file size limit, causing push failures.


   - **Fix:**

     - Removed them from Git tracking.
     - Added the files to `.gitignore`.
     - Rewrote Git history using `git filter-repo` to remove traces of the large files.
     - Hosted the model files externally via **Google Drive**.


---

## 🚫 Limitations or Unimplemented Components

- Inference is **synchronous**; async optimization was skipped.
- Large model files (`asr_model.onnx`, `stt_hi_conformer_ctc_medium.nemo`) are **not hosted in the repo** due to GitHub's 100MB limit.
  - **Manual download is required** if you're building the image locally.
- No frontend or graphical UI — interaction is limited to:
  - Swagger UI (`/docs`)
  - `curl` CLI

---

### ❓ Why Async Inference Was Not Implemented

Although FastAPI supports asynchronous endpoints, true async execution wasn't used because:

- **ONNX Runtime is synchronous** — `InferenceSession.run()` blocks the thread and has no async API.
- **Librosa and NumPy** (used for audio loading and preprocessing) are CPU-bound and synchronous.
- Wrapping these in `async def` wouldn’t provide real concurrency benefits.

Implementing true async would require:

- Async-compatible inference (e.g., **Triton Inference Server** or **TensorRT**)
- Background task queues (e.g., **Celery** with workers)
---


## 🚀 Future Improvements

- **Async Inference**: Use `run_in_executor` with FastAPI to offload blocking ONNX inference, or adopt Triton Inference Server for full async support.

- **Model Size Optimization**: Apply ONNX quantization (e.g., INT8/FP16) or switch to lighter models like QuartzNet.

- **Minimal Web UI**: Add a basic HTML/JS interface for audio upload and transcription display, integrated with the FastAPI backend.


---

## 🧩 Known Limitations

- Large Docker image (~2.5GB compressed)
- Transcription accuracy depends on audio quality and speaker clarity
- API accepts only `.wav` files (not `.mp3` or `.ogg`)

---

## 🧠 Assumptions

- Input audio is clean, short (5–10s), and in Hindi
- User has Docker Desktop installed and running

---
## 🎯 Bonus Implementation

### ✅ CI/CD with GitHub Actions
- Configured a CI/CD pipeline using **GitHub Actions**.
- Automatically builds the Docker image and pushes it to Docker Hub on every push to the `main` branch.
- **Workflow File:** `.github/workflows/docker-build.yml`

### ✅ Test File for `/transcribe`
- Created a `test_transcribe.py` script.
- It sends a sample `.wav` file to the `/transcribe` endpoint.
- Prints the response JSON containing the transcription and confidence scores.
