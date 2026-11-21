def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            a = b["postRebalance_current_allocation"].astype(float)
            r1 = c.shift(-1) / c - 1
            lr = np.log(c).diff()
            vol30 = lr.rolling(30, min_periods=20).std() * np.sqrt(365)
            vol90 = lr.rolling(90, min_periods=40).std() * np.sqrt(365)
            ret28 = c / c.shift(28) - 1
            dd90 = c / c.rolling(90, min_periods=20).max() - 1
            pv = b["postRebalance_total_value"].astype(float)
            br = pv.shift(-1) / pv - 1  # approx book next-day
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)), "a": a, "r1": r1,
                               "fc": b["forecast"].astype(float), "vol30": vol30, "volratio": vol30 / vol90,
                               "ret28": ret28, "dd90": dd90, "ts": b["timestamp"]})
            rows.append(df)
    B = pd.concat(rows, ignore_index=True)
    B = B.dropna(subset=["r1", "a"])
    mu = B.groupby("coin")["r1"].mean()
    B["mu"] = B["coin"].map(mu)
    B["g"] = B["a"] * B["r1"]
    B["mkt"] = B["a"] * B["mu"]
    B["tim"] = B["g"] - B["mkt"]
    B["side"] = np.sign(B["a"]).map({1: "long", -1: "short", 0: "flat"})
    def agg(x):
        return pd.Series({"n": len(x), "mean_a": x["a"].mean(), "gain_bps": x["g"].mean() * 1e4,
                          "mkt_bps": x["mkt"].mean() * 1e4, "timing_bps": x["tim"].mean() * 1e4,
                          "t_gain": x["g"].mean() / (x["g"].std() / np.sqrt(len(x)))})
    out["by_side"] = B.groupby("side").apply(agg)
    B["fcq"] = pd.qcut(B["fc"], 5, labels=False, duplicates="drop")
    out["by_forecast_quintile"] = B.groupby("fcq").apply(agg).join(B.groupby("fcq")["fc"].mean().rename("fc_mean"))
    B["volq"] = B.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by_vol_tercile"] = B.groupby(["volq", "side"]).apply(agg)
    B["vrq"] = B.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by_volratio_tercile"] = B.groupby(["vrq", "side"]).apply(agg)
    out["by_coin"] = B.groupby("coin").apply(agg)
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w)[["day", "win", "coin", "book_return", "coin_return"]])
    D = pd.concat(D)
    P = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna().reset_index()
    P["wn"] = P["win"].str[1:].astype(int)
    P = P.sort_values(["wn", "day"]).reset_index(drop=True)
    out["book_by_window"] = P.groupby("wn").agg(n=("book", "size"), book_bps=("book", lambda x: x.mean() * 1e4),
                                               hold_bps=("hold", lambda x: x.mean() * 1e4),
                                               book_cum=("book", lambda x: (1 + x).prod() - 1),
                                               hold_cum=("hold", lambda x: (1 + x).prod() - 1))
    eq = (1 + P["book"]).cumprod()
    peak = eq.cummax()
    ddp = eq / peak - 1
    P["dd"] = ddp
    # episodes
    eps = []
    in_dd = False
    for k in range(len(P)):
        if ddp[k] < 0 and not in_dd:
            st = k; in_dd = True
        if in_dd and (ddp[k] == 0 or k == len(P) - 1):
            seg = P.iloc[st:k + 1]
            tr = seg["dd"].idxmin()
            eps.append({"start": st, "trough": tr, "end": k, "depth": seg["dd"].min(),
                        "days_to_trough": tr - st + 1, "wins": "-".join(sorted(set(P.loc[st:tr, "win"]), key=lambda s: int(s[1:]))),
                        "hold_ret_to_trough": (1 + P.loc[st:tr, "hold"]).prod() - 1})
            in_dd = False
    E = pd.DataFrame(eps).sort_values("depth").head(6).reset_index(drop=True)
    out["deepest_falls"] = E.drop(columns=["start", "trough", "end"])
    # what book held during the 3 deepest falls
    B["day"] = pd.to_datetime(B["ts"]).dt.floor("D")
    P["day_dt"] = pd.to_datetime(P["day"])
    hold_rows = []
    for j, e in E.head(4).iterrows():
        seg = P.loc[e["start"]:e["trough"]]
        keys = set(zip(seg["win"], seg["day_dt"].dt.floor("D")))
        sub = B[[ (w, d) in keys for w, d in zip(B["win"], B["day"])]]
        pre = B[(B["win"].isin(seg["win"].unique()))]
        first = sub.groupby("coin").head(1)
        hold_rows.append({"fall": j, "mean_alloc": sub["a"].mean(), "share_long": (sub["a"] > 0).mean(),
                          "share_short": (sub["a"] < 0).mean(), "gain_long_bps": sub.loc[sub.a > 0, "g"].mean() * 1e4,
                          "gain_short_bps": sub.loc[sub.a < 0, "g"].mean() * 1e4,
                          "start_ret28": first["ret28"].mean(), "start_dd90": first["dd90"].mean(),
                          "start_volratio": first["volratio"].mean(), "start_fc": first["fc"].mean(),
                          "coin_ret_in_fall": sub.groupby("coin")["r1"].apply(lambda x: (1 + x).prod() - 1).mean()})
    out["held_in_falls"] = pd.DataFrame(hold_rows)
    out["book_mean_bps"] = P["book"].mean() * 1e4
    out["share_long_bars"] = (B["a"] > 0).mean()
    out["share_short_bars"] = (B["a"] < 0).mean()
    # gain by ret28 tercile x dd90 tercile for longs
    B["r28q"] = B.groupby("coin")["ret28"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["long_by_ret28"] = B[B.a > 0].groupby("r28q").apply(agg)
    out["short_by_ret28"] = B[B.a < 0].groupby("r28q").apply(agg)
    return out
