def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=20).std()
            feats = {}
            for K in (3, 5, 10):
                feats[f"ret{K}"] = (c / c.shift(K) - 1) / sd
            hh = h.rolling(20, min_periods=20).max()
            feats["d20"] = (c - hh) / hh / sd
            ll = l.rolling(20, min_periods=20).min()
            feats["upl20"] = (c - ll) / ll / sd
            rec = (df["regime"] == "unknown").values
            for H in (3, 5, 10):
                fwd = c.shift(-H) / c - 1
                for i in range(0, len(df), H):
                    if np.isnan(fwd.iloc[i]) or np.isnan(sd.iloc[i]): continue
                    row = dict(coin=coin, w=w, H=H, fwd=fwd.iloc[i], rec=bool(rec[i]),
                               year=pd.Timestamp(df["timestamp"].iloc[i]).year)
                    for k, v in feats.items(): row[k] = v.iloc[i]
                    rows.append(row)
    d = pd.DataFrame(rows)
    mu = d.groupby(["coin", "H"])["fwd"].mean().rename("mu")
    d = d.join(mu, on=["coin", "H"]); d["ex"] = d["fwd"] - d["mu"]
    p = d[d.rec]
    out = {}
    res = []
    for H, g in p.groupby("H"):
        for f in ("ret3", "ret5", "ret10", "d20", "upl20"):
            gg = g.dropna(subset=[f])
            if len(gg) < 20: continue
            sl = stats.linregress(gg[f], gg["ex"])
            q = pd.qcut(gg[f], 3, labels=False, duplicates="drop")
            m = gg.groupby(q)["ex"].mean()
            pos = gg[gg[f] > 0]
            res.append(dict(H=H, f=f, n=len(gg), slope=sl.slope, t=sl.slope / sl.stderr,
                            low3=m.iloc[0], mid3=m.iloc[1], high3=m.iloc[-1],
                            n_pos=len(pos), ex_pos=pos["ex"].mean() if len(pos) else np.nan,
                            fwd_pos=pos["fwd"].mean() if len(pos) else np.nan))
    out["recorded_FC_features"] = pd.DataFrame(res)
    r2 = []
    for (H, key), g in p[p.H.isin([3, 5])].groupby(["H", "coin"]):
        for f in ("ret5", "ret10"):
            gg = g.dropna(subset=[f])
            if len(gg) < 10: continue
            sl = stats.linregress(gg[f], gg["ex"])
            r2.append(dict(H=H, coin=key, f=f, n=len(gg), slope=sl.slope, t=sl.slope / sl.stderr))
    out["by_coin"] = pd.DataFrame(r2)
    r3 = []
    for (H, key), g in p[p.H.isin([3, 5])].groupby(["H", "year"]):
        for f in ("ret5", "ret10"):
            gg = g.dropna(subset=[f])
            if len(gg) < 8: continue
            sl = stats.linregress(gg[f], gg["ex"])
            r3.append(dict(H=H, year=key, f=f, n=len(gg), slope=sl.slope, t=sl.slope / sl.stderr))
    out["by_year"] = pd.DataFrame(r3)
    return out
