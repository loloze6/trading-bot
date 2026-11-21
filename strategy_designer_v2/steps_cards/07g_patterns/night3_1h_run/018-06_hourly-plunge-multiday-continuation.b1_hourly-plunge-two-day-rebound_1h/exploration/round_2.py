def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().shift(1).rolling(720, min_periods=120).mean()
            ratio = r24 / mabs
            vol = np.log(c).diff().rolling(720, min_periods=120).std()
            n = len(c)
            for h in [24, 48]:
                idx = np.arange(0, n - h, h)
                fwd = (c.values[idx + h] / c.values[idx]) - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "yr": ts.dt.year.values[idx],
                                          "ratio": ratio.values[idx], "vol": vol.values[idx], "fwd": fwd}))
    R = pd.concat(rows, ignore_index=True)
    R["drift"] = R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["sd"] = R.groupby(["coin", "h"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"] / R["sd"]
    R = R.dropna(subset=["ratio", "vol"])
    R["vt"] = R.groupby(["coin", "h"])["vol"].transform(lambda s: pd.qcut(s, 3, labels=["lowvol", "midvol", "highvol"])).astype(str)
    def summ(g):
        n = len(g)
        return pd.Series({"n": n, "ex_bps": g["ex"].mean() * 1e4, "tot_bps": g["fwd"].mean() * 1e4,
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": g["str"].mean()})
    out = {}
    hv = R[(R.vt == "highvol") & (R.ratio < 0)].copy()
    hv["rb"] = pd.cut(hv["ratio"], [-np.inf, -2, -1.5, -1, -0.5, 0]).astype(str)
    out["highvol_drops_by_size"] = hv.groupby(["h", "rb"]).apply(summ)
    hd = R[(R.vt == "highvol") & (R.ratio < -1)]
    out["highvol_drop1_h48_by_coin"] = hd[hd.h == 48].groupby("coin").apply(summ)
    out["highvol_drop1_h48_by_year"] = hd[hd.h == 48].groupby("yr").apply(summ)
    out["highvol_drop1_h24_by_year"] = hd[hd.h == 24].groupby("yr").apply(summ)
    sp = {}
    for h in [24, 48]:
        for v in ["lowvol", "midvol", "highvol"]:
            s = R[(R.h == h) & (R.vt == v) & (R.ratio < 0)]
            rho, p = stats.spearmanr(-s["ratio"], s["ex"])
            sp[f"h{h}_{v}"] = (rho, p, len(s))
    out["spearman_dropsize_ex_by_vol"] = pd.DataFrame(sp, index=["rho", "p", "n"]).T
    # interaction regression: ex/sd on dropsize * vol rank
    s = R[(R.h == 48) & (R.ratio < 0)].copy()
    s["vr"] = s.groupby("coin")["vol"].rank(pct=True)
    s["x"] = (-s["ratio"]) * s["vr"]
    out["spearman_drop_x_volrank_h48"] = pd.Series(stats.spearmanr(s["x"], s["ex"]), index=["rho", "p"])
    # book: daily returns by coin vol tercile
    dl = []
    for coin, wins in days.items():
        for w, d in wins.items():
            dl.append(d[["book_return", "coin_return"]].assign(coin=coin))
    Dd = pd.concat(dl).dropna()
    out["book_daily"] = pd.Series({"book_mean_bps": Dd.book_return.mean() * 1e4, "coin_mean_bps": Dd.coin_return.mean() * 1e4,
                                   "n": len(Dd)})
    return out
