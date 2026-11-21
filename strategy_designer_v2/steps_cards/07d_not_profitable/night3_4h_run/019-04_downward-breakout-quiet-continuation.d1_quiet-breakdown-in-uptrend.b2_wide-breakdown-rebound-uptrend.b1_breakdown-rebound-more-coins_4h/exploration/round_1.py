def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # pooled daily book: per window & day, mean over coins
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    P = P.dropna()
    eq = (1 + P["book_return"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    P["dd"] = dd
    i = int(np.argmin(dd)); pk = int(np.argmax(eq[:i+1]))
    out["deepest_fall"] = pd.Series({"depth": dd[i], "days_peak_to_trough": i - pk,
                                     "window_of_peak": P["wn"].iloc[pk], "window_of_trough": P["wn"].iloc[i]})
    # fall by window
    byw = P.groupby("wn").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                              book_sum=("book_return", "sum"), min_dd=("dd", "min"), n=("book_return", "size"))
    out["by_window"] = byw
    # bar-level: exposure and gain by state
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; lo = b["low"]; hi = b["high"]
            r180 = cl / cl.shift(180) - 1
            prevlow = lo.shift(1).rolling(12).min()
            brk = cl / prevlow - 1
            ret1 = cl / cl.shift(1) - 1
            ret6 = cl / cl.shift(6) - 1
            vol = ret1.rolling(180).std()
            fwd18 = cl.shift(-18) / cl - 1
            sig = (b["regime"] == "trending")
            pos = b["postRebalance_current_allocation"].fillna(0)
            g = pos * (cl.shift(-1) / cl - 1)
            df = pd.DataFrame({"sig": sig, "r180": r180, "brk": brk, "ret1": ret1, "ret6": ret6,
                               "vol": vol, "fwd18": fwd18, "pos": pos, "g": g,
                               "wid": b.get("debug_info.components.width.last_history_value")})
            df["coin"] = c; df["w"] = w
            # grid cases: first signal per 18-cell
            df["cell"] = np.arange(len(df)) // 18
            recs.append(df)
    B = pd.concat(recs, ignore_index=True)
    out["exposure"] = pd.Series({"share_bars_long": (B["pos"] > 0).mean(),
                                 "mean_pos_when_long": B.loc[B["pos"] > 0, "pos"].mean(),
                                 "share_bars_signal": B["sig"].mean()})
    S = B[B["sig"] & B["fwd18"].notna()].groupby(["coin", "w", "cell"]).first().reset_index()
    drift = B.groupby("coin")["fwd18"].mean()  # approx
    S["u"] = S["fwd18"] - S["coin"].map(drift)
    S["ret6n"] = S["ret6"] / S["vol"]
    S["r180n"] = S["r180"] / (S["vol"] * np.sqrt(180))
    S["brkn"] = S["brk"] / S["vol"]
    def q(col):
        t = S.dropna(subset=[col, "u"]).copy()
        t["q"] = pd.qcut(t[col], 5, labels=False, duplicates="drop")
        return t.groupby("q").agg(mid=(col, "median"), mean_u=("u", "mean"), mean_tot=("fwd18", "mean"),
                                  n=("u", "size"), sd=("u", "std"),
                                  neg_share=("fwd18", lambda x: (x < -0.1).mean()))
    for col in ["r180n", "ret6n", "brkn", "vol", "wid"]:
        out["q_" + col] = q(col)
    # trades
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; T.append(t)
    T = pd.concat(T)
    out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
                               "mean_gross": T["profit_loss_percent"].mean(),
                               "median_dur_h": T["duration_minutes"].median() / 60,
                               "worst5pct": T["net_profit_loss_percent"].quantile(0.05),
                               "share_neg": (T["net_profit_loss_percent"] < 0).mean()})
    return out
