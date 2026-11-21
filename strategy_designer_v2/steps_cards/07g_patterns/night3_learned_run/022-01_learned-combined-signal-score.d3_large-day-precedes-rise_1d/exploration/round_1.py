def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sc = r1.abs().rolling(60, min_periods=20).mean().shift(1)
            z = r1 / sc
            vol20 = r1.rolling(20, min_periods=15).std()
            vol60 = r1.rolling(60, min_periods=40).std()
            mom20 = c / c.shift(20) - 1
            mom20z = mom20 / (vol60 * np.sqrt(20))
            near = c / c.rolling(60, min_periods=40).max() - 1
            nearz = near / (vol60 * np.sqrt(20))
            rng = (b["high"] - b["low"]) / c
            rngz = rng / rng.rolling(60, min_periods=20).mean().shift(1)
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            n = len(b)
            for h in (1, 5, 10, 20):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, pos=i, z=z[i], r1=r1[i], volr=vol20[i]/vol60[i] if vol60[i] else np.nan,
                                     mom=mom20z[i], near=nearz[i], rngz=rngz[i], wd=wd[i], fwd=fwd[i],
                                     fc=b["forecast"][i]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    def terc(col, h, name):
        d = df[(df.h == h)].dropna(subset=[col, "ex"])
        q = d[col].rank(pct=True)
        top, bot = d[q > 2/3]["ex"], d[q <= 1/3]["ex"]
        mid = d[(q > 1/3) & (q <= 2/3)]["ex"]
        t = stats.ttest_ind(top, bot, equal_var=False)
        return {"var": name, "h": h, "n": len(d), "top": top.mean(), "mid": mid.mean(), "bot": bot.mean(),
                "top-bot": top.mean() - bot.mean(), "t": t.statistic}
    res = []
    for col in ["z", "volr", "mom", "near", "rngz", "fc"]:
        for h in (1, 5, 10, 20):
            res.append(terc(col, h, col))
    out["terciles"] = pd.DataFrame(res).round(4)
    # signed z quintiles at 5 and 10
    for h in (5, 10):
        d = df[df.h == h].dropna(subset=["z", "ex"]).copy()
        d["q"] = pd.qcut(d["z"], 5, labels=False)
        g = d.groupby("q")["ex"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["zmean"] = d.groupby("q")["z"].mean()
        out[f"z_quintiles_h{h}"] = g.round(4)
    # weekday
    d = df[df.h == 1].dropna(subset=["ex"])
    g = d.groupby("wd")["ex"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["weekday_h1"] = g.round(5)
    # per coin top-bot of fc at 5
    pc = []
    for coin in df.coin.unique():
        d = df[(df.h == 5) & (df.coin == coin)].dropna(subset=["z", "ex"])
        q = d["z"].abs().rank(pct=True)
        top, bot = d[q > 2/3]["ex"], d[q <= 1/3]["ex"]
        pc.append({"coin": coin, "n": len(d), "absz_top-bot": top.mean()-bot.mean(), "t": stats.ttest_ind(top, bot, equal_var=False).statistic})
    out["per_coin_absz_h5"] = pd.DataFrame(pc).round(4)
    # book: market vs timing
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"] = coin; dd["win"] = w; br.append(dd)
    D = pd.concat(br)
    out["book_coin_corr"] = float(D[["book_return", "coin_return"]].corr().iloc[0, 1])
    out["book_mean_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean().round(5)
    return out
