"""analyst_queries._describe cells: abs_mean on every numeric column, share_at_cap on
`forecast` only (the engine clips the ensemble to [-20, 20]); the old keys and the
zero comparison charge are unchanged. Synthetic data only (2020 dates)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyst_queries as aq  # noqa: E402,F401
from test_e075_pr4_queries import engine, make_run  # noqa: E402

OLD_KEYS = ("n", "nan_share", "mean", "std", "p10", "p50", "p90")
PINNED = {0: 20.0, 1: -20.0, 2: 19.5, 3: -19.5, 4: 20.0, 5: np.nan}   # per window, first bars


@pytest.fixture()
def run(tmp_path):
    root = make_run(tmp_path / "run_001")
    for csv in sorted(root.glob("variants/base/results/*/bars.csv")):
        df = pd.read_csv(csv)
        for i, v in PINNED.items():
            df.loc[i, "forecast"] = v
        df.to_csv(csv, index=False)
    return root


def _forecasts(run):
    """Per window (in protocol order) the forecast column as written to disk."""
    return [pd.read_csv(p)["forecast"].to_numpy(float)
            for p in sorted(Path(run).glob("variants/base/results/*/bars.csv"))]


def test_abs_mean_matches_numpy_ungrouped_and_by_window(run):
    eng = engine(run)
    fcs = _forecasts(run)
    allv = np.concatenate(fcs)
    fin = allv[np.isfinite(allv)]
    assert (fin < 0).any()
    g = eng.describe("forecast")["result"]["groups"]["all"]
    assert g["abs_mean"] == aq.r8(np.abs(fin).mean()) and g["abs_mean"] != g["mean"]
    by_w = eng.describe("forecast", by="window")["result"]["groups"]
    for key, v in zip(["AAA/w0", "AAA/w1", "BBB/w0"], fcs):
        f = v[np.isfinite(v)]
        assert by_w[key]["abs_mean"] == aq.r8(np.abs(f).mean())
    # present on a non-forecast numeric column too
    close = eng.describe("close")["result"]["groups"]["all"]
    assert close["abs_mean"] == close["mean"]            # all positive


def test_share_at_cap_counts_both_signs_over_finite_values(run):
    eng = engine(run)
    allv = np.concatenate(_forecasts(run))
    fin = allv[np.isfinite(allv)]
    hand = int((np.abs(fin) >= 20.0 - 1e-9).sum())
    assert hand == 9                                     # +20, -20, +20 in each of 3 windows
    assert len(fin) == len(allv) - 3                     # the NaNs are out of the denominator
    g = eng.describe("forecast")["result"]["groups"]["all"]
    assert g["share_at_cap"] == aq.r8(hand / len(fin))
    assert g["nan_share"] == aq.r8(3 / len(allv))
    by_w = eng.describe("forecast", by="window")["result"]["groups"]
    for cell in by_w.values():
        assert cell["share_at_cap"] == aq.r8(3 / (cell["n"] - 1))      # one NaN a window


def test_share_at_cap_absent_for_other_columns(run):
    eng = engine(run)
    for col in ("close", "volume", "approved_rebalance"):
        for cell in eng.describe(col)["result"]["groups"].values():
            assert "share_at_cap" not in cell and "abs_mean" in cell
    for cell in eng.describe("close", by="window")["result"]["groups"].values():
        assert "share_at_cap" not in cell


def test_ungrouped_forecast_describe_charges_no_comparisons(run):
    eng = engine(run)
    assert eng.describe("forecast")["n_comparisons"] == 0
    assert eng.describe("forecast", by="window")["n_comparisons"] == 0
    assert eng.describe("forecast", by="coin")["n_comparisons"] == 0


def test_existing_keys_unchanged(run):
    eng = engine(run)
    allv = np.concatenate(_forecasts(run))
    fin = allv[np.isfinite(allv)]
    g = eng.describe("forecast")["result"]["groups"]["all"]
    assert all(k in g for k in OLD_KEYS)
    p10, p50, p90 = np.percentile(fin, [10, 50, 90])
    assert g["n"] == len(allv) and g["nan_share"] == aq.r8(1 - len(fin) / len(allv))
    assert g["mean"] == aq.r8(fin.mean()) and g["std"] == aq.r8(fin.std(ddof=1))
    assert (g["p10"], g["p50"], g["p90"]) == (aq.r8(p10), aq.r8(p50), aq.r8(p90))
