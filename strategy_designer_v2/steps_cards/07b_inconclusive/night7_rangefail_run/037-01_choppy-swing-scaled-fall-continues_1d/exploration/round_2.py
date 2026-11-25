import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    H = [5, 10]
    drift, usual = {}, {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            usual[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    # coin-level vol30 median over all its B/C bars (proxy for past-year median)
    vmed = {}
    for coin, wins in bars.items():
        vs = []
        for w, df in wins.items():
            vs.extend(list(pd.Series(df["close"].values).pct_change().rolling(30).std().dropna().values))
        vmed[coin] = np.median(vs) if vs else np.nan
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c); f = df["forecast"].values
            s = pd.Series(c)
            r5 = s.pct_change(5).values
            sd20 = s.pct_change().rolling(20).std().values
            v30 = s.pct_change().rolling(30).std().values
            r20 = s.pct_change(20).values
            for i in range(0, n, 5):
                if not (f[i] < 0):
                    continue
                rec = dict(coin=coin, w=w, day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                           f=f[i], z=r5[i] / sd20[i] if sd20[i] else np.nan,
                           agit=(v30[i] > vmed[coin]) if not np.isnan(v30[i]) else np.nan,
                           r20=r20[i])
                for h in H:
                    rec[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                    rec[f"s{h}"] = rec[f"u{h}"] / usual[(coin, h)] if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def tday(x, col):
        x = x.dropna(subset=[col])
        N = len(x)
        if N < 3:
            return pd.Series(dict(n=N, days=np.nan, mean=x[col].mean() if N else np.nan, t=np.nan))
        m = x[col].mean()
        dev = x.groupby("day")[col].apply(lambda s: (s - m).sum())
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / N if G > 1 else np.nan
        return pd.Series(dict(n=N, days=G, mean=m, t=m / se if se else np.nan))

    out = {}
    d["zq"] = pd.qcut(d["z"].rank(method="first"), 4, labels=["z1deep", "z2", "z3", "z4shallow"])
    out["z quartile h5"] = d.groupby("zq").apply(lambda x: tday(x, "u5"))
    out["z quartile strength h5"] = d.groupby("zq").apply(lambda x: tday(x, "s5"))
    out["corr z vs u5 (spearman)"] = float(d[["z", "u5"]].dropna().corr(method="spearman").iloc[0, 1])
    d2 = d.dropna(subset=["agit"])
    d2["ag"] = np.where(d2["agit"].astype(bool), "agitated", "calm")
    out["profile-like agitation h5"] = d2.groupby("ag").apply(lambda x: tday(x, "u5"))
    out["agitation x z half h5"] = d2.assign(zh=np.where(d2["z"] <= d2["z"].median(), "deep", "shallow")).groupby(["ag", "zh"]).apply(lambda x: tday(x, "u5"))
    out["agitated: corr z vs u5"] = float(d2[d2.ag == "agitated"][["z", "u5"]].dropna().corr(method="spearman").iloc[0, 1])
    out["calm: corr z vs u5"] = float(d2[d2.ag == "calm"][["z", "u5"]].dropna().corr(method="spearman").iloc[0, 1])
    d["r20s"] = np.where(d["r20"] < 0, "20d down", "20d up")
    out["by 20d sign h5"] = d.dropna(subset=["r20"]).groupby("r20s").apply(lambda x: tday(x, "u5"))
    out["no DOGE h5"] = tday(d[d.coin != "DOGEUSD"], "u5")
    out["core6 h5"] = tday(d[d.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])], "u5")
    return out
