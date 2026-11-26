def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    hs = [3, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            dist = df.get("debug_info.components.ma_dist.last_history_value")
            sma = pd.Series(c).rolling(20).mean().values
            d_raw = (c / sma - 1) * 100
            ret60 = pd.Series(c).pct_change(60).values * 100
            vol30 = pd.Series(c).pct_change().rolling(30).std().values
            for h in hs:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                     year=str(df["timestamp"].iloc[i])[:4],
                                     fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                     dist=d_raw[i], r60=ret60[i], vol30=vol30[i],
                                     fwd=c[i + h] / c[i] - 1))
    R = pd.DataFrame(rows)
    # drift per coin per h over all windows (grid)
    R["drift"] = R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["ex"] = R["fwd"] - R["drift"]
    out = {}
    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, corr=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr, corr=r.rvalue))
    act = R[(R.reg == "unknown") & (R.fc != 0)]
    out["slope by horizon, choppy active"] = act.groupby("h").apply(slope)
    out["slope by horizon, all bars with fc!=0 (any regime) using raw dist"] = R.dropna(subset=["dist"]).groupby("h").apply(lambda g: slope(g, "dist"))
    a10 = act[act.h == 10].copy()
    out["h10 by coin"] = a10.groupby("coin").apply(slope)
    out["h10 by year"] = a10.groupby("year").apply(slope)
    a10["side"] = np.where(a10.fc > 0, "above", "below")
    out["h10 by side: mean ex, mean fc"] = a10.groupby("side").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_fc=("fc", "mean"),
                                                                  t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    a10["q"] = pd.qcut(a10.fc, 5, labels=False)
    out["h10 by forecast quintile"] = a10.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), mean_ex=("ex", "mean"),
                                                           t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    a10["vq"] = a10.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x.rank(method="first"), 2, labels=["calm", "agit"]))
    out["h10 by vol half (within coin)"] = a10.groupby("vq").apply(slope)
    # other regimes: rising/falling, with raw dist
    R10 = R[(R.h == 10)].dropna(subset=["dist", "r60"]).copy()
    R10["trend"] = np.where(R10.r60 > 10, "rising", np.where(R10.r60 < -10, "falling", "choppy"))
    out["h10 raw dist slope by trend (r60 within window)"] = R10.groupby("trend").apply(lambda g: slope(g, "dist"))
    return out
