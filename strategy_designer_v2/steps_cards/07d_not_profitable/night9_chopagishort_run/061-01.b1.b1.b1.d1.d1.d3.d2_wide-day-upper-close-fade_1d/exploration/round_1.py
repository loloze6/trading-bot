def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # ---- daily book ----
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna(subset=["book_return"])
    B["year"] = pd.to_datetime(B["day"]).dt.year
    v = (1 + B["book_return"]).cumprod(); dd_ = v / v.cummax() - 1
    B["dd"] = dd_.values
    out["book by window"] = B.groupby("w").agg(mean=("book_return", "mean"), std=("book_return", "std"), sum=("book_return", "sum"),
                                              coin=("coin_return", "mean"), n=("book_return", "size")).assign(
        sh=lambda x: x["mean"] / x["std"] * np.sqrt(365)).sort_index(key=lambda s: s.str[1:].astype(int))
    out["max dd"] = float(dd_.min())
    # worst 10-day stretches
    B["roll10"] = B.groupby("w")["book_return"].transform(lambda s: s.rolling(10).sum())
    out["worst10 by window"] = B.groupby("w")["roll10"].min().sort_values().head(6)
    # ---- trades ----
    T = []
    for c in trades:
        for w, t in trades[c].items():
            t = t.copy(); t["coin"] = c; t["w"] = w; T.append(t)
    T = pd.concat(T)
    T["dur"] = T["duration_minutes"] / 1440
    out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(), "mean_gross": T["profit_loss_percent"].mean(),
                               "win": (T["net_profit_loss_percent"] > 0).mean(), "dur_mean": T["dur"].mean(), "dur_med": T["dur"].median(),
                               "comm_mean": T["total_commission"].mean()})
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=["low", "mid", "high"], duplicates="drop")
    out["trades by |forecast| tercile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count", "sum"])
    # ---- case-level from bars ----
    cases = []
    for c in bars:
        drifts = []
        per = {}
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].values
            r5 = np.full(len(b), np.nan); r5[:-5] = cl[5:] / cl[:-5] - 1
            for h in [1, 2, 3, 10]:
                x = np.full(len(b), np.nan); x[:-h] = cl[h:] / cl[:-h] - 1; b[f"f{h}"] = x
            b["f5"] = r5
            drifts += list(r5[::5][~np.isnan(r5[::5])])
            b["loc"] = (b["close"] - b["low"]) / (b["high"] - b["low"])
            b["ret5"] = b["close"].pct_change(5)
            b["ret20"] = b["close"].pct_change(20)
            rng = (b["high"] - b["low"]) / b["close"]
            b["rm"] = (b["high"] - b["low"]) / (b["high"] - b["low"]).rolling(20).mean()
            b["ret1"] = b["close"].pct_change()
            b["inprof"] = b["regime"] != "chop"
            b["alloc"] = b["postRebalance_current_allocation"]
            b["g"] = np.arange(len(b)) % 5 == 0
            b["coin"] = c; b["w"] = w
            per[w] = b
        drift = np.mean(drifts); sd = np.std(drifts)
        for w, b in per.items():
            b["drift"] = drift; b["usd"] = sd
            cases.append(b)
    C = pd.concat(cases)
    C["day"] = C["timestamp"].astype(str).str[:10]
    G = C[C["g"] & C["inprof"]].dropna(subset=["f5", "loc", "ret5"]).copy()
    G["um"] = -(G["f5"] - G["drift"])  # short direction
    G["sit"] = (G["loc"] >= 0.5) & (G["ret5"] < 0)
    def tt(s, dcol):
        x = s.groupby(dcol).sum(); n = s.groupby(dcol).size()
        m = s.mean(); dev = (s - m).groupby(dcol).sum()
        Gn = len(dev); se = np.sqrt((dev ** 2).sum() * Gn / (Gn - 1)) / len(s)
        return m, m / se, len(s), Gn
    def grp(df, key):
        r = {}
        for k, sub in df.groupby(key, observed=True):
            if len(sub) > 5:
                m, t, n, g = tt(sub["um"], sub["day"]); r[str(k)] = {"um": m, "t": t, "n": n, "days": g}
        return pd.DataFrame(r).T
    G["grp"] = np.where(G["sit"], "sit", np.where(G["loc"] >= 0.5, "up_ret5pos", "lowclose"))
    out["profile cells by group (short dir 5d)"] = grp(G, "grp")
    S = G[G["sit"]].copy()
    S["rmq"] = pd.qcut(S["rm"], 3, labels=["n", "m", "w"])
    out["sit by range mult tercile"] = grp(S, "rmq")
    S["r5q"] = pd.qcut(S["ret5"], 3, labels=["deep", "mid", "shallow"])
    out["sit by ret5 tercile"] = grp(S, "r5q")
    S["locq"] = pd.cut(S["loc"], [0.5, 0.7, 0.85, 1.01], right=False)
    out["sit by loc"] = grp(S, "locq")
    S["r20s"] = np.where(S["ret20"] > 0, "r20pos", "r20neg")
    out["sit by ret20 sign"] = grp(S, "r20s")
    G["r20s"] = np.where(G["ret20"] > 0, "r20pos", "r20neg")
    out["nonsit by ret20 sign"] = grp(G[~G["sit"]], "r20s")
    S["year"] = pd.to_datetime(S["day"]).dt.year
    out["sit by year"] = grp(S, "year")
    # horizons
    hz = {}
    for h in [1, 2, 3, 5, 10]:
        x = -(S[f"f{h}"]) ; hz[h] = {"mean_short": x.mean(), "t": x.mean() / x.std() * np.sqrt(x.notna().sum()), "n": x.notna().sum()}
    out["sit horizons (raw short)"] = pd.DataFrame(hz).T
    # allocation size when in position
    P = C[C["alloc"].abs() > 1e-6]
    out["alloc"] = pd.Series({"mean_abs_alloc": P["alloc"].abs().mean(), "share_pos_bars": len(P) / len(C),
                              "mean_coin_ret_next_in_pos": (P["alloc"] * P.groupby(["coin", "w"])["close"].shift(-1).div(P["close"]).sub(1)).mean()})
    return out
