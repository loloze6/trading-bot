def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]; days = data["days"]
    wnum = lambda s: int(s[1:])
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            r = b["close"].shift(-1) / b["close"] - 1
            r5 = b["close"].shift(-5) / b["close"] - 1
            df = pd.DataFrame({"coin": c, "wn": wnum(w), "r": r.values, "r5": r5.values,
                               "x": b["postRebalance_current_allocation"].values, "f": b["forecast"].values,
                               "pos": np.arange(len(b)),
                               "ret28": (b["close"] / b["close"].shift(28) - 1).values,
                               "ret1": (b["close"] / b["close"].shift(1) - 1).values})
            for k in ["mom28", "rev1", "high90", "vol30"]:
                col = f"debug_info.components.{k}.post_pipeline_value"
                df[k] = b[col].values if col in b else np.nan
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            rows.append(df)
    X = pd.concat(rows, ignore_index=True)
    X["gain"] = X.x * X.r
    G = X[X.pos % 5 == 0].dropna(subset=["r5"]).copy()
    G["mu5"] = G.groupby("coin").r5.transform("mean")
    G["ex5"] = G.r5 - G.mu5
    def tt(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "t": s.mean() / s.std() * np.sqrt(len(s)), "n": len(s)})
    sc = {}
    sc["all4"] = tt(((G.mom28 + G.rev1 + G.high90 + G.vol30) / 4) * G.ex5)
    sc["mom_high"] = tt(((G.mom28 + G.high90) / 2) * G.ex5)
    sc["mom_high_minus_rev"] = tt(((G.mom28 + G.high90 - G.rev1) / 3) * G.ex5)
    sc["mom_only"] = tt(G.mom28 * G.ex5)
    sc["mom_long_side_only"] = tt(G.mom28.clip(lower=0) * G.ex5)
    sc["mom_short_side_only"] = tt(G.mom28.clip(upper=0) * G.ex5)
    out["scores_t"] = pd.DataFrame(sc).T.round(4)
    # graded: ex5 by mom28 quintile
    G["mq"] = pd.qcut(G.mom28, 5, labels=False)
    out["ex5_by_mom28_quintile"] = G.groupby("mq").agg(n=("ex5", "size"), ex5=("ex5", "mean"), r5=("r5", "mean"),
                                                       ret28=("ret28", "mean")).round(4)
    G["r1q"] = pd.qcut(G.ret1, 5, labels=False)
    out["ex5_by_ret1_quintile"] = G.groupby("r1q").agg(n=("ex5", "size"), ex5=("ex5", "mean")).round(4)
    # side x mom state gain
    X["mom_t"] = X.groupby("coin").ret28.transform(lambda s: pd.qcut(s, 3, labels=["dn", "mid", "up"]))
    X["side"] = np.sign(X.x)
    out["gain_side_mom"] = X.groupby(["side", "mom_t"], observed=True).agg(
        n=("gain", "size"), gain_bps=("gain", lambda s: s.mean() * 1e4), r_bps=("r", lambda s: s.mean() * 1e4)).round(2)
    # deepest fall stretch
    drows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["wn"] = wnum(w); drows.append(dd)
    D = pd.concat(drows)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    chain = (1 + B.book_return).cumprod()
    peak = chain.cummax()
    dd_ = chain / peak - 1
    tr = dd_.idxmin()
    pk = chain.loc[:tr].idxmax()
    seg = B.loc[pk:tr]
    out["deepest_fall"] = pd.Series({"fall": dd_.min(), "n_days": len(seg), "win_from": pk[0], "win_to": tr[0],
                                     "book_sum": seg.book_return.sum(), "coin_sum": seg.coin_return.sum()})
    Xd = X.copy(); Xd["key"] = list(zip(Xd.wn, Xd.day))
    segkeys = set(seg.index)
    S = Xd[Xd.key.isin(segkeys)]
    out["fall_holdings"] = S.groupby("side").agg(n=("gain", "size"), gain_bps=("gain", lambda s: s.mean() * 1e4),
                                                 r_bps=("r", lambda s: s.mean() * 1e4), absx=("x", lambda s: s.abs().mean()),
                                                 ret28=("ret28", "mean")).round(3)
    out["fall_by_mom"] = S.groupby(["side", "mom_t"], observed=True).agg(
        n=("gain", "size"), gain_bps=("gain", lambda s: s.mean() * 1e4)).round(2)
    return out
