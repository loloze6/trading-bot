def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    def drift(coin, h):
        rs = []
        for w, df in bars[coin].items():
            c = df["close"].values
            for i in range(0, len(c) - h, h):
                rs.append(c[i + h] / c[i] - 1)
        return np.mean(rs) if rs else np.nan, np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    def cases(h, cond="fc"):
        rows = []
        for coin in bars:
            d, s = drift(coin, h)
            for w, df in bars[coin].items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                for i in range(0, len(df) - h, h):
                    r = df.iloc[i]
                    ok = r["forecast"] > 0 if cond == "fc" else r["regime"] == "mean_reversion"
                    if not ok: continue
                    fwd = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, day=pd.Timestamp(r["timestamp"]).floor("D"),
                                     year=pd.Timestamp(r["timestamp"]).year,
                                     un=fwd - d, tot=fwd, st=(fwd - d) / s, fc=r["forecast"],
                                     r90=r.get("debug_info.components.fall90.last_history_value", np.nan),
                                     r30=r.get("debug_info.components.fall30.last_history_value", np.nan)))
        return pd.DataFrame(rows)
    def ct(x):
        if len(x) < 3: return pd.Series(dict(n=len(x), mean=x["un"].mean() if len(x) else np.nan, t=np.nan, days=x["day"].nunique() if len(x) else 0))
        m = x["un"].mean(); g = (x["un"] - m).groupby(x["day"]).sum(); D = len(g)
        se = np.sqrt((g ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series(dict(n=len(x), mean=m, t=m / se if se > 0 else np.nan, days=D, strength=x["st"].mean(), tot=x["tot"].mean()))
    out = {}
    hz = {}
    for h in [7, 14, 30, 45, 60]:
        for cond in ["fc", "regime"]:
            x = cases(h, cond); hz[f"h{h}_{cond}"] = ct(x)
    out["by horizon"] = pd.DataFrame(hz).T
    x = cases(30, "regime")
    out["h30 regime by year"] = x.groupby("year").apply(ct)
    out["h30 regime by coin"] = x.groupby("coin").apply(ct)
    x["r30pos"] = np.where(x["r30"] > 0, "r30>0", np.where(x["r30"] <= 0, "r30<=0", "na"))
    out["h30 regime by 30d sign"] = x.groupby("r30pos").apply(ct)
    x["r90q"] = pd.qcut(x["r90"].rank(method="first"), 3, labels=["deep", "mid", "shallow"]) if x["r90"].notna().sum() > 9 else "na"
    out["h30 regime by 90d depth tercile"] = x.groupby("r90q").apply(ct)
    x["btcgrp"] = np.where(x["coin"].isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]), "default6", "other13")
    out["h30 regime by coin group"] = x.groupby("btcgrp").apply(ct)
    out["corr r30 vs un"] = float(x[["r30", "un"]].dropna().corr().iloc[0, 1])
    out["corr r90 vs un"] = float(x[["r90", "un"]].dropna().corr().iloc[0, 1])
    return out
