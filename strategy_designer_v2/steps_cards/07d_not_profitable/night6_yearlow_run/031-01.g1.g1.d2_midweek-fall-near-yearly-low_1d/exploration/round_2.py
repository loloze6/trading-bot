def explore(data):
    import pandas as pd, numpy as np
    out = {}
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            lr = np.log(b["close"]).diff()
            b["vol20"] = lr.rolling(20).std()
            b["coin"] = c; b["w"] = w
            cs.append(b)
    A = pd.concat(cs)
    A["ts"] = pd.to_datetime(A["timestamp"])
    A["wd"] = A["ts"].dt.weekday
    A["wn"] = A["w"].str[1:].astype(int)
    mu = A.groupby("coin")["ret1"].mean()
    A["ex"] = A["ret1"] - A["coin"].map(mu)
    # vol terciles per coin on all bars (same cut as round 1 approx) and also realised vol from sizing
    A["volq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    A["rvq"] = A.groupby("coin")["sizing_realised_vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    Fr = A[(A["wd"] == 4)].dropna(subset=["ret1"]).copy()
    Fr["al"] = Fr["postRebalance_current_allocation"]
    Fr["side"] = np.where(Fr["al"] > 1e-6, "long", np.where(Fr["al"] < -1e-6, "short", "flat"))
    # condition alone: Saturday excess return on Fridays by vol tercile, regime, side
    def s(g):
        return pd.Series({"n": len(g), "mean_ex": g.ex.mean(), "t": g.ex.mean() / g.ex.std() * np.sqrt(len(g))})
    out["sat_ex_by_volq_regime_side"] = Fr.groupby(["volq", "regime", "side"]).apply(s)
    # short side with realised-vol terciles (sizing vol, 60d) 
    Sh = Fr[Fr.side == "short"].copy(); Sh["pnl"] = Sh.al * Sh.ret1
    out["short_by_rvq"] = Sh.groupby("rvq")["pnl"].agg(["count", "mean", "sum"])
    Lo = Fr[Fr.side == "long"].copy(); Lo["pnl"] = Lo.al * Lo.ret1
    out["long_by_rvq"] = Lo.groupby("rvq")["pnl"].agg(["count", "mean", "sum"])
    # grading of short in low vol
    Sh["fq"] = pd.qcut(Sh["forecast"], 3, labels=False)
    out["short_volq_fq"] = Sh.groupby(["volq", "fq"])["pnl"].agg(["count", "mean"])
    # pnl by window groups and side (drawdown windows 5-10)
    Fr["pnl"] = Fr.al * Fr.ret1
    Fr["wgrp"] = np.where(Fr.wn.between(4, 10), "w4-10", "other")
    out["pnl_wgrp_side_volq"] = Fr[Fr.side != "flat"].groupby(["wgrp", "side", "volq"])["pnl"].agg(["count", "mean", "sum"])
    # rebuild book: remove short positions; and remove only low-vol shorts
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            x = d[["day", "book_return"]].copy(); x["coin"] = c; x["w"] = w
            rows.append(x)
    D = pd.concat(rows)
    D["day"] = pd.to_datetime(D["day"])
    D["wn"] = D["w"].str[1:].astype(int)
    Sh2 = Fr[Fr.side == "short"][["coin", "w", "ts", "volq"]].copy()
    Sh2["fri"] = Sh2.ts.dt.normalize(); 
    def book(mask_df):
        keys = set()
        for _, r in mask_df.iterrows():
            keys.add((r.coin, r.w, r.fri)); keys.add((r.coin, r.w, r.fri + pd.Timedelta(days=1)))
        DD = D.copy()
        m = [(a, b, c) in keys for a, b, c in zip(DD.coin, DD.w, DD.day)]
        DD.loc[m, "book_return"] = 0.0
        Bk = DD.groupby(["wn", "day"])["book_return"].mean().dropna().sort_index()
        eq = (1 + Bk).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yrs = len(Bk) / 365.0
        yr = eq.iloc[-1] ** (1 / yrs) - 1
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": Bk.mean() / Bk.std() * np.sqrt(365)})
    out["book_variants"] = pd.DataFrame({
        "as_is": book(Sh2.iloc[0:0]),
        "no_short": book(Sh2),
        "no_lowvol_short": book(Sh2[Sh2.volq == 0]),
    })
    return out
