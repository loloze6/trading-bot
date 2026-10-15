"""
D-131 -- the composite fingerprint compares the TEST WINDOW's bars only.

The defect: tools/composite_cache.run_fingerprint used each window manifest's
`data.data_sha256`, a hash over EVERY row the run loaded, warm-up prefetch
included. The warm-up length follows each strategy's own lookback, so two
strategies on the same window with identical test bars (run_094: candidate
warm-up 2, composite SMA-100 warm-up 100) hashed differently and
composite_series / residual_ic_by_variant raised "different market data".

The fix: the fingerprint's data value is a hash of the OHLCV of the window's
bars.csv (test-window bars only).

Case 1: different warm-up (different manifest hash), identical test bars ->
        equal fingerprints; the composite-vs-candidate check and the
        same-coin-group check both pass.
Case 2: one close inside the test window differs -> fingerprints differ, the
        composite-vs-candidate check still raises CompositeError.
Case 3: a missing / empty / incomplete bars.csv -> CompositeError.

Sandbox: tests/conftest.py's autouse fixture. No market data, no network, no
backtest; the bars are synthetic and every date is in 2020.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import composite_cache as cc  # noqa: E402

# Two manifests that differ because the loads started at different bars
# (warm-up 2 vs warm-up 100); the test-window bars are identical.
MANIFEST_SHA_SHORT_WARMUP = "5c" * 32
MANIFEST_SHA_LONG_WARMUP = "a7" * 32
ENGINE = "b" * 40
N = 600


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _t60():
    import test_e060_s2_residual_ic as t60
    return t60


def _window(results_dir, wrid, forecasts, manifest_sha, git_sha=ENGINE):
    """One window dir: bars.csv holds the test-window bars (same bars whatever
    the warm-up), manifest.json carries the hash of ALL loaded rows, which
    differs with the warm-up."""
    t60 = _t60()
    t60._write_bars(Path(results_dir), wrid, forecasts, data_sha="3e" * 32, git_sha=git_sha)
    (Path(results_dir) / wrid / "manifest.json").write_text(
        json.dumps({"git_sha": git_sha, "data": {"data_sha256": manifest_sha}}), encoding="utf-8")


def _summary(wrid, symbol="BTCUSDT"):
    s = _t60()._summary(wrid)
    s["results"] = [{**s["results"][0], "symbol": symbol}]
    return s


def _manifest_sha(results_dir, wrid):
    return json.loads((Path(results_dir) / wrid / "manifest.json").read_text("utf-8"))[
        "data"]["data_sha256"]


def _two_strategies(tmp_path):
    t60 = _t60()
    cand = tmp_path / "cand" / "results"
    comp = tmp_path / "comp" / "results"
    _window(cand, "wr_cand", t60.Z_CAND[:N], MANIFEST_SHA_SHORT_WARMUP)
    _window(comp, "wr_comp", t60.Z_COMP[:N], MANIFEST_SHA_LONG_WARMUP)
    return cand, comp


def _change_one_close(results_dir, wrid, row=N // 2, bump=0.5):
    path = Path(results_dir) / wrid / "bars.csv"
    df = pd.read_csv(path)
    df.loc[row, "close"] = df.loc[row, "close"] + bump
    df.to_csv(path, index=False)


# --- Case 1 ---------------------------------------------------------------

def test_different_warmup_same_test_bars_have_equal_fingerprints(tmp_path):
    cand, comp = _two_strategies(tmp_path)
    assert _manifest_sha(cand, "wr_cand") != _manifest_sha(comp, "wr_comp")
    fp_cand = cc.run_fingerprint(_summary("wr_cand"), cand)
    fp_comp = cc.run_fingerprint(_summary("wr_comp"), comp)
    assert fp_cand == fp_comp
    assert set(fp_cand["data"]) == {"BTCUSDT|2020-01"}
    assert fp_cand["data"]["BTCUSDT|2020-01"] not in (MANIFEST_SHA_SHORT_WARMUP,
                                                      MANIFEST_SHA_LONG_WARMUP)


def _composite_fixture(tmp_path):
    t60 = _t60()
    rel, sha = t60._config_on_disk()
    proto = t60._write_protocol(rpr.ROOT, "p1h.json", t60._protocol())
    return rel, sha, proto


def test_composite_vs_candidate_check_passes_with_different_warmup(tmp_path):
    t60 = _t60()
    cand, _ = _two_strategies(tmp_path)
    candidate_fp = cc.run_fingerprint(_summary("wr_cand"), cand)
    rel, sha, proto = _composite_fixture(tmp_path)

    def runner(config_path, protocol_path, out_dir):
        _window(Path(out_dir) / "results", "wr_comp", t60.Z_COMP[:N], MANIFEST_SHA_LONG_WARMUP)
        (Path(out_dir) / "protocol_summary.json").write_text(json.dumps(_summary("wr_comp")),
                                                             encoding="utf-8")

    recs, _steps, cache_dir = cc.composite_series(
        t60._resolved(rel, sha), root=rpr.ROOT, protocol_path=proto,
        holdout_range=t60._seal(), candidate_fingerprint=candidate_fp, runner=runner)
    assert len(recs["BTCUSDT"]) == N - 1
    assert (cache_dir / "composite.yaml").exists()


def test_same_coin_group_with_different_warmup_does_not_raise(tmp_path):
    """The :428-435 path: two variants of one coin group whose loads started at
    different bars (different manifest hashes) but ran the same test bars."""
    t60 = _t60()
    rel, sha = t60._config_on_disk()
    reg = t60._registry_file([t60._block("H1:run_700", ref=rel, sha=sha)])
    proto = t60._write_protocol(rpr.ROOT, "p1h.json", t60._protocol())
    run_dir = rpr.ROOT / "runs" / "run_941"
    results, summaries = {}, {}
    for vid, manifest_sha in (("base", MANIFEST_SHA_SHORT_WARMUP),
                              ("design", MANIFEST_SHA_LONG_WARMUP)):
        res = run_dir / "variants" / vid / "results"
        _window(res, f"wr_{vid}", t60.Z_CAND[:N], manifest_sha)
        results[vid] = res
        summaries[vid] = _summary(f"wr_{vid}")
    calls = []

    def runner(config_path, protocol_path, out_dir):
        calls.append(1)
        _window(Path(out_dir) / "results", "wr_comp", t60.Z_COMP[:N], "9d" * 32)
        (Path(out_dir) / "protocol_summary.json").write_text(json.dumps(_summary("wr_comp")),
                                                             encoding="utf-8")

    doc = cc.residual_ic_by_variant(
        summaries, results, root=rpr.ROOT, protocol_path=proto, registry_path=reg,
        compositions_path=rpr.ROOT / "campaign_record" / "compositions.yaml",
        holdout_range=t60._seal(), runner=runner)
    assert len(calls) == 1  # one composite served both variants
    assert sorted(doc["variants"]) == ["base", "design"]


# --- Case 2 ---------------------------------------------------------------

def test_one_changed_close_changes_the_fingerprint(tmp_path):
    cand, comp = _two_strategies(tmp_path)
    before = cc.run_fingerprint(_summary("wr_comp"), comp)
    _change_one_close(comp, "wr_comp")
    after = cc.run_fingerprint(_summary("wr_comp"), comp)
    assert after["git_sha"] == before["git_sha"]
    assert after["data"] != before["data"]


def _perturb_bars(path, kind):
    """One change inside the test window's bars.csv, with non-default values."""
    df = pd.read_csv(path)
    mid = N // 2
    if kind == "timestamp":
        df.loc[mid, "timestamp"] = "2020-01-05 03:30:00"
    elif kind in ("open", "high", "low", "close", "volume"):
        df.loc[mid, kind] = df.loc[mid, kind] + 0.37
    elif kind == "drop_row":
        df = df.drop(index=mid).reset_index(drop=True)
    elif kind == "add_row":
        extra = df.iloc[[mid]].copy()
        extra["timestamp"] = "2020-02-01 00:00:00"
        df = pd.concat([df, extra], ignore_index=True)
    else:
        raise AssertionError(kind)
    df.to_csv(path, index=False)


@pytest.mark.parametrize("kind", ["timestamp", "open", "high", "low", "close", "volume",
                                  "drop_row", "add_row"])
def test_any_test_window_bar_change_changes_the_fingerprint(tmp_path, kind):
    """Every fingerprint column, and a dropped or an added bar row, must move the
    fingerprint's data value (not just a changed close)."""
    _, comp = _two_strategies(tmp_path)
    before = cc.run_fingerprint(_summary("wr_comp"), comp)
    _perturb_bars(comp / "wr_comp" / "bars.csv", kind)
    after = cc.run_fingerprint(_summary("wr_comp"), comp)
    assert after["data"] != before["data"]


def test_composite_vs_candidate_check_still_raises_on_different_bars(tmp_path):
    t60 = _t60()
    cand, _ = _two_strategies(tmp_path)
    candidate_fp = cc.run_fingerprint(_summary("wr_cand"), cand)
    rel, sha, proto = _composite_fixture(tmp_path)

    def runner(config_path, protocol_path, out_dir):
        _window(Path(out_dir) / "results", "wr_comp", t60.Z_COMP[:N], MANIFEST_SHA_LONG_WARMUP)
        _change_one_close(Path(out_dir) / "results", "wr_comp")
        (Path(out_dir) / "protocol_summary.json").write_text(json.dumps(_summary("wr_comp")),
                                                             encoding="utf-8")

    with pytest.raises(cc.CompositeError, match="different market data"):
        cc.composite_series(
            t60._resolved(rel, sha), root=rpr.ROOT, protocol_path=proto,
            holdout_range=t60._seal(), candidate_fingerprint=candidate_fp, runner=runner)


# --- Case 3 ---------------------------------------------------------------

def test_missing_bars_csv_raises(tmp_path):
    _, comp = _two_strategies(tmp_path)
    (comp / "wr_comp" / "bars.csv").unlink()
    with pytest.raises(cc.CompositeError, match="bars.csv"):
        cc.run_fingerprint(_summary("wr_comp"), comp)


def test_empty_bars_csv_raises(tmp_path):
    _, comp = _two_strategies(tmp_path)
    path = comp / "wr_comp" / "bars.csv"
    path.write_text(path.read_text(encoding="utf-8").splitlines()[0] + "\n", encoding="utf-8")
    with pytest.raises(cc.CompositeError, match="no bar rows"):
        cc.run_fingerprint(_summary("wr_comp"), comp)


def test_bars_csv_without_an_ohlcv_column_raises(tmp_path):
    _, comp = _two_strategies(tmp_path)
    path = comp / "wr_comp" / "bars.csv"
    pd.read_csv(path).drop(columns=["volume"]).to_csv(path, index=False)
    with pytest.raises(cc.CompositeError, match="needs the columns"):
        cc.run_fingerprint(_summary("wr_comp"), comp)


def test_the_existing_raises_are_kept(tmp_path):
    _, comp = _two_strategies(tmp_path)
    manifest = comp / "wr_comp" / "manifest.json"
    manifest.write_text(json.dumps({"data": {"data_sha256": "1" * 64}}), encoding="utf-8")
    with pytest.raises(cc.CompositeError, match="no git_sha"):
        cc.run_fingerprint(_summary("wr_comp"), comp)
    manifest.unlink()
    with pytest.raises(cc.CompositeError, match="manifest.json"):
        cc.run_fingerprint(_summary("wr_comp"), comp)
    with pytest.raises(cc.CompositeError, match="no window"):
        cc.run_fingerprint({"results": []}, comp)
    _window(comp, "wr_other", _t60().Z_COMP[:N], "7" * 64, git_sha="c" * 40)
    two = {"results": [_summary("wr_comp")["results"][0],
                       {**_summary("wr_other")["results"][0], "window": "2020-02"}]}
    _window(comp, "wr_comp", _t60().Z_COMP[:N], "7" * 64)
    with pytest.raises(cc.CompositeError, match="different engine versions"):
        cc.run_fingerprint(two, comp)
