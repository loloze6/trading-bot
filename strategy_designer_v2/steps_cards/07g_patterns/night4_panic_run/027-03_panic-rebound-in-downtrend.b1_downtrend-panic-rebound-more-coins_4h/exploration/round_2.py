def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    H = {"1d": 6, "3d": 18, "14d": 84}
    rows = {k: [] for k in H}
    for coin, wins in bars.items():
        per = {k: [] for k in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            lr = np.log(c).diff()
            vol5 = lr.rolling(30).std(); vol30 = lr.rolling(180).std()
            vr = vol5 / vol30
            r24 = c / c.shift(6) - 1
            r7 = c / c.shift(42) - 1
            prior = c.shift(6) / c.shift(186) - 1
            ts = pd.to_datetime(df["timestamp"])
            for k, h in H.items():
                idx = np.arange(0, len(df) - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                per[k].append(pd.DataFrame({"fwd": fwd, "vr": vr.values[idx], "r24": r24.values[idx],
                    "r7": r7.values[idx], "prior": prior.values[idx], "z24": (r24 / (vol30 * np.sqrt(6))).values[idx],
                    "w": w, "year": ts.dt.year.values[idx], "coin": coin}))
        for k in H:
            d = pd.concat(per[k]); d["ex"] = d["fwd"] - d["fwd"].mean()
            for f in ["vr", "z24"]:
                ok = d[f].notna()
                d.loc[ok, "q_" + f] = pd.qcut(d.loc[ok, f].rank(method="first"), 5, labels=False)
            rows[k].append(d)
    def summ(d, by):
        g = d.groupby(by)["ex"]; r = g.agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"])); return r[["mean", "count", "t"]].round(4)
    for k in H:
        d = pd.concat(rows[k]).dropna(subset=["q_vr", "r7"])
        d["r7pos"] = (d["r7"] > 0).astype(int)
        d["priorpos"] = (d["prior"] > 0).astype(int)
        out[f"{k} ex by vr q x r7>0"] = summ(d, ["r7pos", "q_vr"])
        out[f"{k} ex by vr q x prior>0"] = summ(d, ["priorpos", "q_vr"])
        out[f"{k} vr top-bottom by year"] = d.groupby(["year", "q_vr"])["ex"].mean().unstack()[[0.0, 4.0]].assign(diff=lambda x: x[4.0] - x[0.0]).round(4)
        d["rank_vr"] = d.groupby("coin")["vr"].rank(pct=True)
        out[f"{k} spearman vr per coin"] = d.groupby("coin").apply(lambda x: x["vr"].corr(x["ex"], method="spearman")).describe().round(3)
    d = pd.concat(rows["1d"]).dropna(subset=["q_z24", "prior"])
    d["priorpos"] = (d["prior"] > 0).astype(int)
    out["1d ex by z24 q x prior>0"] = summ(d, ["priorpos", "q_z24"])
    out["1d z24 bottom-q by year"] = summ(d[d["q_z24"] == 0], "year")
    d3 = pd.concat(rows["3d"]).dropna(subset=["q_z24", "prior"]); d3["priorpos"] = (d3["prior"] > 0).astype(int)
    out["3d ex by z24 q x prior>0"] = summ(d3, ["priorpos", "q_z24"])
    return out
