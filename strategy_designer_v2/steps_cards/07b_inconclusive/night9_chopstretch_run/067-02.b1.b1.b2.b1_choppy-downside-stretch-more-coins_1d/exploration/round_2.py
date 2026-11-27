def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            r = s.pct_change()
            sma = s.rolling(20).mean().values
            sd = r.rolling(20).std().values
            st = (c - sma) / sma / sd
            vol30 = r.rolling(30).std().values
            vol90 = r.rolling(90, min_periods=40).std().values
            tr60 = (s / s.shift(60) - 1).values
            tr20 = (s / s.shift(20) - 1).values
            raw = df.get("debug_info.components.stretch.last_history_value")
            for h in [5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     ret=c[i + h] / c[i] - 1, fc=float(df["forecast"].iloc[i]),
                                     reg=df["regime"].iloc[i], st=st[i],
                                     agr=vol30[i] / vol90[i] if vol90[i] == vol90[i] else np.nan,
                                     tr60=tr60[i], tr20=tr20[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    def summ(g, wcol=None):
        g = g.copy()
        wt = g[wcol].values if wcol else np.ones(len(g))
        x = g["sx"].values
        m = (x * wt).sum() / wt.sum()
        g["dev"] = wt * (x - m)
        dd = g.groupby("day")["dev"].sum()
        D = len(dd)
        se = np.sqrt((dd ** 2).sum() * D / max(D - 1, 1)) / wt.sum()
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se if se > 0 else np.nan))
    out = {}
    act = d[(d.reg == "unknown") & (d.fc < 0)].copy()
    act["sx"] = -act["ex"]; act["afc"] = act["fc"].abs()
    out["fc_active_by_h_unw"] = act.groupby("h").apply(summ)
    out["fc_active_by_h_wtd"] = act.groupby("h").apply(lambda g: summ(g, "afc"))
    a5 = act[act.h == 5].copy()
    a5["fq"] = pd.qcut(a5["afc"], 4, labels=["fq1_small", "fq2", "fq3", "fq4_large"])
    out["h5_by_fc_quart"] = a5.groupby("fq").apply(summ)
    a5["sq"] = pd.qcut(a5["st"], 4, labels=["sq1_far", "sq2", "sq3", "sq4_near"])
    out["h5_by_rawstretch_quart"] = a5.groupby("sq").apply(summ)
    out["corr_fc_rawstretch"] = float(a5[["afc", "st"]].corr().iloc[0, 1])
    a5["agi"] = np.where(a5.agr > 1, "agit(vol30>vol90)", "calm")
    out["h5_by_agit"] = a5.dropna(subset=["agr"]).groupby("agi").apply(summ)
    a5["t60"] = pd.cut(a5["tr60"], [-1, -0.03, 0.03, 1], labels=["t60_down", "t60_flat", "t60_up"])
    out["h5_by_tr60"] = a5.dropna(subset=["tr60"]).groupby("t60").apply(summ)
    a5["t20"] = pd.qcut(a5["tr20"], 3, labels=["t20_low", "t20_mid", "t20_high"])
    out["h5_by_tr20"] = a5.dropna(subset=["tr20"]).groupby("t20").apply(summ)
    a10 = act[act.h == 10].copy()
    a10["agi"] = np.where(a10.agr > 1, "agit(vol30>vol90)", "calm")
    out["h10_by_agit"] = a10.dropna(subset=["agr"]).groupby("agi").apply(summ)
    # agitated subset graded?
    ag = a5[a5.agr > 1].copy()
    if len(ag) > 20:
        ag["sq"] = pd.qcut(ag["st"], 3, labels=["far", "mid", "near"])
        out["h5_agit_by_stretch_terc"] = ag.groupby("sq").apply(summ)
    return out
