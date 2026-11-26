def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [5, 10, 20, 40]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.mom60.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            # trailing 60-day vol regime proxy: 20-day abs return
            for h in H:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i],
                                     r=c[i + h] / c[i] - 1, year=ts.iloc[i].year,
                                     r20past=(c[i] / c[i - 20] - 1) if i >= 20 else np.nan))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")
    out = {}
    def slope(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 10 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g["f"], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))
    out["slope by horizon"] = d.groupby("h").apply(slope)
    d20 = d[d.h == 20].copy()
    out["slope by coin h20"] = d20.groupby("coin").apply(slope)
    out["slope by window h20"] = d20.groupby("w").apply(slope)
    out["slope by year h20"] = d20.groupby("year").apply(slope)
    d20["side"] = np.sign(d20["f"])
    out["by side h20"] = d20.groupby("side")["ex"].agg(["count", "mean", "std"]).assign(
        t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    d20["q"] = pd.qcut(d20["f"], 5, labels=False, duplicates="drop")
    out["by forecast quintile h20"] = d20.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"),
                                                           ex=("ex", "mean"), r=("r", "mean"))
    for h in [10, 40]:
        dh = d[d.h == h].copy()
        dh["q"] = pd.qcut(dh["f"], 5, labels=False, duplicates="drop")
        out[f"by quintile h{h}"] = dh.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), ex=("ex", "mean"))
    # regime: past 20-day move size (choppiness proxy) splits
    d20["absr20"] = d20["r20past"].abs()
    d20["vq"] = pd.qcut(d20["absr20"], 3, labels=False, duplicates="drop")
    out["slope by recent 20d |move| tercile h20"] = d20.groupby("vq").apply(slope)
    out["raw vs forecast corr"] = float(d20[["raw", "f"]].corr().iloc[0, 1])
    return out
