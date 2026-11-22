import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 8
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            if n < 30:
                continue
            r1 = c.pct_change()
            r3 = c / c.shift(3) - 1
            r10 = c / c.shift(10) - 1
            r20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            hi20 = c.shift(1).rolling(20).max()
            lo20 = c.shift(1).rolling(20).min()
            dist_hi = c / c.rolling(20).max() - 1
            brk = (c > hi20).astype(float)
            # failure at bar t: breakout on one of t-3..t-1, close back below that breakout's old high
            fail = np.zeros(n)
            fdepth = np.full(n, np.nan)
            for t in range(n):
                for k in (1, 2, 3):
                    e = t - k
                    if e >= 0 and brk.iloc[e] == 1 and not np.isnan(hi20.iloc[e]):
                        if c.iloc[t] < hi20.iloc[e]:
                            fail[t] = 1
                            fdepth[t] = hi20.iloc[e] / c.iloc[t] - 1
                        break
            fwd = c.shift(-H) / c - 1
            fwd_lag2 = c.shift(-H - 2) / c.shift(-2) - 1
            hi_ = b["high"].astype(float); lo_ = b["low"].astype(float)
            rng = (hi_ - lo_) / c
            rng_rel = rng / rng.rolling(20).mean()
            vchg = b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean()
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            grid = np.arange(0, n, H)
            for t in grid:
                if t + H >= n:
                    continue
                rows.append(dict(coin=coin, w=w, fwd=fwd.iloc[t], r1=r1.iloc[t], r3=r3.iloc[t],
                                 r10=r10.iloc[t], r20=r20.iloc[t], vol20=vol20.iloc[t],
                                 dist_hi=dist_hi.iloc[t], brk=brk.iloc[t], fail=fail[t],
                                 rng_rel=rng_rel.iloc[t], vchg=vchg.iloc[t], wd=wd.iloc[t]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["unu"] = df["fwd"] - df["drift"]
    out = {}
    def summ(g):
        x = g["unu"].dropna()
        return pd.Series({"n": len(x), "mean_unu": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "mean_fwd": g["fwd"].mean()})
    out["drift_by_coin"] = df.groupby("coin")["fwd"].agg(["mean", "std", "count"])
    for f in ["r1", "r3", "r10", "r20", "vol20", "dist_hi", "rng_rel", "vchg"]:
        d = df.dropna(subset=[f]).copy()
        # rank within coin to quintiles
        d["q"] = d.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["q5_" + f] = d.groupby("q").apply(summ)
    out["by_brk"] = df.groupby("brk").apply(summ)
    out["by_fail"] = df.groupby("fail").apply(summ)
    # combos: r20 quintile x vol tercile
    d = df.dropna(subset=["r20", "vol20"]).copy()
    d["qr"] = d.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["qv"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["r20t_x_volt"] = d.groupby(["qr", "qv"]).apply(summ)
    # spearman per coin of r20, dist_hi with unu
    sp = []
    for coin, g in df.groupby("coin"):
        rr = {}
        for f in ["r1", "r10", "r20", "dist_hi", "vol20"]:
            gg = g.dropna(subset=[f, "unu"])
            rr[f] = stats.spearmanr(gg[f], gg["unu"])[0]
        rr["coin"] = coin
        sp.append(rr)
    out["spearman_by_coin"] = pd.DataFrame(sp).set_index("coin")
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w
            dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["coin_ret_by_weekday"] = dd.groupby("wd")["coin_return"].agg(["mean", "std", "count"]).assign(t=lambda s: s["mean"] / (s["std"] / np.sqrt(s["count"])))
    out["book_ret_by_coin"] = dd.groupby("coin")[["book_return", "coin_return"]].mean()
    return out
