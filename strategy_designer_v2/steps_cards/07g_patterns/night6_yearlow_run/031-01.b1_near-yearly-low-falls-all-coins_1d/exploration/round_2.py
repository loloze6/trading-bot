def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]

    def clustered_t(d, col):
        # mean of col with cases of one day taken together (deviations summed per day)
        d = d.dropna(subset=[col])
        m = d[col].mean()
        dev = (d[col] - m).groupby(d["day"]).sum()
        G = len(dev); n = len(d)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return m, m / se if se and se > 0 else np.nan, n, G

    # drift per coin for each horizon from non-overlapping grids
    recs = {h: [] for h in (1, 5, 10, 20)}
    for coin, wd in bars.items():
        for w, df in wd.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            raw = df.get("debug_info.components.low_prox.last_history_value")
            raw = raw.astype(float).values if raw is not None else np.full(n, np.nan)
            lr = np.log(c)
            r1 = np.r_[np.nan, np.diff(lr)]
            vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
            z1 = r1 / vol20
            p20 = np.r_[np.full(20, np.nan), c[20:] / c[:-20] - 1] if n > 20 else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            for h in recs:
                for i in range(0, n, h):
                    if i + h >= n: break
                    recs[h].append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                        z1=z1[i], raw=raw[i], p20=p20[i], f=c[i + h] / c[i] - 1))
    for h, rr in recs.items():
        g = pd.DataFrame(rr)
        g["ex"] = g["f"] - g.groupby("coin")["f"].transform("mean")
        d = g.dropna(subset=["z1", "ex"]).copy()
        d["q"] = pd.qcut(d["z1"].rank(method="first"), 5, labels=False)
        tab = []
        for q, dq in d.groupby("q"):
            m, t, nn, G = clustered_t(dq, "ex")
            tab.append(dict(q=q, z1max=dq["z1"].max(), mean=m, t_cl=t, n=nn, days=G))
        out[f"ex{h}_by_z1_q_clustered"] = pd.DataFrame(tab).set_index("q")
        # z1 bottom quintile by year
        if h in (5, 20):
            b = d[d["q"] == 0]
            out[f"ex{h}_z1_bottomq_by_year"] = b.groupby("year")["ex"].agg(["size", "mean"])
            # day-pooled regression of ex on z1
            dd = d.groupby("day")[["z1", "ex"]].mean()
            sl = stats.linregress(dd["z1"], dd["ex"])
            out[f"ex{h}_on_z1_daypooled"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "days": len(dd)})
        if h in (5, 20):
            # at the yearly low (raw near 1)
            for thr in (0.9, 0.99):
                a = g[g["raw"] >= thr]
                m, t, nn, G = clustered_t(a, "ex")
                out[f"ex{h}_raw_ge_{thr}"] = pd.Series({"mean": m, "t_cl": t, "n": nn, "days": G})

    # weekday, day-pooled across coins
    dr = []
    for coin, wd in data["days"].items():
        for w, df in wd.items():
            x = df[["day", "coin_return", "book_return"]].copy(); x["coin"] = coin
            dr.append(x)
    D = pd.concat(dr); D["day"] = pd.to_datetime(D["day"])
    P = D.groupby("day")[["coin_return", "book_return"]].mean()
    P["wd"] = P.index.dayofweek; P["year"] = P.index.year
    t = P.groupby("wd")["coin_return"].agg(["size", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["size"]))
    out["coin_ret_by_weekday_daypooled"] = t.drop(columns="std")
    out["coin_ret_wd_by_year"] = P.pivot_table(index="year", columns="wd", values="coin_return", aggfunc="mean")
    # per-coin weekday 5 (Saturday) mean minus others
    D["wd"] = D["day"].dt.dayofweek
    pc = D.groupby(["coin", "wd"])["coin_return"].mean().unstack()
    out["coin_ret_wd_by_coin"] = pc
    # book's largest days: what preceded
    P["prev_coin"] = P["coin_return"].shift(1)
    big = P["book_return"].abs().quantile(0.95)
    out["book_extreme_days"] = pd.Series({
        "n_gain": (P["book_return"] > big).sum(), "coin_ret_on_gain_days": P.loc[P["book_return"] > big, "coin_return"].mean(),
        "n_loss": (P["book_return"] < -big).sum(), "coin_ret_on_loss_days": P.loc[P["book_return"] < -big, "coin_return"].mean()})
    return out
