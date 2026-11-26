def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [7, 14]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            usual[(c, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            cl = pd.Series(df["close"].values)
            n = len(df)
            r7 = cl.pct_change(7)
            sc = r7 / r7.abs().rolling(30).mean()
            r60 = cl.pct_change(60)
            r30 = cl.pct_change(30)
            dr = cl.pct_change()
            v30 = dr.rolling(30).std()
            v120 = dr.rolling(120).std()
            rng = (df["high"] - df["low"]) / df["close"]
            yr = pd.Timestamp(df["timestamp"].iloc[0]).year
            low = 0.0; last_cell = -1
            for t in range(n):
                if f[t] <= 0:
                    low = 0.0; continue
                low = min(low, f[t])
                cell = t // 7
                if f[t] - low >= 2 and cell != last_cell and t + 7 < n:
                    last_cell = cell
                    rec = dict(coin=c, win=w, year=yr, fc=f[t], sc=sc.iloc[t], r60=r60.iloc[t],
                               r30=r30.iloc[t], vr=v30.iloc[t] / v120.iloc[t] if v120.iloc[t] > 0 else np.nan,
                               r1=dr.iloc[t], day=str(df["timestamp"].iloc[t])[:10])
                    for h in H:
                        if t + h < n:
                            rec[f"u{h}"] = cl.iloc[t + h] / cl.iloc[t] - 1 - drift[(c, h)]
                    rows.append(rec)
                    low = f[t]
    d = pd.DataFrame(rows)
    def ts(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    def grp(col, q=2):
        x = d.dropna(subset=[col]).copy()
        x["g"] = pd.qcut(x[col].rank(method="first"), q, labels=[f"{col}{i+1}" for i in range(q)])
        a = x.groupby("g")["u7"].apply(ts).unstack().add_prefix("u7_")
        b = x.groupby("g")["u14"].apply(ts).unstack().add_prefix("u14_")
        m = x.groupby("g")[col].mean().rename("mid")
        return pd.concat([m, a, b], axis=1)
    out = {}
    out["u14 day pooled"] = ts(d.groupby("day")["u14"].sum())
    out["by r60 half"] = grp("r60")
    out["by r30 half"] = grp("r30")
    out["by vol ratio half"] = grp("vr")
    out["by last day return half"] = grp("r1")
    out["by r60 sign"] = d.assign(g=np.sign(d["r60"])).groupby("g")["u7"].apply(ts).unstack()
    out["spearman"] = pd.Series({"sc~u14": d[["sc", "u14"]].corr("spearman").iloc[0, 1],
                                 "r60~u7": d[["r60", "u7"]].corr("spearman").iloc[0, 1],
                                 "vr~u7": d[["vr", "u7"]].corr("spearman").iloc[0, 1],
                                 "share r60 missing": d["r60"].isna().mean()})
    out["year x sc half u7"] = d.assign(g=pd.qcut(d["sc"].rank(method="first"), 2, labels=["low", "high"])).groupby(["year", "g"])["u7"].mean().unstack()
    return out
