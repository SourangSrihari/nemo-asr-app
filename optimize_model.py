from nemo.collections.asr.models import EncDecCTCModel

# Load the model from the local .nemo file
model = EncDecCTCModel.restore_from("stt_hi_conformer_ctc_medium.nemo")

# (Optional) Ensure CPU-safe export
model.to('cpu')

# Export to ONNX format
model.export("asr_model.onnx")

