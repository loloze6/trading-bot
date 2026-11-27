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
            for P in (10, 20, 40):
                hh = h.rolling(P, min_periods=P).max()
                feats[f"d{P}"] = (c - hh) / hh / sd
            ll = l.rolling(20, min_periods=20).min()
            feats["up_from_low"] = (c - ll) / ll / sd
            feats["ret5"] = (c / c.shift(5) - 1) / sd
            tr60 = c / c.shift(60) - 1
            vol30 = r.rolling(30, min_periods=30).std()
            pct = vol30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            prof = np.where(tr60 < -0.10, np.where(pct > 0.5, "FA", "FC"), "other")
            for H in (3, 5):
                fwd = c.shift(-H) / c - 1
                for i in range(0, len(df), H):
                    if np.isnan(fwd.iloc[i]) or np.isnan(feats["d20"].iloc[i]): continue
                    row = dict(coin=coin, w=w, H=H, fwd=fwd.iloc[i], prof=prof[i],
                               rec=(df["regime"].iloc[i] == "unknown"),
                               year=pd.Timestamp(df["timestamp"].iloc[i]).year)
                    for k, v in feats.items(): row[k] = v.iloc[i]
                    rows.append(row)
    d = pd.DataFrame(rows)
    mu = d.groupby(["coin", "H"])["fwd"].mean().rename("mu")
    d = d.join(mu, on=["coin", "H"]); d["ex"] = d["fwd"] - d["mu"]
    out = {}
    res = []
    for (H, p), g in d.groupby(["H", "prof"]):
        for f in ("d10", "d20", "d40", "up_from_low", "ret5"):
            gg = g.dropna(subset=[f])
            if len(gg) < 20: continue
            sl = stats.linregress(gg[f], gg["ex"])
            q = pd.qcut(gg[f], 3, labels=False, duplicates="drop")
            m = gg.groupby(q)["ex"].mean()
            res.append(dict(H=H, prof=p, f=f, n=len(gg), slope=sl.slope, t=sl.slope / sl.stderr,
                            low3=m.iloc[0], high3=m.iloc[-1], meanfwd=gg["fwd"].mean()))
    out["slopes_by_profile_feature"] = pd.DataFrame(res)
    fc = d[(d.prof == "FC")]
    r2 = []
    for (H, y), g in fc.groupby(["H", "year"]):
        if len(g) < 8: continue
        sl = stats.linregress(g["d20"], g["ex"])
        r2.append(dict(H=H, year=y, n=len(g), slope=sl.slope, t=sl.slope / sl.stderr,
                       meanex=g["ex"].mean(), meanfwd=g["fwd"].mean()))
    out["fc_by_year_d20"] = pd.DataFrame(r2)
    out["agree_recorded_vs_mine"] = d.groupby("prof")["rec"].mean()
    return out
