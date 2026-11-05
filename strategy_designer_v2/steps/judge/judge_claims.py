"""The claim judge, try 02: measure three claims of fake brief 01 on real hourly bars, one fold.

Code only, no AI. The pass rule applied to every claim:
  - the claim's own numeric threshold, on the whole fold;
  - the sign of the claim's effect holds in at least 5 of the fold's 6 windows;
  - the claim's own minimum number of events;
  - cost: the engine's Kraken BTC cost, 5 bps fee + 2.5 bps slippage per leg = 0.15% per round trip.
Windows are reported as W1..W6, never as dates. The sealed holdout range is read through
the policy reader and masked out of the data; it is never printed.

Reused from v1 (by hand, with a reason): tools/research_folds.py (the fold loader, so a fold here
is the same fold as in v1) and tools/holdout_policy.py (the seal: the range comes from the policy file).
"""
import sys, pathlib, datetime as dt
import numpy as np, pandas as pd, yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
SR_TOOLS = ROOT / "strategy-research" / "tools"
sys.path.insert(0, str(SR_TOOLS))
import research_folds as rf  # noqa: E402

FEE_RT = 0.0015            # 0.15% per round trip (engine cost model, kraken BTCUSD)
WINDOWS_MUST_AGREE = 5     # of 6
FOLD = sys.argv[1] if len(sys.argv) > 1 else "A"
SYMBOL = "BTCUSD"
DATA = ROOT / "trading-bot" / "local_data" / f"kraken_{SYMBOL}_1h.csv"
OUT = ROOT / "strategy_designer_v2" / "tries" / "try_02" / "verdicts.yaml"
LEDGER = ROOT / "strategy_designer_v2" / "records" / "trials.yaml"


def load_bars() -> pd.DataFrame:
    df = pd.read_csv(DATA, usecols=["timestamp", "close", "volume"], parse_dates=["timestamp"])
    df = df.sort_values("timestamp").drop_duplicates("timestamp").set_index("timestamp")
    # Mask the sealed holdout: the range is read from the policy, never written out.
    hs, he = rf.policy_ranges()["holdout"]
    sealed = (df.index >= pd.Timestamp(hs)) & (df.index <= pd.Timestamp(he) + pd.Timedelta(days=1))
    df.loc[sealed, ["close", "volume"]] = np.nan
    return df


def features(df: pd.DataFrame) -> pd.DataFrame:
    r = df["close"].pct_change()
    med_abs = r.abs().rolling(168, min_periods=168).median().shift(1)   # prior 168 bars
    med_vol = df["volume"].rolling(168, min_periods=168).median().shift(1)
    big = (r.abs() >= 3 * med_abs)
    # one event per 24 bars: keep a big bar only if no big bar in the prior 24 bars
    prior = big.shift(1).rolling(24, min_periods=1).max().fillna(0).astype(bool)
    event = big & ~prior
    out = pd.DataFrame({
        "r": r, "sign": np.sign(r), "event": event,
        "vol_ratio": df["volume"] / med_vol,
        "fwd24": df["close"].shift(-24) / df["close"] - 1,
        "fwd12": df["close"].shift(-12) / df["close"] - 1,
    }, index=df.index)
    out["s24"] = -out["sign"] * out["fwd24"]   # signed against the bar's own direction
    out["s12"] = -out["sign"] * out["fwd12"]
    return out


def in_windows(index: pd.DatetimeIndex, windows: list) -> pd.Series:
    """Window number (1..6) of each bar, 0 outside the fold."""
    w = pd.Series(0, index=index)
    for i, win in enumerate(windows, start=1):
        s, e = pd.Timestamp(win["test"]["start"]), pd.Timestamp(win["test"]["end"]) + pd.Timedelta(days=1)
        w[(index >= s) & (index < e)] = i
    return w


def per_window(mask_a, mask_b, col, f, wn):
    """Difference of means (a minus b) of column `col`, per window and overall, plus counts."""
    rows = []
    for i in range(1, 7):
        a = f.loc[mask_a & (wn == i), col].dropna(); b = f.loc[mask_b & (wn == i), col].dropna()
        rows.append({"window": f"W{i}", "n_a": int(len(a)), "n_b": int(len(b)),
                     "mean_a": float(a.mean()) if len(a) else None,
                     "diff": float(a.mean() - b.mean()) if len(a) and len(b) else None})
    A = f.loc[mask_a & (wn > 0), col].dropna(); B = f.loc[mask_b & (wn > 0), col].dropna()
    return rows, {"n_a": int(len(A)), "n_b": int(len(B)), "mean_a": float(A.mean()), "mean_b": float(B.mean()),
                  "diff": float(A.mean() - B.mean())}


def agree(rows, key, want_positive=True):
    vals = [r[key] for r in rows if r[key] is not None]
    return sum(1 for v in vals if (v > 0) == want_positive), len(vals)


def judge(f, wn):
    ev = f["event"].fillna(False)
    verdicts = {}

    # 1. large_bar_fade_baseline: events vs all other bars, s24; event mean - base >= 0.30%,
    #    event mean >= 0.40% gross, >= 100 events, net positive in >= 5 of 6 windows.
    rows, tot = per_window(ev, ~ev, "s24", f, wn)
    net_pos, n_w = agree([{"net": (r["mean_a"] - FEE_RT) if r["mean_a"] is not None else None} for r in rows], "net")
    checks = {"diff_ge_0.30%": tot["diff"] >= 0.0030, "event_mean_ge_0.40%": tot["mean_a"] >= 0.0040,
              "events_ge_100": tot["n_a"] >= 100, f"net_positive_in_{WINDOWS_MUST_AGREE}_of_6": net_pos >= WINDOWS_MUST_AGREE}
    verdicts["large_bar_fade_baseline"] = {"fold_totals": tot, "windows": rows,
                                           "net_positive_windows": f"{net_pos} of {n_w}",
                                           "checks": checks, "verdict": "pass" if all(checks.values()) else "fail"}

    # 2. low_volume_shock_reverts_more: events with vol < median vs events with vol >= 2x median, s24;
    #    diff >= 0.40%, same sign in >= 5 of 6, >= 30 per group, low-vol mean net positive.
    low = ev & (f["vol_ratio"] < 1.0); high = ev & (f["vol_ratio"] >= 2.0)
    rows, tot = per_window(low, high, "s24", f, wn)
    same, n_w = agree(rows, "diff", want_positive=(tot["diff"] > 0))
    checks = {"diff_ge_0.40%": tot["diff"] >= 0.0040, f"same_sign_in_{WINDOWS_MUST_AGREE}_of_6": same >= WINDOWS_MUST_AGREE,
              "min_30_per_group": min(tot["n_a"], tot["n_b"]) >= 30, "low_vol_mean_net_positive": tot["mean_a"] - FEE_RT > 0}
    verdicts["low_volume_shock_reverts_more"] = {"fold_totals": tot, "windows": rows,
                                                 "same_sign_windows": f"{same} of {n_w}",
                                                 "checks": checks, "verdict": "pass" if all(checks.values()) else "fail"}

    # 3. volume_climax_exhaustion: events with vol >= 4x median vs other events, s12;
    #    diff >= 0.30%, same sign in >= 5 of 6, >= 30 climax events, climax net positive in >= 5 of 6.
    climax = ev & (f["vol_ratio"] >= 4.0); other = ev & (f["vol_ratio"] < 4.0)
    rows, tot = per_window(climax, other, "s12", f, wn)
    same, n_w = agree(rows, "diff", want_positive=(tot["diff"] > 0))
    net_pos, _ = agree([{"net": (r["mean_a"] - FEE_RT) if r["mean_a"] is not None else None} for r in rows], "net")
    checks = {"diff_ge_0.30%": tot["diff"] >= 0.0030, f"same_sign_in_{WINDOWS_MUST_AGREE}_of_6": same >= WINDOWS_MUST_AGREE,
              "climax_events_ge_30": tot["n_a"] >= 30, f"climax_net_positive_in_{WINDOWS_MUST_AGREE}_of_6": net_pos >= WINDOWS_MUST_AGREE}
    verdicts["volume_climax_exhaustion"] = {"fold_totals": tot, "windows": rows,
                                            "same_sign_windows": f"{same} of {n_w}",
                                            "climax_net_positive_windows": f"{net_pos} of {n_w}",
                                            "checks": checks, "verdict": "pass" if all(checks.values()) else "fail"}
    return verdicts


def main():
    windows = rf.load_fold_windows(FOLD)
    df = load_bars()
    f = features(df)
    wn = in_windows(f.index, windows)
    verdicts = judge(f, wn)
    doc = {"try": "try_02", "brief": "fake_01_btc_overreaction.md", "symbol": SYMBOL, "fold": FOLD,
           "windows": 6, "rule": f"claim threshold on the fold, same sign in >= {WINDOWS_MUST_AGREE} of 6 windows, "
                                 f"claim's minimum events, cost {FEE_RT:.4%} per round trip",
           "bars_in_fold": int((wn > 0).sum()), "claims": verdicts}
    OUT.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    # Trial ledger: one row per claim measured on market data (scar 5).
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {"trials": []}
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for cid, v in verdicts.items():
        ledger["trials"].append({"at": stamp, "try": "try_02", "claim": cid, "symbol": SYMBOL, "fold": FOLD,
                                 "verdict": v["verdict"], "result": str(OUT.relative_to(ROOT))})
    LEDGER.write_text(yaml.safe_dump(ledger, sort_keys=False), encoding="utf-8")
    for cid, v in verdicts.items():
        t = v["fold_totals"]
        print(f"{cid}: {v['verdict'].upper()}  n_a={t['n_a']} n_b={t['n_b']} mean_a={t['mean_a']:+.4%} diff={t['diff']:+.4%}  "
              + ", ".join(f"{k}={'ok' if ok else 'NO'}" for k, ok in v["checks"].items()))
    print(f"bars in fold {FOLD}: {int((wn > 0).sum())}; written {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
