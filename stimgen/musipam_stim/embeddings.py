"""Learned motif representations from a pretrained music transformer.

MERT-v1-95M (Li et al., 2024; ``m-a-p/MERT-v1-95M`` on HuggingFace) is a
transformer trained self-supervised on ~160k hours of music. It plays the
role Word2Vec plays in PAM: a representation learned without knowledge of
our stimuli, so model tests built on it cannot be circular.

Each motif is cut from the stimulus audio participants actually hear and
embedded on its own (no context), so relations cannot leak into node vectors.
Inference runs on CPU for bit-for-bit reproducibility of frozen predictions.
The remote model code is pinned to an audited revision.
"""
from __future__ import annotations

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

MERT_MODEL = "m-a-p/MERT-v1-95M"
MERT_REVISION = "12af15fef9d0ac838c3f475bfbbf26d2060dd4f5"  # audited 2026-11-06: no I/O, network or exec
MERT_SR = 24000
FADE_S = 0.01


def load_mert():
    """Load the pinned model, verify every pretrained weight loaded, and hook
    all 13 layer outputs (transformers 5 no longer returns ``hidden_states``
    through MERT's remote code; the hooks recover exactly what it returned:
    the input to layer 1 plus each layer's output)."""
    import torch
    from transformers import AutoModel, Wav2Vec2FeatureExtractor
    torch.manual_seed(0)
    model, info = AutoModel.from_pretrained(MERT_MODEL, revision=MERT_REVISION, trust_remote_code=True,
                                            output_loading_info=True)
    bad = {k: sorted(map(str, info.get(k, []))) for k in ("missing_keys", "unexpected_keys", "mismatched_keys")}
    if any(bad.values()):
        raise RuntimeError(f"MERT weights did not load cleanly: {bad}")
    proc = Wav2Vec2FeatureExtractor.from_pretrained(MERT_MODEL, revision=MERT_REVISION, trust_remote_code=True)
    model.eval()
    caps: dict = {}
    layers = model.encoder.layers

    def pre_hook(_mod, args, kwargs):
        caps[0] = (args[0] if args else kwargs["hidden_states"]).detach()

    def make_hook(i):
        def hook(_mod, _args, out):
            caps[i + 1] = (out[0] if isinstance(out, (tuple, list)) else out).detach()
        return hook

    layers[0].register_forward_pre_hook(pre_hook, with_kwargs=True)
    for i, layer in enumerate(layers):
        layer.register_forward_hook(make_hook(i))
    model._musipam_caps = caps
    model._musipam_n = len(layers) + 1
    return model, proc


def load_mono_24k(wav_path) -> np.ndarray:
    x, sr = sf.read(str(wav_path), always_2d=True, dtype="float64")
    x = x.mean(axis=1)
    if sr != 44100:
        raise ValueError(f"{wav_path}: expected 44.1 kHz, got {sr}")
    return resample_poly(x, 80, 147)  # 44100 -> 24000 exactly


def slice_motif(x24: np.ndarray, start_s: float, dur_s: float) -> np.ndarray:
    a, b = int(round(start_s * MERT_SR)), int(round((start_s + dur_s) * MERT_SR))
    seg = x24[a:b].copy()
    nf = int(FADE_S * MERT_SR)
    seg[:nf] *= np.linspace(0, 1, nf)
    seg[-nf:] *= np.linspace(1, 0, nf)
    return seg


def embed_clip(model, proc, clip: np.ndarray) -> np.ndarray:
    """Time-pooled hidden states of every layer: array [n_layers, dim]."""
    import torch
    caps = model._musipam_caps
    caps.clear()
    inputs = proc(clip.astype(np.float32), sampling_rate=MERT_SR, return_tensors="pt")
    with torch.no_grad():
        model(**inputs)
    hs = torch.stack([caps[i] for i in range(model._musipam_n)]).squeeze(1)  # [layers, frames, dim]
    return hs.mean(dim=1).numpy().astype(np.float32)


def node_code(layer_stack: np.ndarray) -> np.ndarray:
    """Confirmatory MERT node code: mean over all layers, unit-normalized.
    (Layer-wise codes are exploratory.)"""
    v = layer_stack.mean(axis=0).astype(np.float64)
    return v / np.linalg.norm(v)
