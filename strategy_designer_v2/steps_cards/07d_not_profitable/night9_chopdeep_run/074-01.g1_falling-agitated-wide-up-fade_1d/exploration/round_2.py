def explore(data):
    import pandas as pd, numpy as np
    out = {}
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; rng = b["high"] - b["low"]
            mult = rng / rng.rolling(20, min_periods=20).mean()
            r1 = cl.pct_change()
            nxt = cl.shift(-1) / cl - 1
            nhigh = b["high"].shift(-1) / cl - 1
            clv = (cl - b["low"]) / rng
            f = b["forecast"]
            sig = (f < 0) & ~(f.shift(1) < 0)
            inprof = b["regime"] != "chop"
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            cs.append(pd.DataFrame({"coin": c, "w": w, "day": day, "nxt": nxt, "nhigh": nhigh, "mult": mult,
                                    "r1": r1, "clv": clv, "sig": sig, "inprof": inprof, "regime": b["regime"]}))
    G = pd.concat(cs)
    G["drift"] = G["coin"].map(G.groupby("coin")["nxt"].mean())
    G["un"] = -(G["nxt"] - G["drift"])
    out["regime_counts"] = G["regime"].value_counts()
    def stat(x):
        x = x.dropna(subset=["un"])
        dsum = x.groupby("day")["un"].sum()
        t = dsum.mean() / dsum.std() * np.sqrt(len(dsum)) * 1.0 if len(dsum) > 2 else np.nan
        return pd.Series({"mean": x["un"].mean(), "n": len(x), "days": len(dsum), "t_daypooled": t})
    S = G[G["sig"]]
    S = S.assign(clvb=pd.cut(S["clv"], [0, 0.5, 0.68, 0.85, 1.0001], include_lowest=True))
    out["signal_by_clv"] = S.groupby("clvb").apply(stat)
    # baseline: up days in profile, NOT signal (mult<=1), by clv
    base = G[G["inprof"] & (G["r1"] > 0) & (G["mult"] <= 1.0) & ~G["sig"]]
    base = base.assign(clvb=pd.cut(base["clv"], [0, 0.5, 0.68, 0.85, 1.0001], include_lowest=True))
    out["noSignal_upday_inprofile_by_clv"] = base.groupby("clvb").apply(stat)
    # all in-profile days not signal, by clv (any day)
    nb = G[G["inprof"] & ~G["sig"]]
    nb = nb.assign(clvb=pd.cut(nb["clv"], [0, 0.5, 0.68, 0.85, 1.0001], include_lowest=True))
    out["noSignal_anyday_inprofile_by_clv"] = nb.groupby("clvb").apply(stat)
    out["signal_clv_hi_vs_lo"] = pd.Series({"hi(>0.68)": stat(S[S["clv"] > 0.68])["mean"],
                                            "lo(<=0.68)": stat(S[S["clv"] <= 0.68])["mean"],
                                            "t_hi": stat(S[S["clv"] > 0.68])["t_daypooled"]})
    # next-day high on signal cases: share with high > +10%
    out["next_high_quantiles"] = S["nhigh"].describe()
    # book recomputed: zero coin's book return on day after a low-clv signal
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return"]].copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    low = S[S["clv"] <= 0.68][["coin", "w", "day"]].copy()
    low["day"] = low["day"] + pd.Timedelta(days=1)
    low["kill"] = True
    D = D.merge(low, on=["coin", "w", "day"], how="left")
    D["kill"] = D["kill"].fillna(False)
    D["br2"] = np.where(D["kill"], 0.0, D["book_return"])
    D["wn"] = D["w"].str[1:].astype(int)
    res = {}
    for col in ["book_return", "br2"]:
        B = D.groupby(["wn", "day"])[col].mean().dropna().sort_index()
        v = (1 + B).cumprod()
        mdd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(B)) - 1
        res[col] = {"yearly": yr, "maxdd": mdd, "calmar": yr / -mdd,
                    "sharpe": B.mean() / B.std() * np.sqrt(365)}
    out["book_vs_clvfiltered"] = pd.DataFrame(res).T
    out["killed_days"] = int(D["kill"].sum())
    return out
