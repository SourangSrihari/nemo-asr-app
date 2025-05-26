from fastapi import FastAPI, File, UploadFile, HTTPException
import onnxruntime as ort
import numpy as np
import librosa
import io
from nemo.collections.asr.models import EncDecCTCModel

app = FastAPI()

# Load ONNX model
session = ort.InferenceSession("asr_model.onnx")

# Load vocabulary from NeMo model for decoding only
nemo_model = EncDecCTCModel.restore_from("stt_hi_conformer_ctc_medium.nemo")
vocab = nemo_model.decoder.vocabulary

# Ensure ONNX output token size matches vocab
onnx_vocab_size = session.get_outputs()[0].shape[-1]
if len(vocab) < onnx_vocab_size:
    vocab.append("")  # Add dummy token for ID 128

def decode_ids(ids):
    """Decode token IDs to text, apply CTC-style decoding."""
    text = ""
    prev = None
    for id in map(int, ids):  # convert np.int64 to int
        if id != prev and id != 0 and id < len(vocab):
            text += vocab[id]
        prev = id
    # Clean spacing (▁ and | are token separators)
    return text.replace("▁", " ").replace("|", " ").strip()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported.")

    audio_bytes = await file.read()

    try:
        # Load and preprocess audio: mono, 16kHz, trim silence, normalize
        waveform, _ = librosa.load(io.BytesIO(audio_bytes), sr=16000, mono=True)
        waveform, _ = librosa.effects.trim(waveform, top_db=20)
        waveform = waveform / (np.max(np.abs(waveform)) + 1e-9)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio loading error: {str(e)}")

    try:
        # Compute log-mel spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=waveform,
            sr=16000,
            n_mels=80,
            n_fft=1024,
            hop_length=160,
            win_length=400
        )
        log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

        # Apply CMVN (per mel band)
        log_mel_spec = (log_mel_spec - np.mean(log_mel_spec, axis=1, keepdims=True)) / \
                       (np.std(log_mel_spec, axis=1, keepdims=True) + 1e-9)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spectrogram processing error: {str(e)}")

    # Prepare inputs
    input_tensor = np.expand_dims(log_mel_spec.astype(np.float32), axis=0)  # (1, 80, time)
    input_length = np.array([log_mel_spec.shape[-1]], dtype=np.int64)       # (1,)

    inputs = {
        "audio_signal": input_tensor,
        "length": input_length
    }

    try:
        # Inference
        logits = session.run(None, inputs)[0][0]               # (time, vocab)
        confidences = np.max(logits, axis=-1)                 # (time,)
        token_ids = np.argmax(logits, axis=-1)                # (time,)

        # Suppress low-confidence tokens
        threshold = -10
        filtered_ids = [
            tid if conf > threshold else 0
            for tid, conf in zip(token_ids, confidences)
        ]

        # Decode text
        transcription = decode_ids(filtered_ids)

        # Confidence summary
        avg_conf = float(np.mean(confidences))
        low_conf_count = int(np.sum(confidences <= threshold))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ONNX inference failed: {str(e)}")

    return {
        "transcription": transcription,
        "predicted_ids": list(map(int, filtered_ids)),
        "confidence_summary": {
            "average_confidence": round(avg_conf, 2),
            "low_confidence_tokens": low_conf_count,
            "total_tokens": len(confidences)
        }
    }
