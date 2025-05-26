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


---

## ❌ Limitations or Unimplemented Components

- **CI/CD Pipeline (GitHub Actions)** was not added initially.
- **Test file** was not written during development phase.
- **Large image size (~2–3GB)** may be unsuitable for low-bandwidth environments.

---

## 🔄 Plan to Overcome Limitations

- Add GitHub Actions workflow for CI/CD with Docker image build and push.
- Include basic FastAPI endpoint test script (`test_main.py`) to validate the API.
- Optimize Dockerfile with `multi-stage builds` or remove unused dependencies to shrink image size.

---

## 🧩 Known Limitations

- Large Docker image (~2.5GB compressed)
- Transcription accuracy depends on audio quality and speaker clarity
- API accepts only `.wav` files (not `.mp3` or `.ogg`)

---

## 🧠 Assumptions

- Input audio is clean, short (5–10s), and in Hindi
- User has Docker Desktop installed and running