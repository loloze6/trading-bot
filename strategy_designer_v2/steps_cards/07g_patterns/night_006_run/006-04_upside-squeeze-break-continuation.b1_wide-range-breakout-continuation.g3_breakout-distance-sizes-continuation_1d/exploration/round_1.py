def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            prior_hi = hi.shift(1).rolling(20).max()
            prior_lo = lo.shift(1).rolling(20).min()
            dist_hi = c / prior_hi - 1
            dist_lo = c / prior_lo - 1
            width = (prior_hi - prior_lo) / c
            width_rel = width / width.rolling(120, min_periods=40).median()
            volr = v.rolling(10).mean() / v.rolling(60, min_periods=30).mean()
            vol20 = r1.rolling(20).std()
            past10 = c / c.shift(10) - 1
            past30 = c / c.shift(30) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            df = pd.DataFrame(dict(coin=coin, win=w, fwd=fwd, dist_hi=dist_hi, dist_lo=dist_lo, width_rel=width_rel,
                                   volr=volr, vol20=vol20, past10=past10, past30=past30, r1=r1, fwd1=fwd1, wd=wd,
                                   fc=b["forecast"], alloc=b["postRebalance_current_allocation"]))
            df["grid"] = (np.arange(len(df)) % H) == 0
            rows.append(df)
        for w, d in data["days"][coin].items():
            dd = d[["book_return", "coin_return"]].copy(); dd["coin"] = coin; dd["win"] = w
            daily.append(dd)
    A = pd.concat(rows, ignore_index=True)
    cm = A[A.grid].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(cm)
    G = A[A.grid].dropna(subset=["ex"])
    def qtab(col, q=5, dfx=G):
        d = dfx.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("q")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["absmean"] = d.groupby("q")["fwd"].apply(lambda s: s.abs().mean())
        rho = stats.spearmanr(d[col], d["ex"])
        t.loc["spearman_rho"] = [rho[0], len(d), np.nan, rho[1], np.nan]
        return t
    for col in ["dist_hi", "dist_lo", "width_rel", "volr", "vol20", "past10", "past30"]:
        out["ex10 by " + col] = qtab(col)
    # compression: abs forward move
    d = G.dropna(subset=["width_rel", "volr"]).copy()
    d["absf"] = d["fwd"].abs()
    d["absf_rel"] = d["absf"] / d["coin"].map(d.groupby("coin")["absf"].mean())
    d["q"] = d.groupby("coin")["width_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["abs move rel by width q"] = d.groupby("q")["absf_rel"].agg(["mean", "count"])
    # per coin rho past30
    pc = {}
    for coin, g in G.dropna(subset=["past30"]).groupby("coin"):
        r = stats.spearmanr(g["past30"], g["ex"]); pc[coin] = (r[0], r[1], len(g))
    out["past30 rho per coin"] = pd.DataFrame(pc, index=["rho", "p", "n"]).T
    # next-day after large moves
    A["z"] = A["r1"] / A["vol20"].shift(1)
    A["fwd1ex"] = A["fwd1"] - A["coin"].map(A.groupby("coin")["fwd1"].mean())
    zz = A.dropna(subset=["z", "fwd1ex"]).copy()
    zz["zb"] = pd.cut(zz["z"], [-99, -2, -1, 1, 2, 99])
    t = zz.groupby("zb")["fwd1ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next day ex by z of today"] = t
    t = A.dropna(subset=["fwd1ex"]).groupby("wd")["fwd1ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next day ex by weekday"] = t
    # book
    D = pd.concat(daily, ignore_index=True).dropna()
    out["book"] = pd.Series({"mean_book": D.book_return.mean(), "mean_coin": D.coin_return.mean(),
                             "sharpe_book": D.book_return.mean() / D.book_return.std() * np.sqrt(365),
                             "n": len(D)})
    # book by year
    A["fc_pos"] = A["fc"] > 0
    gain = A.dropna(subset=["fwd1"]).copy(); gain["g"] = gain["alloc"].fillna(0) * gain["fwd1"]
    out["position gain by coin"] = gain.groupby("coin")["g"].agg(["mean", "sum"]).join(gain.groupby("coin")["alloc"].apply(lambda s: (s.abs() > 0).mean()).rename("share_in"))
    return out
