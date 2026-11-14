def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            lc = np.log(b["close"].astype(float))
            b["r1"] = lc.diff()
            b["nr1"] = b["r1"].shift(-1)
            b["f12"] = lc.shift(-12) - lc
            b["f12x"] = b["f12"] - b["f12"].mean()
            b["p12"] = lc - lc.shift(12)
            b["vol24"] = b["r1"].rolling(24).std()
            b["vol24q_w"] = b["vol24"]
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            pv = b["postRebalance_total_value"].astype(float)
            b["bookr"] = np.log(pv).diff()
            b["gross_pnl"] = b["alloc"] * b["nr1"]
            b["turn"] = b["alloc"].diff().abs()
            b["z1"] = b["r1"] / b["r1"].rolling(168).std().shift(1)
            b["coin"] = coin; b["w"] = w
            b["hour"] = b["ts"].dt.hour; b["year"] = b["ts"].dt.year
            b["grid"] = (np.arange(len(b)) % 12 == 0)
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    out["gross_vs_book_per_coin"] = B.groupby("coin").agg(gross_sum=("gross_pnl", "sum"),
        book_sum=("bookr", "sum"), turnover=("turn", "sum"), n=("r1", "size"))
    # momentum: past 12h decile x vol tercile, non-overlapping
    G = B[B["grid"]].copy()
    G["p12q"] = G.groupby("coin")["p12"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["volt"] = G.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    def tt(s):
        return s.mean() / (s.std() / np.sqrt(s.count())) if s.count() > 2 else np.nan
    g = G.groupby(["volt", "p12q"])["f12x"]
    out["nonovl_fwd12x_volTerc_x_past12Quint"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.apply(tt)})
    g = G.groupby(["coin", "p12q"])["f12x"]
    out["nonovl_fwd12x_coin_x_past12Quint"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.apply(tt)})
    # top-forecast bins split by vol
    G["ext"] = G["forecast"] <= -10
    g = G.groupby(["volt", "ext"])["f12x"]
    out["nonovl_extreme_by_vol"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.apply(tt)})
    # after large 1h moves
    B["zb"] = pd.cut(B["z1"], [-99, -3, -2, 2, 3, 99])
    g = B.groupby("zb", observed=True)
    out["after_1h_zmove"] = pd.DataFrame({"n": g.size(), "next1_bp": g["nr1"].mean() * 1e4,
        "fwd12x": g["f12x"].mean(), "t12": g["f12x"].apply(lambda s: s.mean() / (s.std() / np.sqrt(max(s.count() / 12, 1))))})
    # hour 20/22 consistency across coin/window
    H = B[B["hour"].isin([1, 20, 22])]
    out["hour_1_20_22_by_coin_year_bp"] = (H.groupby(["hour", "coin", "year"])["r1"].mean() * 1e4).unstack("year")
    # book around largest losses/gains
    B["bkq"] = B.groupby("coin")["bookr"].transform(lambda s: pd.qcut(s.rank(method="first"), 100, labels=False))
    def around(mask):
        res = {}
        for k in [-12, -3, -1, 1, 3, 12]:
            sh = B.groupby(["coin", "w"])["r1"].shift(-k) if k > 0 else B.groupby(["coin", "w"])["r1"].shift(-k)
            res[k] = sh[mask].mean() * 1e4
        res["alloc"] = B.loc[mask, "alloc"].mean()
        res["vol"] = B.loc[mask, "vol24"].mean()
        res["n"] = int(mask.sum())
        return res
    out["around_book_worst1pct"] = pd.Series(around(B["bkq"] == 0))
    out["around_book_best1pct"] = pd.Series(around(B["bkq"] == 99))
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["efq"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entry_forecast"] = T.groupby("efq", observed=True).agg(n=("side", "size"),
        gross=("profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda s: s.mean() / 60),
        win=("profit_loss_percent", lambda s: (s > 0).mean()))
    out["trade_gross_skew"] = pd.Series({"median": T["profit_loss_percent"].median(),
        "p5": T["profit_loss_percent"].quantile(.05), "p95": T["profit_loss_percent"].quantile(.95),
        "share_loss_from_worst10pct": T.loc[T["profit_loss_percent"] <= T["profit_loss_percent"].quantile(.1), "profit_loss_percent"].sum() / T["profit_loss_percent"].sum()})
    return out
