import pandas as pd, numpy as np
from scipy import stats

def _reg(d, x, y):
    d = d[[x, y]].dropna()
    if len(d) < 10: return (np.nan, np.nan, len(d))
    r = stats.linregress(d[x], d[y])
    return (r.slope, r.slope/r.stderr if r.stderr > 0 else np.nan, len(d))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                "r1": r1, "vol30": r1.rolling(30, min_periods=20).std(),
                "regime": b["regime"].values,
                "year": pd.to_datetime(b["timestamp"]).dt.year.values})
            for h in [1, 3, 7, 14]:
                df[f"f{h}"] = c.shift(-h)/c - 1
            for L in [3, 7, 14]:
                df[f"p{L}"] = c/c.shift(L) - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 3, 7, 14]:
        A[f"f{h}d"] = A[f"f{h}"] - A.groupby("coin")[f"f{h}"].transform("mean")
    for L in [3, 7, 14]:
        A[f"z{L}"] = A[f"p{L}"] / (A["vol30"] * np.sqrt(L))
    out = {}
    # grid of lookback x horizon x regime, non-overlapping grid of horizon
    res = []
    for h in [3, 7, 14]:
        G = A[A["pos"] % h == 0]
        for L in [3, 7, 14]:
            for reg in ["trending", "unknown"]:
                s, t, n = _reg(G[G["regime"] == reg], f"z{L}", f"f{h}d")
                res.append({"h": h, "L": L, "reg": reg, "slope": s, "t": t, "n": n})
    out["lookback_horizon"] = pd.DataFrame(res)
    # robustness of p7 -> f7 in trending: grid offsets
    off = []
    for o in range(7):
        G = A[(A["pos"] % 7 == o) & (A["regime"] == "trending")]
        s, t, n = _reg(G, "z7", "f7d")
        off.append({"offset": o, "slope": s, "t": t, "n": n})
    out["offsets_trend_z7_f7"] = pd.DataFrame(off)
    G7 = A[A["pos"] % 7 == 0]
    bc = []
    for coin in G7["coin"].unique():
        for reg in ["trending", "unknown"]:
            s, t, n = _reg(G7[(G7["coin"] == coin) & (G7["regime"] == reg)], "z7", "f7d")
            bc.append({"coin": coin, "reg": reg, "slope": s, "t": t, "n": n})
    by = []
    for y in sorted(G7["year"].unique()):
        s, t, n = _reg(G7[(G7["year"] == y) & (G7["regime"] == "trending")], "z7", "f7d")
        by.append({"year": y, "slope": s, "t": t, "n": n})
    out["coin_z7_f7"] = pd.DataFrame(bc)
    out["year_trend_z7_f7"] = pd.DataFrame(by)
    T = G7[G7["regime"] == "trending"].dropna(subset=["z7", "f7d"]).copy()
    T["q"] = pd.qcut(T["z7"], 5, labels=False)
    out["trend_z7_quint"] = T.groupby("q")["f7d"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    U = G7[G7["regime"] == "unknown"].dropna(subset=["z7", "f7d"]).copy()
    U["q"] = pd.qcut(U["z7"], 5, labels=False)
    out["unk_z7_quint"] = U.groupby("q")["f7d"].agg(["count", "mean"])
    # interaction test: slope difference
    a = _reg(G7[G7["regime"] == "trending"], "z7", "f7d"); b_ = _reg(G7[G7["regime"] == "unknown"], "z7", "f7d")
    out["slope_diff_t_approx"] = float((a[0]-b_[0])/np.sqrt((a[0]/a[1])**2 + (b_[0]/b_[1])**2))
    # after large daily moves, by regime
    A["zr"] = A["r1"] / A["vol30"]
    A["zq"] = pd.qcut(A["zr"], 5, labels=False)
    out["after_move_by_reg"] = A.groupby(["regime", "zq"])["f1d"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    s, t, n = _reg(A, "zr", "f1d"); out["zr_f1_all_t"] = f"slope {s:.5f} t {t:.2f} n {n}"
    # book's largest days
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; bk.append(d)
    D = pd.concat(bk).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"], 10, labels=False, duplicates="drop")
    out["book_decile_coin"] = D.groupby("bq")[["book_return", "coin_return"]].mean()
    return out
