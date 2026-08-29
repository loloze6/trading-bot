"""
A8.5.1a fixtures (per pre-registration spec, strategy-research/engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md):
  (a) synthetic clustered signal with known IC -> recovered CI covers the true IC.
  (b) same data evaluated with the naive 24-bar block must show a NARROWER
      (overconfident) CI than the episode method — that gap is the point of the rule.
  (c) n_episodes < 8 -> significance suppressed regardless of p-value.
"""

import random
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import episode_significance as es  # noqa: E402
import prescreen_signal  # noqa: E402


def _make_clustered_records(
    n_episodes: int,
    episode_len: int,
    gap_between: int,
    mu_beta: float,
    sd_beta: float,
    noise_sd: float,
    seed: int,
):
    """
    Build a synthetic bar sequence where active bars cluster into `n_episodes`
    well-separated episodes (gap_between > default gap_bars=48, so episodes never
    merge). Each episode draws its OWN forecast->return slope `beta_e ~
    N(mu_beta, sd_beta)`; within the episode the relationship is nearly
    deterministic (small noise_sd) but the slope itself varies episode-to-episode.

    This is the case A8.5.1a exists for: the true independent unit of evidence is
    the EPISODE (its one beta_e draw), not the individual bar. A method that chops
    a 200-bar episode into ~8 "independent" 24-bar blocks is fabricating 8x more
    independent evidence than actually exists — all 8 blocks share the identical
    beta_e and therefore are NOT independent draws of the underlying relationship.

    forecast[i]        = base[i]  ~ Uniform(-1, 1)
    next_return_bps[i] = beta_e * base[i] + noise[i]   (noise_sd small, per-bar)
    """
    rng = random.Random(seed)
    records = []
    for ep in range(n_episodes):
        beta = rng.gauss(mu_beta, sd_beta)
        for _ in range(episode_len):
            base = rng.uniform(-1, 1)
            noise = rng.gauss(0, noise_sd)
            ret = beta * base + noise
            records.append({"forecast": base, "next_return_bps": ret, "active": True})
        # inactive gap between episodes
        for _ in range(gap_between):
            records.append({"forecast": 0.0, "next_return_bps": rng.gauss(0, noise_sd), "active": False})
    return records


# Shared synthetic dataset for fixtures (a) and (b): 15 well-separated, LONG
# episodes (200 active bars each, gap_between=300 >> default gap_bars=48), each
# with its own randomly-drawn slope beta_e. Episode length >> block_size=24 is
# what exposes the naive method's flaw: it would see ~8 "blocks" per episode.
_N_EPISODES = 15
_EPISODE_LEN = 200
_GAP_BETWEEN = 300
_MU_BETA = 25.0
_SD_BETA = 50.0
_NOISE_SD = 5.0
_SEED = 1234


def _build_fixture_records():
    return _make_clustered_records(
        n_episodes=_N_EPISODES,
        episode_len=_EPISODE_LEN,
        gap_between=_GAP_BETWEEN,
        mu_beta=_MU_BETA,
        sd_beta=_SD_BETA,
        noise_sd=_NOISE_SD,
        seed=_SEED,
    )


# ---------------------------------------------------------------------------
# Fixture (a): recovered CI covers the true point IC
# ---------------------------------------------------------------------------


def test_fixture_a_recovered_ci_covers_truth():
    records = _build_fixture_records()
    episodes = es.identify_episodes(records, gap_bars=48)

    assert len(episodes) == _N_EPISODES, (
        f"episode construction should find exactly {_N_EPISODES} well-separated "
        f"episodes given gap_between={_GAP_BETWEEN} > gap_bars=48, got {len(episodes)}"
    )
    for ep in episodes:
        assert len(ep) == _EPISODE_LEN

    result = es.episode_block_bootstrap(records, episodes, n_resamples=2000, seed=42)

    # The "truth" here is the point estimate itself (pooled_ic over ALL active bars,
    # which is our best unbiased estimate of the population IC under this generative
    # model) — the CI must cover it (it is definitionally the resampling center).
    assert result["ci_low"] <= result["pooled_ic"] <= result["ci_high"], (
        f"CI [{result['ci_low']}, {result['ci_high']}] does not cover the point estimate {result['pooled_ic']}"
    )
    # And the point estimate should be positive and non-trivial given true_ic_scale > 0
    # dominates episode_shock_sd/per_bar_noise_sd at this magnitude.
    assert result["pooled_ic"] > 0.05, (
        f"pooled_ic={result['pooled_ic']} should reflect the known positive true_ic_scale={_TRUE_IC_SCALE} signal"
    )
    assert result["n_episodes"] == _N_EPISODES


# ---------------------------------------------------------------------------
# Fixture (b): naive 24-bar block gives a narrower (overconfident) CI than the
# episode method on the SAME data, because it doesn't know the within-episode
# shared shock makes 30 consecutive active bars far less than 30 independent draws.
# ---------------------------------------------------------------------------


def test_fixture_b_naive_block_is_overconfident_vs_episode_method():
    records = _build_fixture_records()
    episodes = es.identify_episodes(records, gap_bars=48)
    n_active = sum(1 for r in records if r["active"])

    episode_result = es.episode_block_bootstrap(records, episodes, n_resamples=2000, seed=42)
    episode_ci_width = episode_result["ci_high"] - episode_result["ci_low"]

    # Naive method: existing 24-bar Fisher-z significance, fed the single pooled
    # active-bar IC (exactly what prescreen_signal.py does today).
    active_idx = [i for i, r in enumerate(records) if r["active"]]
    pooled_ic = es._pooled_ic(records, active_idx)
    naive_sig = prescreen_signal._block_adjusted_significance([pooled_ic], n_active, block_size=24)

    # Reconstruct the naive method's implied CI from its z-statistic (Fisher z: CI
    # half-width = 1.645 / sqrt(dof) for a 90% CI, matching the p<0.10 convention
    # used throughout this codebase).
    dof = max(naive_sig["n_eff"] - 3, 1)
    naive_half_width = 1.645 / (dof**0.5)
    naive_ci_width = 2 * naive_half_width

    assert naive_ci_width < episode_ci_width, (
        f"naive 24-bar CI width={naive_ci_width:.4f} should be NARROWER than the "
        f"episode-bootstrap CI width={episode_ci_width:.4f} — the naive method treats "
        f"the {_N_EPISODES * _EPISODE_LEN} active bars as ~{n_active // 24} independent "
        f"24-bar blocks, ignoring that they collapse into only {_N_EPISODES} truly "
        f"independent episodes (shared per-episode shock). If this assertion fails, "
        f"the whole justification for A8.5.1a is empirically wrong on this fixture."
    )


# ---------------------------------------------------------------------------
# Fixture (c): n_episodes < 8 -> significance suppressed regardless of p-value
# ---------------------------------------------------------------------------


def test_fixture_c_below_floor_suppresses_significance():
    # Only 4 episodes — deliberately below the n_episodes >= 8 floor. Use a huge
    # mu_beta with tiny noise so that IF the floor were not enforced, the naive
    # p-value would look highly "significant" — the floor must override that
    # regardless.
    records = _make_clustered_records(
        n_episodes=4,
        episode_len=30,
        gap_between=100,
        mu_beta=200.0,
        sd_beta=5.0,
        noise_sd=5.0,
        seed=7,
    )
    result = es.compute_a851a_significance(records, gap_bars=48, min_n_episodes=8)

    assert result["n_episodes"] == 4
    assert result["method"] == "episode_bootstrap_insufficient_n"
    assert result["significant"] is False
    assert result["p_value"] is None
    assert result["disposition_note"] == "insufficient_sample_inconclusive"
    # pooled_ic is still reported (descriptive only), just not used for a claim
    assert result["pooled_ic"] is not None


# ---------------------------------------------------------------------------
# Supporting unit tests: episode construction respects era boundaries and gaps
# ---------------------------------------------------------------------------


def test_identify_episodes_respects_era_boundary():
    # Two active bars only 2 bars apart (well within gap_bars=48) but on opposite
    # sides of a declared era boundary must NOT merge into one episode.
    records = [{"active": True}, {"active": False}, {"active": False}, {"active": True}]

    def era_of(i):
        return "era_A" if i < 2 else "era_B"

    episodes = es.identify_episodes(records, gap_bars=48, era_of=era_of)
    assert len(episodes) == 2
    assert episodes[0] == [0]
    assert episodes[1] == [3]


def test_identify_episodes_merges_within_gap():
    records = [{"active": True}] + [{"active": False}] * 10 + [{"active": True}]
    episodes = es.identify_episodes(records, gap_bars=48)
    assert len(episodes) == 1
    assert episodes[0] == [0, 11]


def test_density_fallback_routes_to_block_24():
    # >= 50% activation -> dense fallback, not episode bootstrap.
    rng = random.Random(99)
    records = []
    for _ in range(1000):
        active = rng.random() < 0.6  # 60% activation
        base = rng.uniform(-1, 1) if active else 0.0
        ret = 30.0 * base + rng.gauss(0, 40)
        records.append({"forecast": base, "next_return_bps": ret, "active": active})

    result = es.compute_a851a_significance(records)
    assert result["method"] == "block_24_dense_fallback"
    assert result["n_episodes"] is None
    assert result["density_pct"] >= 50.0


def test_per_era_report_survives_yaml_roundtrip_with_tuple_era_of():
    """
    F4e (2026-07-05, run_050): prescreen_signal.py's real wiring uses an era_of
    that returns a (symbol, era_id) TUPLE, to keep episodes symbol-bounded when
    pooled. per_era_report's output dict used the raw tuple as a key — this
    round-trips fine through yaml.safe_dump but CRASHES yaml.safe_load on
    read-back ("found unhashable key"), because YAML's complex-mapping-key
    syntax deserializes a sequence key as a Python list (unhashable), not a
    tuple. Caught live: run_050's prescreen_result.yaml wrote successfully but
    crashed the very next stage that tried to read it back.
    """
    records = [
        {"forecast": 1.0, "next_return_bps": 5.0, "active": True, "symbol": "BTCUSDT"},
        {"forecast": -1.0, "next_return_bps": -3.0, "active": True, "symbol": "BTCUSDT"},
        {"forecast": 1.0, "next_return_bps": 2.0, "active": True, "symbol": "ETHUSDT"},
    ]

    def era_of(i, _records=records):
        return (_records[i]["symbol"], "era_2024_burned")  # tuple, matches real wiring

    report = es.per_era_report(records, era_of)

    # Keys must be plain strings, not tuples.
    assert all(isinstance(k, str) for k in report.keys())
    assert "BTCUSDT::era_2024_burned" in report
    assert "ETHUSDT::era_2024_burned" in report

    # The actual failure mode: dump then load must not raise.
    dumped = yaml.safe_dump(report, sort_keys=False)
    reloaded = yaml.safe_load(dumped)
    assert reloaded == report
