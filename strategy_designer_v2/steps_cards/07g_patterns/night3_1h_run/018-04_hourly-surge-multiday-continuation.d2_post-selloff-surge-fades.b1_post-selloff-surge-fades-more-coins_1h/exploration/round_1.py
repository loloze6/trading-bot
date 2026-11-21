def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows120 = []; rows24 = []
    for coin, wins in bars.items():
        # coin usual move/drift
        r120_all = []; r24_all = []
        prepared = {}
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            n = len(c)
            f120 = c.shift(-120) / c - 1
            f24 = c.shift(-24) / c - 1
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=240).mean()
            surge = r24 / mabs
            r1 = c.pct_change()
            vol720 = r1.rolling(720, min_periods=240).std()
            vol24 = r1.rolling(24, min_periods=24).std()
            prior7 = (c.shift(24) / c.shift(192) - 1) / (vol720 * np.sqrt(168))
            r30d = (c / c.shift(720) - 1) / (vol720 * np.sqrt(720))
            volratio = vol24 / vol720
            g120 = np.arange(0, n, 120); g24 = np.arange(0, n, 24)
            r120_all += list(f120.iloc[g120].dropna()); r24_all += list(f24.iloc[g24].dropna())
            prepared[w] = (g120, g24, f120, f24, surge, prior7, r30d, volratio, ts)
        if len(r120_all) < 10: continue
        d120, s120 = np.mean(r120_all), np.std(r120_all)
        d24, s24 = np.mean(r24_all), np.std(r24_all)
        for w, (g120, g24, f120, f24, surge, prior7, r30d, volratio, ts) in prepared.items():
            for i in g120:
                if pd.isna(f120.iloc[i]): continue
                rows120.append(dict(coin=coin, win=w, y=(f120.iloc[i]-d120)/s120, yraw=f120.iloc[i]-d120,
                    surge=surge.iloc[i], prior7=prior7.iloc[i], r30=r30d.iloc[i], vr=volratio.iloc[i]))
            for i in g24:
                if pd.isna(f24.iloc[i]): continue
                rows24.append(dict(coin=coin, y=(f24.iloc[i]-d24)/s24, surge=surge.iloc[i],
                    prior7=prior7.iloc[i], vr=volratio.iloc[i], wd=ts.iloc[i].dayofweek, hr=ts.iloc[i].hour))
    A = pd.DataFrame(rows120); B = pd.DataFrame(rows24)
    def summ(df, key):
        g = df.dropna(subset=[key, "y"]).groupby(key)["y"]
        out = g.agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.drop(columns="std")
    res = {}
    for k in ["surge", "prior7", "r30", "vr"]:
        A[k+"_q"] = pd.qcut(A[k], 5, labels=False, duplicates="drop")
        res["5d strength by "+k+" quintile"] = summ(A, k+"_q")
    A["combo"] = A["surge_q"].astype(str) + "_p" + np.sign(A["prior7"]).astype(str)
    res["5d by surge q x prior7 sign"] = summ(A, "combo")
    for k in ["surge", "prior7", "vr"]:
        B[k+"_q"] = pd.qcut(B[k], 5, labels=False, duplicates="drop")
        res["1d strength by "+k+" quintile"] = summ(B, k+"_q")
    res["1d by weekday"] = summ(B, "wd")
    res["5d by window"] = summ(A, "win")
    sp = {}
    for k in ["surge", "prior7", "r30", "vr"]:
        d = A.dropna(subset=[k, "y"]); sp["5d_"+k] = stats.spearmanr(d[k], d["y"])[0]
    for k in ["surge", "prior7", "vr"]:
        d = B.dropna(subset=[k, "y"]); sp["1d_"+k] = stats.spearmanr(d[k], d["y"])[0]
    res["spearman"] = pd.Series(sp)
    res["n"] = pd.Series({"n120": len(A), "n24": len(B)})
    return res
