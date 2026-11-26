def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def drift(coin, h):
        rs = []
        for w, df in bars[coin].items():
            c = df["close"].values
            for i in range(0, len(c) - h, h):
                rs.append(c[i + h] / c[i] - 1)
        return np.mean(rs), np.std(rs, ddof=1)
    def cases(h):
        rows = []
        for coin in bars:
            d, s = drift(coin, h)
            for w, df in bars[coin].items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                for i in range(0, len(df) - h, h):
                    r = df.iloc[i]
                    if r["regime"] != "mean_reversion": continue
                    fwd = c[i + h] / c[i] - 1
                    ts = pd.Timestamp(r["timestamp"])
                    rows.append(dict(coin=coin, w=w, day=ts.floor("D"), year=ts.year,
                                     un=fwd - d, tot=fwd, st=(fwd - d) / s, fc=r["forecast"],
                                     r90=r.get("debug_info.components.fall90.last_history_value", np.nan),
                                     r30=r.get("debug_info.components.fall30.last_history_value", np.nan),
                                     f90=r.get("debug_info.components.fall90.post_pipeline_value", np.nan)))
        return pd.DataFrame(rows)
    def ct(x):
        if len(x) < 3: return pd.Series(dict(n=len(x), mean=x["un"].mean() if len(x) else np.nan, t=np.nan, days=x["day"].nunique() if len(x) else 0))
        m = x["un"].mean(); g = (x["un"] - m).groupby(x["day"]).sum(); D = len(g)
        se = np.sqrt((g ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series(dict(n=len(x), mean=m, t=m / se if se > 0 else np.nan, days=D, strength=x["st"].mean(), tot=x["tot"].mean()))
    out = {}
    for h in [30, 45]:
        x = cases(h)
        out[f"h{h} r90 describe"] = x["r90"].describe()
        bins = [-np.inf, -2.5, -2.0, -1.5, -1.0, np.inf]
        x["b"] = pd.cut(x["r90"], bins)
        out[f"h{h} by r90 bin"] = x.groupby("b", observed=True).apply(ct)
        y = x.dropna(subset=["r90"])
        rho, p = stats.spearmanr(y["r90"], y["un"])
        out[f"h{h} spearman r90 vs un"] = f"rho {rho:.3f} p {p:.3f} n {len(y)}"
        rho, p = stats.spearmanr(y["fc"], y["un"])
        out[f"h{h} spearman fc vs un"] = f"rho {rho:.3f} p {p:.3f} n {len(y)}"
        med = y["r90"].median()
        deep = y[y["r90"] <= med]
        out[f"h{h} deeper half by year"] = deep.groupby("year").apply(ct)
        out[f"h{h} deeper half by coin group"] = deep.assign(g=np.where(deep["coin"].isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]),"default6","other13")).groupby("g").apply(ct)
        out[f"h{h} deeper half"] = ct(deep)
        # weighted by depth beyond -1
        wgt = (-y["r90"] - 1).clip(lower=0)
        out[f"h{h} un weighted by depth beyond 1"] = float((y["un"] * wgt).sum() / wgt.sum())
        # slope regression un on r90, clustered by day approx
        X = y["r90"].values; Y = y["un"].values
        b = np.polyfit(X, Y, 1)
        res = Y - np.polyval(b, X); xc = X - X.mean()
        g = pd.Series(xc * res).groupby(y["day"].values).sum(); D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / (xc ** 2).sum()
        out[f"h{h} slope un on r90"] = f"slope {b[0]:.4f} t {b[0]/se:.2f} days {D}"
    return out
