def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allg = []
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            b["fwd5"] = c.shift(-5) / c - 1
            b["ret1"] = c.pct_change()
            b["sd30"] = b["ret1"].rolling(30, min_periods=20).std()
            b["z1"] = b["ret1"] / b["sd30"].shift(1)
            b["low30"] = l.shift(1).rolling(30, min_periods=30).min()
            b["high30"] = h.shift(1).rolling(30, min_periods=30).max()
            b["reclaim"] = (l < b["low30"]) & (c >= b["low30"])
            b["closebelow"] = c < b["low30"]
            b["clv"] = (c - l) / (h - l).replace(0, np.nan)
            b["ret10"] = c / c.shift(10) - 1
            b["inprof"] = b["regime"] != "chop"
            b["pos"] = np.arange(len(b))
            b["cell"] = b["pos"] // 5
            b["coin"] = coin; b["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday; b["yr"] = ts.dt.year; b["dkey"] = ts.dt.floor("D")
            b["grid"] = (b["pos"] % 5 == 0)
            allg.append(b.loc[b["grid"], "fwd5"].dropna())
            rows.append(b)
        drift[coin] = pd.concat(allg).mean()
    B = pd.concat(rows, ignore_index=True)
    B["ex5"] = B["fwd5"] - B["coin"].map(drift)
    B["volrank"] = B.groupby("coin")["sd30"].rank(pct=True)

    def ev(mask):
        d = B[mask & B["ex5"].notna()]
        d = d.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)
        if len(d) < 3: return [len(d), np.nan, np.nan, np.nan]
        s = d.groupby("dkey")["ex5"].apply(lambda x: (x - d["ex5"].mean()).sum())
        D = len(s); m = d["ex5"].mean()
        se = np.sqrt((s**2).sum() * D / max(D - 1, 1)) / len(d)
        return [len(d), D, m, m / se if se > 0 else np.nan]

    def tab(groups):
        out = {k: ev(v) for k, v in groups.items()}
        return pd.DataFrame(out, index=["cases", "days", "mean_ex5", "t"]).T.round(4)

    P = B["inprof"]
    r = {}
    r["drift5"] = pd.Series(drift).round(4)
    r["profile_share"] = B.groupby("coin")["inprof"].mean().round(3)
    r["situations"] = tab({
        "prof_all": P, "prof_reclaim": P & B["reclaim"], "prof_closebelow": P & B["closebelow"],
        "prof_ordinary": P & ~B["reclaim"] & ~B["closebelow"],
        "out_all": ~P, "out_reclaim": ~P & B["reclaim"], "out_closebelow": ~P & B["closebelow"],
        "all_reclaim": B["reclaim"], "all_closebelow": B["closebelow"]})
    q = pd.qcut(B["z1"], 5, labels=False)
    r["z1_quintile_all"] = tab({f"q{i}": q == i for i in range(5)})
    r["z1_quintile_prof"] = tab({f"q{i}": P & (q == i) for i in range(5)})
    qc = pd.qcut(B["clv"], 5, labels=False)
    r["clv_quintile_all"] = tab({f"q{i}": qc == i for i in range(5)})
    r["clv_quintile_prof"] = tab({f"q{i}": P & (qc == i) for i in range(5)})
    qv = pd.cut(B["volrank"], [0, 1/3, 2/3, 1], labels=False)
    r["vol_tercile"] = tab({f"v{i}": qv == i for i in range(3)})
    q10 = pd.qcut(B["ret10"], 5, labels=False)
    r["ret10_quintile_all"] = tab({f"q{i}": q10 == i for i in range(5)})
    r["weekday"] = tab({f"wd{i}": B["wd"] == i for i in range(7)})
    r["year"] = tab({str(y): B["yr"] == y for y in sorted(B["yr"].unique())})
    r["reclaim_by_coin"] = tab({c: B["reclaim"] & (B["coin"] == c) for c in drift})
    return r
