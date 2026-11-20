"""Topic 33 (2026-11-20): compute_a851a_significance(method_only=True) gives the label of the full call, on each of
its three paths (dense fallback, too few episodes, episode bootstrap), without computing the numbers."""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backtest"))
import episode_significance as es  # noqa: E402


def _records(active_every, n=600, burst=1, seed=0):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        active = (i // burst) % active_every == 0
        out.append({"forecast": rng.gauss(0, 1) if active else 0.0, "next_return_bps": rng.gauss(0, 10),
                    "active": active})
    return out


def _both(records):
    full = es.compute_a851a_significance(records, block_size=24, n_resamples=50, seed=1)
    label = es.compute_a851a_significance(records, block_size=24, n_resamples=50, seed=1, method_only=True)
    return full, label


def test_dense_path():
    full, label = _both(_records(active_every=1))
    assert full["method"] == "block_24_dense_fallback"
    assert label == {"method": full["method"]}


def test_insufficient_episodes_path():
    recs = _records(active_every=1000, n=600, burst=5)     # one burst only: one episode
    full, label = _both(recs)
    assert full["method"] == "episode_bootstrap_insufficient_n"
    assert label == {"method": full["method"]}


def test_bootstrap_path():
    recs = _records(active_every=50, n=3000, burst=3)      # sparse bursts: about 20 episodes
    full, label = _both(recs)
    assert full["method"] == "episode_block_bootstrap"
    assert label == {"method": full["method"]}
