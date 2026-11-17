import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float); hi = b["high"].astype(float); vol = b["volume"].astype(float)
            r1 = cl.pct_change()
            d = pd.DataFrame({"coin": c, "win": w, "pos": np.arange(len(b))})
            d["ts"] = pd.to_datetime(b["timestamp"])
            d["r1"] = r1
            d["past5"] = cl / cl.shift(5) - 1
            d["past10"] = cl / cl.shift(10) - 1
            d["past20"] = cl / cl.shift(20) - 1
            d["dist30"] = cl / hi.shift(1).rolling(30).max() - 1
            d["vol20"] = r1.rolling(20).std()
            d["volz"] = np.log(vol / vol.shift(1).rolling(20).mean())
            for h in (1, 5, 10):
                d[f"f{h}"] = cl.shift(-h) / cl - 1
            d["fc"] = b["forecast"].astype(float)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # demean forward returns per coin using grid mean
    res = []
    for h in (1, 5, 10):
        g = D[D["pos"] % h == 0].copy()
        g[f"x{h}"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
        for xv in ["past5", "past10", "past20", "dist30", "vol20", "volz"]:
            s = g[[xv, f"x{h}"]].dropna()
            # per-coin z of predictor
            z = s[xv]
            sl = stats.linregress(z, s[f"x{h}"])
            res.append({"h": h, "pred": xv, "slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(s),
                        "corr": sl.rvalue})
    out["pooled_regressions"] = pd.DataFrame(res)
    # per-coin for 10d horizon
    pc = []
    g = D[D["pos"] % 10 == 0].copy()
    g["x10"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
    for c, gc in g.groupby("coin"):
        for xv in ["past10", "dist30", "vol20", "volz"]:
            s = gc[[xv, "x10"]].dropna()
            sl = stats.linregress(s[xv], s["x10"])
            pc.append({"coin": c, "pred": xv, "t": sl.slope / sl.stderr, "n": len(s)})
    out["percoin_10d"] = pd.DataFrame(pc).pivot(index="coin", columns="pred", values="t")
    # dist30 quintiles, 10d excess
    s = g[["dist30", "x10"]].dropna()
    s["q"] = pd.qcut(s["dist30"], 5, labels=False)
    out["dist30_quint_10d"] = s.groupby("q").agg(dmean=("dist30", "mean"), x=("x10", "mean"), n=("x10", "size"),
                                                  t=("x10", lambda v: v.mean() / v.std() * np.sqrt(len(v))))
    # weekday daily returns
    dd = D.dropna(subset=["r1"]).copy()
    dd["wd"] = dd["ts"].dt.weekday
    dd["x1"] = dd["r1"] - dd.groupby("coin")["r1"].transform("mean")
    out["weekday"] = dd.groupby("wd")["x1"].agg(["mean", "count", lambda v: v.mean() / v.std() * np.sqrt(len(v))])
    # forecast/position
    out["active_share"] = float((D["fc"] > 0).mean())
    out["alloc_mean_when_active"] = float(D.loc[D["alloc"] > 0, "alloc"].mean())
    out["share_bars_long"] = float((D["alloc"] > 0.01).mean())
    # book daily: largest gains/losses context
    bk = []
    for c in days:
        for w, x in days[c].items():
            x = x.reset_index(drop=True).copy(); x["coin"] = c
            x["prev5"] = x["close"] / x["close"].shift(5) - 1
            x["next5"] = x["close"].shift(-5) / x["close"] - 1
            bk.append(x)
    B = pd.concat(bk, ignore_index=True).dropna(subset=["book_return"])
    act = B[B["book_return"].abs() > 1e-9]
    out["book_active_days"] = len(act)
    q = act["book_return"].quantile([0.05, 0.95])
    out["book_tails"] = pd.DataFrame({
        "worst5%": act[act["book_return"] <= q.iloc[0]][["book_return", "coin_return", "prev5", "next5"]].mean(),
        "best5%": act[act["book_return"] >= q.iloc[1]][["book_return", "coin_return", "prev5", "next5"]].mean()})
    out["book_by_coin"] = act.groupby("coin")["book_return"].agg(["mean", "count", "sum"])
    return out
