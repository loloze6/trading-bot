import pandas as pd, numpy as np

def explore(data):
    rows = []
    bars = data["bars"]
    for coin, ws in bars.items():
        allret = []
        for w, b in ws.items():
            allret.append(b["close"].astype(float).pct_change().dropna())
        mu = pd.concat(allret).mean() if allret else 0.0
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l) / c
            rr = rng / rng.rolling(20).mean()
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            vol30 = r1.rolling(30).std()
            volmed = vol30.rolling(365, min_periods=60).median()
            f = b["forecast"].astype(float)
            reg = b["regime"].astype(str)
            ts = pd.to_datetime(b["timestamp"])
            fw = {k: c.shift(-k) / c - 1 for k in (1, 2, 3)}
            wid = b["debug_info.components.width.post_pipeline_value"] if "debug_info.components.width.post_pipeline_value" in b else pd.Series(np.nan, index=b.index)
            dn = b["debug_info.components.down5.post_pipeline_value"] if "debug_info.components.down5.post_pipeline_value" in b else pd.Series(np.nan, index=b.index)
            for i in range(len(b)):
                if np.isnan(fw[1].iloc[i]):
                    continue
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                    day=ts.iloc[i].normalize(), f=f.iloc[i], reg=reg.iloc[i],
                    u1=-(fw[1].iloc[i] - mu),
                    u2=-(fw[2].iloc[i] - 2*mu), u3=-(fw[3].iloc[i] - 3*mu),
                    r1=r1.iloc[i], rr=rr.iloc[i], r5=r5.iloc[i],
                    wid=wid.iloc[i], dn=dn.iloc[i],
                    agit=(vol30.iloc[i] > volmed.iloc[i]) if not np.isnan(volmed.iloc[i]) else np.nan,
                    cp=(c.iloc[i]-l.iloc[i])/(h.iloc[i]-l.iloc[i]) if h.iloc[i] > l.iloc[i] else np.nan))
    D = pd.DataFrame(rows)

    def summ(g, col="u1"):
        g = g.dropna(subset=[col])
        n = len(g)
        if n < 5:
            return dict(n=n, days=np.nan, mean=np.nan, t=np.nan)
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev**2).sum() * G / (G-1)) / n if G > 1 else np.nan
        return dict(n=n, days=G, mean=m, t=m/se if se else np.nan)

    def grp(g, key, col="u1"):
        return pd.DataFrame({k: summ(s, col) for k, s in g.groupby(key)}).T

    d = D[D.f < 0].copy()
    out = {}
    out["all_horizons"] = pd.DataFrame({k: summ(d, k) for k in ["u1", "u2", "u3"]}).T
    out["by_coin"] = grp(d, "coin").sort_values(by="t")
    out["by_window"] = grp(d, "w")
    out["by_year"] = grp(d, "year")
    d["fq"] = pd.qcut(d["f"].abs().rank(method="first"), 5, labels=False)
    out["by_absf_quint"] = grp(d, "fq")
    d["rrq"] = pd.qcut(d["rr"].rank(method="first"), 5, labels=False)
    out["by_rawwidth_quint"] = grp(d, "rrq")
    d["r5q"] = pd.qcut(d["r5"].rank(method="first"), 5, labels=False)
    out["by_ret5_quint"] = grp(d, "r5q")
    d["r1q"] = pd.qcut(d["r1"].rank(method="first"), 5, labels=False)
    out["by_upday_size_quint"] = grp(d, "r1q")
    out["by_agit"] = grp(d, "agit")
    d["cpb"] = pd.cut(d["cp"], [-0.01, 0.33, 0.67, 1.01], labels=["low", "mid", "high"])
    out["by_closepos"] = grp(d, "cpb")
    out["by_weekday"] = grp(d, "wd")
    core = ["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]
    d["core"] = d.coin.isin(core)
    out["core_vs_other"] = grp(d, "core")
    # comparison: falling-market down days (regime unknown) next-day short unusual move
    out["by_regime_all_bars"] = grp(D, "reg")
    # width effect: wide vs narrow up days in falling market (raw ratio median split)
    d["wide"] = d["rr"] > d["rr"].median()
    out["wide_vs_narrow"] = grp(d, "wide")
    out["corr_absf_u1"] = float(d[["f", "u1"]].corr().iloc[0, 1])
    return out
