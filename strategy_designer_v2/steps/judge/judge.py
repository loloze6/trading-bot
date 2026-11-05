"""The generic claim judge. Reads a claims file written in CLAIM_FORMAT terms, measures every claim
on one fold for each symbol the brief names, applies the common rule, writes verdicts and trial rows.
Code only. Usage: python3 steps/judge/judge.py <claims.yaml> <fold> <bar_size> <SYMBOL> [SYMBOL ...]
Windows are reported as W1..W6, never as dates. The sealed range is masked and never printed."""
import sys, re, pathlib, datetime as dt
import numpy as np, pandas as pd, yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "strategy-research" / "tools"))
import research_folds as rf  # noqa: E402

FEE_RT, AGREE, MIN_BARS, N_WIN = 0.0015, 5, 30, 6
MEASURES = {"mean_diff", "abs_ratio", "rank_corr", "hit_rate", "net_return"}
FORBIDDEN = re.compile(r"shift\(\s*-|center\s*=\s*True|\[::-1\]|import\s|open\(|exec\(|eval\(")
LEDGER = ROOT / "strategy_designer_v2" / "records" / "trials.yaml"


def load_bars(symbol, bar_size):
    path = ROOT / "trading-bot" / "local_data" / f"kraken_{symbol}_{bar_size}.csv"
    df = pd.read_csv(path, usecols=["timestamp", "open", "high", "low", "close", "volume"], parse_dates=["timestamp"])
    df = df.sort_values("timestamp").drop_duplicates("timestamp").set_index("timestamp")
    hs, he = rf.policy_ranges()["holdout"]
    sealed = (df.index >= pd.Timestamp(hs)) & (df.index <= pd.Timestamp(he) + pd.Timedelta(days=1))
    df.loc[sealed, ["open", "high", "low", "close", "volume"]] = np.nan
    return df


def window_numbers(index, windows):
    w = pd.Series(0, index=index)
    for i, win in enumerate(windows, start=1):
        s, e = pd.Timestamp(win["test"]["start"]), pd.Timestamp(win["test"]["end"]) + pd.Timedelta(days=1)
        w[(index >= s) & (index < e)] = i
    return w


def spaced(cond, n):
    cond = cond.fillna(False).astype(bool)
    prior = cond.shift(1).rolling(n, min_periods=1).max().fillna(0).astype(bool)
    return cond & ~prior


def run_code(code, df):
    ns = {"df": df, "ret": df["close"].pct_change(), "hour": pd.Series(df.index.hour, index=df.index),
          "dow": pd.Series(df.index.dayofweek, index=df.index), "spaced": spaced, "pd": pd, "np": np}
    exec(code, ns)  # the claim's own few lines; our model, our sandbox
    a = ns.get("a"); b = ns.get("b"); signal = ns.get("signal"); feature = ns.get("feature")
    if not isinstance(a, pd.Series):
        raise ValueError("code must define a boolean Series `a`")
    return a.reindex(df.index).fillna(False).astype(bool), \
        (b.reindex(df.index).fillna(False).astype(bool) if isinstance(b, pd.Series) else None), signal, feature


def effect(measure, a, b, y, signal, feature, mask):
    """The measure's value on `mask`, plus the counts of a and b used."""
    A = a & mask; B = (b & mask) if b is not None else None
    if measure == "mean_diff":
        ya = (signal * y)[A].dropna(); yb = (signal * y)[B].dropna()
        return ya.mean() - yb.mean(), len(ya), len(yb)
    if measure == "abs_ratio":
        ya = y.abs()[A].dropna(); yb = y.abs()[B].dropna()
        return ya.mean() / yb.mean(), len(ya), len(yb)
    if measure == "rank_corr":
        d = pd.DataFrame({"f": feature, "y": y})[A].dropna()
        return (d["f"].rank().corr(d["y"].rank()) if len(d) > 2 else np.nan), len(d), len(d)
    if measure == "hit_rate":
        ya = ((signal * y) > 0)[A & y.notna()]; yb = ((signal * y) > 0)[B & y.notna()]
        return ya.mean() - yb.mean(), len(ya), len(yb)
    if measure == "net_return":
        ya = (signal * y)[A].dropna()
        return ya.mean() - FEE_RT, len(ya), len(ya)
    raise ValueError(measure)


def centred(measure, v):
    return v - 1.0 if measure == "abs_ratio" else v


def judge_claim(idea, df, wn):
    c = idea["claim"]; m = c["measure"]
    if m not in MEASURES:
        return {"verdict": "refused", "why": f"unknown measure {m}"}
    if FORBIDDEN.search(c["code"]):
        return {"verdict": "refused", "why": "code uses a forbidden form (future shift, import, io)"}
    try:
        a, b, signal, feature = run_code(c["code"], df)
    except Exception as exc:  # noqa: BLE001
        return {"verdict": "refused", "why": f"code failed: {type(exc).__name__}: {exc}"[:200]}
    if m != "rank_corr" and b is None:
        return {"verdict": "refused", "why": "code must define `b`"}
    if m in ("mean_diff", "hit_rate", "net_return") and not isinstance(signal, pd.Series):
        return {"verdict": "refused", "why": "code must define `signal`"}
    if m == "rank_corr" and not isinstance(feature, pd.Series):
        return {"verdict": "refused", "why": "code must define `feature`"}
    h = int(c["horizon_bars"])
    y = df["close"].shift(-h) / df["close"] - 1
    want = c["direction"]; thr = float(c["min_effect"])
    total, na, nb = effect(m, a, b, y, signal, feature, wn > 0)
    wins = []
    for i in range(1, N_WIN + 1):
        v, _, _ = effect(m, a, b, y, signal, feature, wn == i)
        wins.append(None if (v is None or np.isnan(v)) else float(v))
    sign_total = np.sign(centred(m, total)) if not np.isnan(total) else 0
    agree = sum(1 for v in wins if v is not None and np.sign(centred(m, v)) == sign_total and sign_total != 0)
    if m == "abs_ratio":
        meets = (total >= thr) if want == "above" else (total <= thr)
    else:
        meets = (total >= thr) if want == "positive" else (total <= -abs(thr))
    checks = {"meets_min_effect": bool(meets), f"same_sign_in_{AGREE}_of_{N_WIN}": agree >= AGREE,
              f"min_{MIN_BARS}_bars_each": min(na, nb) >= MIN_BARS}
    return {"verdict": "pass" if all(checks.values()) else "fail", "effect": None if np.isnan(total) else float(total),
            "n_a": int(na), "n_b": int(nb), "windows": wins, "agreeing_windows": f"{agree} of {N_WIN}", "checks": checks}


def main():
    claims_path, fold, bar_size, symbols = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], sys.argv[4:]
    doc = yaml.safe_load(claims_path.read_text(encoding="utf-8"))
    windows = rf.load_fold_windows(fold)
    out = {"claims_file": str(claims_path.relative_to(ROOT)), "fold": fold, "bar_size": bar_size, "symbols": symbols,
           "rule": f"min_effect in direction on the fold; same sign in >= {AGREE} of {N_WIN} windows; "
                   f">= {MIN_BARS} bars in a and b; cost {FEE_RT:.2%} per round trip", "ideas": {}}
    frames = {s: load_bars(s, bar_size) for s in symbols}
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {"trials": []}
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for idea in doc["ideas"]:
        per = {}
        for s, df in frames.items():
            per[s] = judge_claim(idea, df, window_numbers(df.index, windows))
        verdicts = {v["verdict"] for v in per.values()}
        overall = "refused" if "refused" in verdicts else ("pass" if verdicts == {"pass"} else "fail")
        out["ideas"][idea["id"]] = {"verdict": overall, "by_symbol": per}
        ledger["trials"].append({"at": stamp, "try": claims_path.parent.name, "claim": idea["id"], "symbols": symbols,
                                 "bar_size": bar_size, "fold": fold, "verdict": overall})
        line = " | ".join(f"{s}: {v['verdict']}" + (f" effect={v['effect']:+.4f} n={v['n_a']}/{v['n_b']} agree={v['agreeing_windows']}"
                          if v["verdict"] != "refused" else f" ({v['why']})") for s, v in per.items())
        print(f"{idea['id']}: {overall.upper()}  {line}")
    out_path = claims_path.parent / "verdicts.yaml"
    out_path.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    LEDGER.write_text(yaml.safe_dump(ledger, sort_keys=False), encoding="utf-8")
    print(f"written {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
