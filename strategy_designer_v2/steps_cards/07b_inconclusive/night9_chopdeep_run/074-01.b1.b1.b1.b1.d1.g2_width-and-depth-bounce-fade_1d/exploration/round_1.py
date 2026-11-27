import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    bars = data["bars"]
    # coin mean daily return over all shown windows
    for coin, ws in bars.items():
        allret = []
        for w, b in ws.items():
            c = b["close"].astype(float).values
            allret.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allret).mean() if allret else 0.0
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l) / c
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            volmed = vol30.rolling(365, min_periods=60).median()
            n = len(b)
            fwd = {k: c.shift(-k) / c - 1 for k in (1, 2, 3, 5)}
            f = b["forecast"].astype(float)
            wid = b.get("debug_info.components.width.post_pipeline_value")
            dn = b.get("debug_info.components.down5.post_pipeline_value")
            ts = pd.to_datetime(b["timestamp"])
            for i in range(n):
                if f.iloc[i] < 0 and not np.isnan(fwd[1].iloc[i]):
                    rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                        day=ts.iloc[i].normalize(), f=f.iloc[i],
                        u1=-(fwd[1].iloc[i] - mu),
                        u2=-(fwd[2].iloc[i] - 2*mu) if not np.isnan(fwd[2].iloc[i]) else np.nan,
                        u3=-(fwd[3].iloc[i] - 3*mu) if not np.isnan(fwd[3].iloc[i]) else np.nan,
                        u5=-(fwd[5].iloc[i] - 5*mu) if not np.isnan(fwd[5].iloc[i]) else np.nan,
                        r1=r1.iloc[i], rng=rng.iloc[i],
                        wid=wid.iloc[i] if wid is not None else np.nan,
                        dn=dn.iloc[i] if dn is not None else np.nan,
                        agit=(vol30.iloc[i] > volmed.iloc[i]) if not np.isnan(volmed.iloc[i]) else np.nan,
                        closepos=(c.iloc[i]-l.iloc[i])/(h.iloc[i]-l.iloc[i]) if h.iloc[i]>l.iloc[i] else np.nan))
    d = pd.DataFrame(rows)

    def summ(g, col="u1"):
        x = g[col].dropna()
        if len(x) < 5: return pd.Series(dict(n=len(x), mean=np.nan, t=np.nan))
        dd = g.dropna(subset=[col]).groupby("day")[col].apply(lambda s: s.sum())
        cnt = g.dropna(subset=[col]).groupby("day")[col].count()
        m = x.mean()
        dev = g.dropna(subset=[col]).assign(dv=lambda z: z[col]-m).groupby("day")["dv"].sum()
        G = len(dev)
        se = np.sqrt((dev**2).sum() * G/(G-1)) / len(x) if G > 1 else np.nan
        return pd.Series(dict(n=len(x), days=G, mean=m, t=m/se if se else np.nan))

    out = {}
    out["all"] = pd.DataFrame({k: summ(d, k) for k in ["u1","u2","u3","u5"]}).T
    out["by_coin"] = d.groupby("coin").apply(summ).sort_values("t")
    out["by_window"] = d.groupby("w").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].abs(), 5, labels=False, duplicates="drop")
    out["by_absf_quint"] = d.groupby("fq").apply(summ)
    d["wq"] = pd.qcut(d["rng"].rank(pct=True) if False else d["wid"], 5, labels=False, duplicates="drop")
    out["by_width_quint"] = d.groupby("wq").apply(summ)
    d["dq"] = d["dn"].apply(lambda v: "dn0" if v == 0 else "dn<0")
    out["by_down5_on"] = d.groupby("dq").apply(summ)
    d["rq"] = pd.qcut(d["r1"], 5, labels=False, duplicates="drop")
    out["by_upday_size_quint"] = d.groupby("rq").apply(summ)
    out["by_agit"] = d.groupby("agit").apply(summ)
    d["cp"] = pd.cut(d["closepos"], [-0.01, 0.33, 0.67, 1.01], labels=["lowclose","mid","highclose"])
    out["by_closepos"] = d.groupby("cp").apply(summ)
    out["by_weekday"] = d.groupby("wd").apply(summ)
    core = d[d.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])]
    out["core_vs_other"] = pd.DataFrame({"core": summ(core), "other": summ(d[~d.index.isin(core.index)])}).T
    return out
