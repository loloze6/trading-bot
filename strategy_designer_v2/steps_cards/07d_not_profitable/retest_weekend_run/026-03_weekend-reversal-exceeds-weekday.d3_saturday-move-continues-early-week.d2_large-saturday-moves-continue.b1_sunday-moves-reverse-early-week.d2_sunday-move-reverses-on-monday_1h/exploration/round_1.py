def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []
    drift = {}
    for coin in bars:
        # normal drift per horizon
        dr = {}
        for h in [6, 12, 24, 48]:
            vals = []
            for w, b in bars[coin].items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.append(c[idx + h] / c[idx] - 1)
            vals = np.concatenate(vals)
            dr[h] = (np.mean(vals), np.std(vals))
        drift[coin] = dr
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=720).mean()
            hr = np.log(c).diff()
            vol = hr.rolling(720, min_periods=720).std()
            nxt = ts + pd.Timedelta(hours=1)
            mask = (nxt.dt.weekday == 0) & (nxt.dt.hour == 0)
            for i in np.where(mask.values)[0]:
                if i < 24 or np.isnan(r24.iloc[i]):
                    continue
                d = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                     "sun": r24.iloc[i], "z": r24.iloc[i] / mabs.iloc[i] if mabs.iloc[i] > 0 else np.nan,
                     "vol": vol.iloc[i], "alloc": b["postRebalance_current_allocation"].iloc[i],
                     "fc": b["forecast"].iloc[i]}
                s = -np.sign(d["sun"])
                for h in [6, 12, 24, 48]:
                    if i + h < len(c):
                        d[f"f{h}"] = s * (c.iloc[i + h] / c.iloc[i] - 1 - drift[coin][h][0])
                        d[f"raw{h}"] = s * (c.iloc[i + h] / c.iloc[i] - 1)
                    else:
                        d[f"f{h}"] = np.nan
                # hours 24-48 alone
                if i + 48 < len(c):
                    d["f24_48"] = s * (c.iloc[i + 48] / c.iloc[i + 24] - 1)
                rows.append(d)
    df = pd.DataFrame(rows)
    df = df[df["sun"] != 0]
    out = {}
    def summ(g, col="f24"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["horizons"] = pd.DataFrame({h: summ(df, h) for h in ["f6", "f12", "f24", "f48", "f24_48"]}).T
    df["zq"] = pd.qcut(df["z"].abs(), 5, labels=False)
    out["by_absz_quintile"] = df.groupby("zq").apply(lambda g: pd.concat([summ(g), pd.Series({"absz": g["z"].abs().mean(), "absalloc": g["alloc"].abs().mean(), "sunabs": g["sun"].abs().mean()})]))
    df["volq"] = df.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["by_vol_tercile"] = df.groupby("volq").apply(summ)
    out["by_coin"] = df.groupby("coin").apply(lambda g: pd.concat([summ(g), pd.Series({"absalloc": g["alloc"].abs().mean(), "usual24": drift[g.name][24][1]})]))
    out["by_year"] = df.groupby("year").apply(summ)
    out["by_side"] = df.groupby(np.sign(-df["sun"])).apply(summ)
    # cross: large |z| and high vol
    out["absz_hi_x_vol"] = df.groupby([df["zq"] >= 3, "volq"]).apply(summ)
    # trades
    tr = []
    for coin in trades:
        for w, t in trades[coin].items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    tr = pd.concat(tr)
    out["trades"] = pd.Series({"n": len(tr), "mean_pl": tr["profit_loss_percent"].mean(), "mean_net": tr["net_profit_loss_percent"].mean(),
                               "med_dur_h": tr["duration_minutes"].median() / 60, "mean_dur_h": tr["duration_minutes"].mean() / 60,
                               "share_long": (tr["side"] == "LONG").mean()})
    out["alloc_stats"] = df["alloc"].abs().describe()
    # book daily
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["day"] = pd.to_datetime(dd["day"])
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wd"] = bk["day"].dt.weekday
    out["book_by_weekday"] = bk.groupby("wd")["book_return"].agg(["mean", "std", "count"])
    return out
