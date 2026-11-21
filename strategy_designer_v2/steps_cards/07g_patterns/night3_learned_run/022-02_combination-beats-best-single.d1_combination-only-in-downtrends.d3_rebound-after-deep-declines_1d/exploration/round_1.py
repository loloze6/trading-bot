import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 5
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "fwd5": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "r1z": r1 / vol20,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "vol20": vol20,
                "hi20": c / c.rolling(20, min_periods=10).max() - 1,
                "rng": (b["high"] - b["low"]) / c,
                "regime": b["regime"].values,
                "depthpp": b.get("debug_info.components.depth.post_pipeline_value"),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            f["volrel"] = f["vol20"] / f["vol20"].rolling(60, min_periods=20).mean()
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A["drift5"] = A.groupby("coin")["fwd5"].transform(lambda s: s[A.loc[s.index, "pos"] % H == 0].mean())
    A["sd5"] = A.groupby("coin")["fwd5"].transform(lambda s: s[A.loc[s.index, "pos"] % H == 0].std())
    G = A[A["pos"] % H == 0].copy()
    G["ex5"] = (G["fwd5"] - G["drift5"]) / G["sd5"]  # in usual-move units
    out["grid_n"] = len(G.dropna(subset=["ex5"]))
    out["regime_counts"] = G["regime"].value_counts()

    feats = ["r1z", "r5", "r20", "vol20", "hi20", "rng", "volrel"]
    res = []
    for ft in feats:
        for reg in ["all", "mean_reversion", "unknown"]:
            g = G if reg == "all" else G[G["regime"] == reg]
            g = g.dropna(subset=[ft, "ex5"]).copy()
            g["z"] = g.groupby("coin")[ft].transform(lambda s: (s - s.mean()) / s.std())
            if len(g) < 50:
                continue
            sl = stats.linregress(g["z"], g["ex5"])
            pc = []
            for coin, gc in g.groupby("coin"):
                pc.append(np.sign(stats.linregress(gc["z"], gc["ex5"]).slope))
            res.append({"feat": ft, "regime": reg, "n": len(g), "slope_usualmove_per_sd": sl.slope,
                        "t": sl.slope / sl.stderr, "coins_pos": int(sum(np.array(pc) > 0))})
    out["slopes"] = pd.DataFrame(res)

    # quintiles of strongest candidates: r20 and vol relative
    for ft in ["r20", "r1z", "volrel", "hi20"]:
        g = G.dropna(subset=[ft, "ex5"]).copy()
        g["q"] = g.groupby("coin")[ft].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        q = g.groupby("q").agg(n=("ex5", "size"), ex_usual=("ex5", "mean"),
                               raw_fwd5=("fwd5", "mean"))
        out["quint_" + ft] = q

    # weekday on 1-day returns
    D = A.dropna(subset=["fwd1"]).copy()
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    wd = D.groupby((D["wd"] + 1) % 7).agg(n=("ex1", "size"), mean_ex_bps=("ex1", lambda s: s.mean() * 1e4),
                                          t=("ex1", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    out["weekday_next_day"] = wd

    # by year
    yrows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy()
            dd["coin"] = coin; dd["win"] = w
            yrows.append(dd)
    Y = pd.concat(yrows, ignore_index=True)
    Y["year"] = pd.to_datetime(Y["day"]).dt.year
    out["book_by_window"] = Y.groupby("win").agg(book_bps=("book_return", lambda s: s.mean() * 1e4),
                                                 coin_bps=("coin_return", lambda s: s.mean() * 1e4)).describe()
    out["book_by_year"] = Y.groupby("year").agg(book_bps=("book_return", lambda s: s.mean() * 1e4),
                                                coin_bps=("coin_return", lambda s: s.mean() * 1e4),
                                                n=("book_return", "size"))
    # positions
    out["active_share"] = float((A["alloc"].abs() > 1e-6).mean())
    out["mean_alloc_active"] = float(A.loc[A["alloc"].abs() > 1e-6, "alloc"].mean())
    return out
