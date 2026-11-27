def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=20).std()
            hi20 = c.rolling(20, min_periods=20).max()
            depth = (c / hi20 - 1) / sd20
            tr60 = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            sdw = r1.std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "r1": r1, "depth": depth, "tr60": tr60, "tr20": tr20,
                "agit": sd20 / sdw,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "regime": b["regime"].astype(str),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = {}
    for h in [1, 2, 3, 5]:
        drift[h] = A.groupby("coin")["f%d" % h].mean()
    for h in [1, 2, 3, 5]:
        A["u%d" % h] = -(A["f%d" % h] - A["coin"].map(drift[h]))
        A["s%d" % h] = -A["f%d" % h]
    act = A[A["fc"] < 0].copy()
    out = {}
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # horizons (non-overlap ignored for h>1, informative)
    out["active by horizon (short unusual, total)"] = pd.DataFrame({h: pd.concat([summ(act, "u%d" % h), summ(act, "s%d" % h).add_prefix("tot_")]) for h in [1, 2, 3, 5]})
    act["dq"] = pd.qcut(act["fc"], 5, labels=False)  # 0 = deepest
    out["by forecast quintile (0 deepest)"] = act.groupby("dq").apply(lambda g: pd.concat([summ(g, "u1"), summ(g, "s1").add_prefix("tot_"), pd.Series({"fc": g["fc"].mean(), "u3%": 100 * g["u3"].mean()})]))
    act["trb"] = pd.cut(act["tr60"], [-9, -0.3, -0.1, 0.1])
    out["by trend60 bucket"] = act.groupby("trb").apply(lambda g: pd.concat([summ(g, "u1"), summ(g, "s1").add_prefix("tot_")]))
    act["ag"] = pd.qcut(act["agit"], 3, labels=["calm", "mid", "agit"])
    out["by agitation tercile (sd20/window sd)"] = act.groupby("ag").apply(lambda g: pd.concat([summ(g, "u1"), summ(g, "s1").add_prefix("tot_")]))
    act["r1q"] = pd.qcut(act["r1"], 4, labels=False)
    out["by up-day size quartile"] = act.groupby("r1q").apply(lambda g: pd.concat([summ(g, "u1"), pd.Series({"r1%": 100 * g["r1"].mean()})]))
    out["by window"] = act.groupby("w").apply(lambda g: summ(g, "u1"))
    # book daily
    D = []
    for coin, ws in days.items():
        for w, d in ws.items():
            dd = d[["book_return", "coin_return"]].copy(); dd["w"] = w; dd["coin"] = coin; dd["i"] = np.arange(len(d))
            D.append(dd)
    D = pd.concat(D)
    bk = D.groupby(["w", "i"])[["book_return", "coin_return"]].mean().reset_index()
    out["book by window"] = bk.groupby("w").agg(book_mean=("book_return", "mean"), book_sd=("book_return", "std"), hold_mean=("coin_return", "mean"), n=("i", "size"))
    # drawdown chain
    br = bk["book_return"].fillna(0)
    v = (1 + br).cumprod(); dd = v / v.cummax() - 1
    bk["dd"] = dd.values
    out["deepest fall"] = pd.Series({"maxdd": dd.min(), "window_of_trough": bk.loc[dd.idxmin(), "w"]})
    out["worst window dd"] = bk.groupby("w")["book_return"].apply(lambda x: ((1 + x.fillna(0)).cumprod() / (1 + x.fillna(0)).cumprod().cummax() - 1).min())
    # loss tails: worst 5% cases characteristics
    a1 = act.dropna(subset=["u1"])
    lo = a1["s1"] < a1["s1"].quantile(0.05)
    out["worst 5% cases vs rest"] = pd.DataFrame({"worst": a1[lo][["r1", "depth", "tr60", "tr20", "agit"]].mean(), "rest": a1[~lo][["r1", "depth", "tr60", "tr20", "agit"]].mean()})
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = pd.Series({"n": len(T), "mean_gross%": T["profit_loss_percent"].mean(), "mean_net%": T["net_profit_loss_percent"].mean(), "mean_dur_days": T["duration_minutes"].mean() / 1440, "short_share": (T["side"] == "SHORT").mean()})
    return out
