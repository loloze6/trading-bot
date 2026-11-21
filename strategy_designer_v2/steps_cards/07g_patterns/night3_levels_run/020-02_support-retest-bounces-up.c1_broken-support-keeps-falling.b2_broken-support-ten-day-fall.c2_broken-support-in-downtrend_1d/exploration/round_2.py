def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    res = {}
    for H in [10, 20]:
        rows = []
        for coin, wins in data["bars"].items():
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    allr.append(c[i + H] / c[i] - 1)
            dr = np.mean(allr); us = np.std(allr)
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"]
                lr = np.log(c).diff()
                vol = lr.rolling(30, min_periods=20).std() * np.sqrt(10)
                r10 = c / c.shift(10) - 1
                r60 = c / c.shift(60) - 1
                hi = c.rolling(60, min_periods=30).max(); lo = c.rolling(60, min_periods=30).min()
                pos = (c - lo) / (hi - lo)
                yr = pd.to_datetime(b["timestamp"]).dt.year
                wd = pd.to_datetime(b["timestamp"]).dt.dayofweek
                for i in range(0, len(c) - H, H):
                    fr = c.iloc[i + H] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, win=w, yr=yr.iloc[i], wd=wd.iloc[i], fwd=fr, ex=fr - dr,
                                     z=(fr - dr) / us, r10=r10.iloc[i], r10v=r10.iloc[i] / vol.iloc[i],
                                     r60=r60.iloc[i], pos=pos.iloc[i], fc=b["forecast"].iloc[i]))
        df = pd.DataFrame(rows).dropna(subset=["r10v"])
        out = {}
        for coin, d in df.groupby("coin"):
            r, p = stats.spearmanr(d["r10v"], d["z"])
            out[coin] = dict(rho=r, p=p, n=len(d))
        res[f"H{H}_rho_r10v_by_coin"] = pd.DataFrame(out).T
        df["early"] = df["yr"] <= 2021
        out = {}
        for k, d in df.groupby("early"):
            r, p = stats.spearmanr(d["r10v"], d["z"]); out[str(k)] = dict(rho=r, p=p, n=len(d))
        res[f"H{H}_rho_r10v_early_late"] = pd.DataFrame(out).T
        df["reg"] = np.where(df.r60 < 0, "down60", "up60")
        out = {}
        for k, d in df.dropna(subset=["r60"]).groupby("reg"):
            r, p = stats.spearmanr(d["r10v"], d["z"])
            out[k] = dict(rho=r, p=p, n=len(d), mean_fwd=d["fwd"].mean(), mean_ex=d["ex"].mean())
        res[f"H{H}_by_reg60"] = pd.DataFrame(out).T
        d = df.copy()
        d["b"] = d.groupby("coin")["r10v"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        g = d.groupby("b").agg(z=("z", "mean"), ex=("ex", "mean"), fwd=("fwd", "mean"), n=("z", "count"))
        g["t"] = d.groupby("b")["z"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        res[f"H{H}_q_r10v"] = g
        if H == 10:
            wdc = df.groupby(["coin"]).apply(lambda x: x[x.wd == 3]["z"].mean() - x[x.wd != 3]["z"].mean())
            res["thu_minus_other_by_coin"] = wdc
            sh = df[df.fc < 0]
            out = {}
            for k, dd in sh.groupby(np.where(sh.r10v < 0, "fell10", "rose10")):
                out[k] = dict(n=len(dd), short_total=-dd["fwd"].mean(), short_unusual=-dd["ex"].mean())
            res["short_cases_by_r10"] = pd.DataFrame(out).T
    return res
