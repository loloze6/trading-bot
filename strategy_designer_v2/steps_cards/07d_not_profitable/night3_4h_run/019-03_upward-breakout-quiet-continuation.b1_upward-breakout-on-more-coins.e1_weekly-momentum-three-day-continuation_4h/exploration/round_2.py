def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # rebuild portfolio daily series to locate falls
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = c; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    P = D.groupby(["wn", "day"]).agg(book=("book_return", "mean")).dropna().reset_index().sort_values(["wn", "day"]).reset_index(drop=True)
    eq = (1 + P["book"]).cumprod(); dd = eq / eq.cummax() - 1
    eps = []; inn = False
    for i in range(len(P)):
        if dd[i] < 0 and not inn: inn = True; s = max(i - 1, 0); m = i
        if inn:
            if dd[i] < dd[m]: m = i
            if dd[i] == 0: eps.append((dd[m], s, m)); inn = False
    if inn: eps.append((dd[m], s, m))
    eps = sorted(eps)[:4]
    fall_keys = set()
    for k, e in enumerate(eps):
        for i in range(e[1] + 1, e[2] + 1):
            fall_keys.add((P.loc[i, "wn"], P.loc[i, "day"], k))
    fk = pd.DataFrame(list(fall_keys), columns=["wn", "day", "ep"])
    # bar level
    B = []; G = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            x = pd.DataFrame({"close": b["close"].values, "pos": b["postRebalance_current_allocation"].values, "fc": b["forecast"].values})
            ts = pd.to_datetime(b["timestamp"].values)
            x["day"] = ts.floor("D")
            x["ret"] = x["close"].shift(-1) / x["close"] - 1
            r1 = x["close"].pct_change()
            vol = r1.rolling(180).std()
            x["ret30s"] = (x["close"] / x["close"].shift(180) - 1) / (vol * np.sqrt(180))
            x["ret90s"] = (x["close"] / x["close"].shift(540) - 1) / (vol * np.sqrt(540))
            x["f18"] = x["close"].shift(-18) / x["close"] - 1
            x["coin"] = c; x["wn"] = int(w[1:])
            B.append(x)
            g = x.iloc[::18].copy(); G.append(g)
    B = pd.concat(B).dropna(subset=["ret", "pos"])
    B["gross"] = B["pos"] * B["ret"]
    B["side"] = np.sign(B["pos"])
    # match day type to P's day type
    pday = P["day"].iloc[0]
    try:
        B["day"] = B["day"].dt.tz_localize(None) if B["day"].dt.tz is not None else B["day"]
        fk["day"] = pd.to_datetime(fk["day"]).dt.tz_localize(None) if pd.to_datetime(fk["day"]).dt.tz is not None else pd.to_datetime(fk["day"])
    except Exception:
        pass
    M = B.merge(fk, on=["wn", "day"], how="inner")
    out["falls_by_side_sum_gross_per_coin"] = M.groupby(["ep", "side"]).agg(bars=("gross", "size"), sum_gross_per_coinday=("gross", lambda s: s.sum()), mean_bps=("gross", lambda s: s.mean() * 1e4))
    out["falls_bars_matched"] = len(M)
    # grid level: unusual move by forecast sign x 30d trend
    G = pd.concat(G).dropna(subset=["f18", "fc"])
    G = G[G["fc"] != 0]
    drift = G.groupby("coin")["f18"].mean()
    G["unus"] = G["f18"] - G["coin"].map(drift)
    G["aligned"] = np.sign(G["fc"]) * G["unus"]
    G["fs"] = np.sign(G["fc"])
    G["t30"] = np.sign(G["ret30s"])
    def st(gb):
        return pd.DataFrame({"n": gb.size(), "aligned_bps": gb["aligned"].mean() * 1e4,
                             "t": gb["aligned"].mean() / (gb["aligned"].std() / np.sqrt(gb.size())),
                             "total_bps": gb.apply(lambda d: (np.sign(d["fc"]) * d["f18"]).mean() * 1e4)})
    out["grid_by_fsign_t30"] = st(G.groupby(["fs", "t30"]))
    # graded: aligned move by quintile of 30d scaled return in forecast's direction
    G["agree30"] = G["fs"] * G["ret30s"]
    G["aq"] = pd.qcut(G["agree30"], 5, labels=False, duplicates="drop")
    out["grid_by_30d_agreement_q"] = st(G.groupby("aq"))
    G["agree90"] = G["fs"] * G["ret90s"]
    G["a9"] = pd.qcut(G["agree90"], 5, labels=False, duplicates="drop")
    out["grid_by_90d_agreement_q"] = st(G.dropna(subset=["agree90"]).groupby("a9"))
    # long-only graded by fc strength within 30d up
    G["fq"] = pd.qcut(G["fc"], 5, labels=False, duplicates="drop")
    out["grid_fq_by_t30_total_signed_bps"] = G.groupby(["t30", "fq"]).apply(lambda d: pd.Series({"n": len(d), "f18_bps": d["f18"].mean() * 1e4})).unstack()
    return out
