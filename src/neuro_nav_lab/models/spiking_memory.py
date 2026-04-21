from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class SpikeState:
    membrane: np.ndarray
    trace: np.ndarray
    rate: np.ndarray

class SpikingTemporalMemory:
    '''
    Lightweight surrogate for a LIF-style temporal encoder. The goal here is not
    to claim biological fidelity; the module acts as a compact state accumulator
    that records short-horizon obstacle pressure and directional asymmetry.
    '''
    def __init__(self, n_features: int, decay: float = 0.82, threshold: float = 0.58):
        self.decay = float(decay)
        self.threshold = float(threshold)
        self.state = SpikeState(
            membrane=np.zeros(n_features, dtype=float),
            trace=np.zeros(n_features, dtype=float),
            rate=np.zeros(n_features, dtype=float),
        )

    def reset(self):
        self.state.membrane[:] = 0.0
        self.state.trace[:] = 0.0
        self.state.rate[:] = 0.0

    def step(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        x = np.asarray(x, dtype=float)
        st = self.state
        st.membrane = self.decay * st.membrane + (1.0 - self.decay) * x
        spikes = (st.membrane > self.threshold).astype(float)
        st.membrane = st.membrane * (1.0 - 0.55 * spikes)
        st.trace = 0.92 * st.trace + spikes
        st.rate = 0.90 * st.rate + 0.10 * spikes
        return spikes, self.embedding()

    def embedding(self) -> np.ndarray:
        st = self.state
        return np.concatenate([st.membrane, st.trace, st.rate], axis=0)
