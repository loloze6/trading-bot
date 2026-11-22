def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = {"1d":6, "7d":42, "14d":84}
    rows = {k: [] for k in H}
    for coin, wins in bars.items():
        drift = {}
        per = {k: [] for k in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            rng = (hi - lo).rolling(180, min_periods=45).mean()
            drop = (hi.rolling(6).max() - c) / rng
            prior = c.shift(6) / c.shift(186) - 1
            r24 = c / c.shift(6) - 1
            r7 = c / c.shift(42) - 1
            lr = np.log(c).diff()
            vol5 = lr.rolling(30).std()
            vol30 = lr.rolling(180).std()
            volratio = vol5 / vol30
            ts = pd.to_datetime(df["timestamp"])
            for k, h in H.items():
                idx = np.arange(0, len(df) - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                d = pd.DataFrame({"fwd": fwd, "drop": drop.values[idx], "prior": prior.values[idx],
                                  "r24": r24.values[idx], "r7": r7.values[idx], "volratio": volratio.values[idx],
                                  "vol30": vol30.values[idx], "hour": ts.dt.hour.values[idx],
                                  "wd": ts.dt.weekday.values[idx], "coin": coin, "w": w,
                                  "year": ts.dt.year.values[idx]})
                per[k].append(d)
        for k in H:
            d = pd.concat(per[k]); d["ex"] = d["fwd"] - d["fwd"].mean()
            for f in ["drop", "prior", "r24", "r7", "volratio", "vol30"]:
                d["q_" + f] = pd.qcut(d[f].rank(method="first"), 5, labels=False) if d[f].notna().sum() > 20 else np.nan
            rows[k].append(d)
    def summ(d, by):
        g = d.groupby(by)["ex"]
        r = g.agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r[["mean", "count", "t"]].round(4)
    for k in H:
        d = pd.concat(rows[k])
        for f in ["drop", "r24", "r7", "volratio", "vol30"]:
            out[f"{k} ex by {f} quintile"] = summ(d, "q_" + f)
        d["neg"] = (d["prior"] < 0).astype(int)
        out[f"{k} ex by drop q x prior<0"] = summ(d.dropna(subset=["q_drop"]), ["neg", "q_drop"])
    d = pd.concat(rows["1d"])
    out["1d ex by hour"] = summ(d, "hour")
    out["1d ex by weekday"] = summ(d, "wd")
    d7 = pd.concat(rows["7d"])
    out["7d ex by r7 q x year"] = d7.groupby(["year", "q_r7"])["ex"].mean().unstack().round(4)
    # book
    days = data["days"]
    bd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["w"] = w; bd.append(x)
    bd = pd.concat(bd)
    bd["wd"] = pd.to_datetime(bd["day"]).dt.weekday
    out["book by weekday"] = bd.groupby("wd")[["book_return", "coin_return"]].mean().round(5)
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): x = df.copy(); x["coin"] = coin; tr.append(x)
    tr = pd.concat(tr)
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry fc quartile"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
    out["trades by duration days"] = tr.groupby(pd.cut(tr["duration_minutes"] / 1440, [0, 7, 14, 21, 40, 1000]))["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
