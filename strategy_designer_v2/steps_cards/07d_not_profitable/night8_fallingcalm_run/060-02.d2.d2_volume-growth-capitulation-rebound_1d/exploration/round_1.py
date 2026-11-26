def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    P = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().dropna()
    P = P.sort_values(["wn", "day"]).reset_index(drop=True)
    v = (1 + P["br"]).cumprod()
    dd_ = v / v.cummax() - 1
    P["dd"] = dd_
    P["peak"] = v.cummax()
    # per-window stats
    def mdd(x):
        vv = (1 + x).cumprod(); return (vv / vv.cummax() - 1).min()
    out["per_window"] = P.groupby("wn").agg(n=("br", "size"), book_sum=("br", "sum"), coin_sum=("cr", "sum"),
                                             book_mdd=("br", mdd)).round(4)
    # deepest fall episode
    i_tr = dd_.idxmin()
    pk = v[:i_tr + 1].idxmax()
    out["deepest"] = pd.Series({"depth": dd_.min(), "peak_window": P.loc[pk, "wn"], "trough_window": P.loc[i_tr, "wn"],
                                "days": i_tr - pk})
    # contributions by coin during deepest fall
    seg = P.loc[pk:i_tr, ["wn", "day"]]
    Dm = D.merge(seg, on=["wn", "day"])
    out["deep_by_coin"] = Dm.groupby("coin")["book_return"].sum().round(4)
    # trades analysis with features at entry
    T = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            ret60 = cl / cl.shift(60) - 1
            fwd5 = cl.shift(-5) / cl - 1
            alloc = b["postRebalance_current_allocation"].fillna(0)
            for i in range(0, len(b) - 5, 5):
                T.append(dict(coin=c, w=w, alloc=alloc[i], fc=b["forecast"][i], fwd5=fwd5[i],
                              vol30=vol30[i], ret60=ret60[i], ret10=cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan,
                              ret3=cl[i] / cl[i - 3] - 1 if i >= 3 else np.nan,
                              vg=b.get("debug_info.components.vol_growth.last_history_value", pd.Series(np.nan, index=b.index))[i],
                              regime=b["regime"][i]))
    G = pd.DataFrame(T)
    G["volrank"] = G.groupby("coin")["vol30"].rank(pct=True)
    mu = G.groupby("coin")["fwd5"].transform("mean")
    G["unus"] = G["fwd5"] - mu
    inpos = G[G["alloc"] > 0]
    out["inpos_n_mean"] = pd.Series({"n": len(inpos), "fwd5": inpos["fwd5"].mean(), "unus": inpos["unus"].mean()})
    def tab(df, col, q=3):
        x = df.dropna(subset=[col, "fwd5"]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        return x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("fwd5", "size"), mean=("fwd5", "mean"),
                                  std=("fwd5", "std"), worst=("fwd5", "min"), share_neg=("fwd5", lambda s: (s < 0).mean())).round(4)
    out["inpos_by_volrank"] = tab(inpos, "volrank")
    out["inpos_by_ret10"] = tab(inpos, "ret10")
    out["inpos_by_ret60"] = tab(inpos, "ret60")
    out["inpos_by_ret3"] = tab(inpos, "ret3")
    out["inpos_by_fc"] = tab(inpos, "fc")
    # falling profile, flat (condition without signal) by volrank
    fl = G[(G["ret60"] < -0.10) & (G["alloc"] == 0)]
    out["falling_flat_by_volrank"] = tab(fl, "volrank")
    # trades
    TR = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; TR.append(t)
    TR = pd.concat(TR)
    out["trades"] = pd.Series({"n": len(TR), "mean_net": TR["net_profit_loss_percent"].mean(),
                               "median": TR["net_profit_loss_percent"].median(),
                               "worst": TR["net_profit_loss_percent"].min(),
                               "dur_days_mean": TR["duration_minutes"].mean() / 1440,
                               "share_neg": (TR["net_profit_loss_percent"] < 0).mean()})
    TR["db"] = pd.cut(TR["duration_minutes"] / 1440, [0, 5.5, 10.5, 20.5, 1000])
    out["trades_by_dur"] = TR.groupby("db")["net_profit_loss_percent"].agg(["size", "mean", "min"]).round(3)
    return out
