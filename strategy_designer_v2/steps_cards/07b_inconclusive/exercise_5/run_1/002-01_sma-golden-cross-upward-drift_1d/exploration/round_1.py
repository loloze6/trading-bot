def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.sma_cross.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            # own 50/200 spread from closes in window (may be nan early)
            s50 = pd.Series(c).rolling(50).mean(); s200 = pd.Series(c).rolling(200).mean()
            spr = (s50 / s200 - 1).values
            r20 = pd.Series(c).pct_change(20).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (5, 10, 20, 40):
                for i in range(0, len(df) - h, h):
                    rows.append((coin, w, h, yr[i], f[i], raw[i], spr[i], r20[i], c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "yr", "f", "raw", "spr", "r20", "ret"])
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")

    def reg(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})

    out = {}
    out["by_h"] = d.groupby("h").apply(reg)
    out["by_h_rawspread"] = d.groupby("h").apply(lambda g: reg(g, "raw"))
    d10 = d[d.h == 10].copy()
    out["by_coin_h10"] = d10.groupby("coin").apply(reg)
    out["by_year_h10"] = d10.groupby("yr").apply(reg)
    # on vs off
    on = d10[d10.f > 0]["ex"]; off = d10[d10.f == 0]["ex"]
    out["on_minus_off_h10"] = pd.Series({"on_mean": on.mean(), "off_mean": off.mean(),
                                         "n_on": len(on), "n_off": len(off),
                                         "welch_t": stats.ttest_ind(on, off, equal_var=False).statistic})
    for h in (20, 40):
        dh = d[d.h == h]
        a = dh[dh.f > 0]["ex"]; b = dh[dh.f == 0]["ex"]
        out[f"on_minus_off_h{h}"] = pd.Series({"on": a.mean(), "off": b.mean(), "n_on": len(a), "n_off": len(b),
                                               "t": stats.ttest_ind(a, b, equal_var=False).statistic})
    pos = d10[d10.f > 0].copy()
    pos["q"] = pd.qcut(pos.f.rank(method="first"), 4, labels=False)
    out["on_quartiles_h10"] = pos.groupby("q").agg(fmean=("f", "mean"), ex=("ex", "mean"), n=("ex", "size"),
                                                   sd=("ex", "std"))
    d10["rq"] = pd.qcut(d10.raw.rank(method="first"), 5, labels=False)
    out["raw_quintiles_h10"] = d10.groupby("rq").agg(raw=("raw", "mean"), ex=("ex", "mean"), n=("ex", "size"),
                                                     sd=("ex", "std"))
    # book decomposition
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            b = bars[coin][w][["timestamp", "postRebalance_current_allocation"]].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            x = df.copy(); x["day"] = pd.to_datetime(x["day"]).dt.floor("D")
            x = x.merge(b.groupby("day")["postRebalance_current_allocation"].last().shift(1).rename("pos"),
                        left_on="day", right_index=True, how="left")
            x["coin"] = coin
            dd.append(x)
    dd = pd.concat(dd)
    dd["cm"] = dd.groupby("coin")["coin_return"].transform("mean")
    out["book_decomp"] = pd.Series({"book_mean": dd["book_return"].mean(),
                                    "market_part": (dd["pos"] * dd["cm"]).mean(),
                                    "mean_pos": dd["pos"].mean()})
    return out
