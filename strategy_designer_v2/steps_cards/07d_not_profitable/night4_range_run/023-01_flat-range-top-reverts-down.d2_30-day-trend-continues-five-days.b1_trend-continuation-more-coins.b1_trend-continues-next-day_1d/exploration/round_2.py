def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            nxt = c.shift(-1) / c - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            pa = b["previous_allocation"].fillna(0)
            vol = c.pct_change().rolling(30).std()
            r30 = c / c.shift(30) - 1
            vol60med = vol.rolling(60, min_periods=20).median()
            df = pd.DataFrame({"coin": coin, "win": w, "t": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "alloc": a, "turn": (a - pa).abs(), "nxt": nxt, "vol": vol,
                               "volrel": vol / vol60med, "r30": r30})
            df["gain"] = df["alloc"] * df["nxt"]
            df["net"] = df["gain"] - df["turn"] * 0.0011
            rows.append(df)
    B = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    B["side"] = np.sign(B["alloc"])
    B["volq"] = pd.qcut(B["vol"], 4, labels=False, duplicates="drop")
    def book(sub_mask):
        x = B.copy()
        x.loc[~sub_mask, "net"] = 0.0
        d = x.groupby(["win", "t"])["net"].mean().reset_index()
        d["wn"] = d["win"].str[1:].astype(int)
        d = d.sort_values(["wn", "t"])
        r = d["net"]
        eq = (1 + r).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yrs = len(r) / 365
        cagr = eq.iloc[-1] ** (1 / yrs) - 1
        return pd.Series({"mean": r.mean(), "sharpe": r.mean() / r.std() * np.sqrt(365), "maxdd": dd, "calmar": cagr / -dd})
    allm = pd.Series(True, index=B.index)
    out["pseudo_books"] = pd.DataFrame({
        "all": book(allm),
        "longs_only": book(B["side"] > 0),
        "shorts_only": book(B["side"] < 0),
        "vol_q0-2": book(B["volq"] <= 2),
        "longs_vol_q0-2": book((B["side"] > 0) & (B["volq"] <= 2)),
        "volrel<1": book(B["volrel"] < 1),
    }).T
    act = B[B["side"] != 0].copy()
    act["dirret"] = act["side"] * act["nxt"]
    g = act.groupby(["side", "volq"])["dirret"]
    out["side_x_volq"] = pd.DataFrame({"n": g.size(), "dirret": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    act["vrq"] = pd.qcut(act["volrel"], 4, labels=False, duplicates="drop")
    g = act.groupby(["side", "vrq"])["dirret"]
    out["side_x_volrel"] = pd.DataFrame({"n": g.size(), "dirret": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    # worst days of the book
    d = B.groupby(["win", "t"]).agg(net=("net", "mean")).reset_index()
    worst = d.nsmallest(int(len(d) * 0.05), "net")[["win", "t"]]
    W = B.merge(worst, on=["win", "t"])
    WA = W[W["side"] != 0]
    out["worst5pct_days"] = pd.Series({"days": len(worst), "mean_book": d.nsmallest(len(worst), "net")["net"].mean(),
        "share_short_of_active": (WA["side"] < 0).mean(), "share_short_all_active": (act["side"] < 0).mean(),
        "loss_from_shorts": WA.loc[WA["side"] < 0, "net"].sum(), "loss_from_longs": WA.loc[WA["side"] > 0, "net"].sum(),
        "vol_worst_active": WA["vol"].mean(), "vol_all_active": act["vol"].mean(),
        "volrel_worst_active": WA["volrel"].mean(), "volrel_all_active": act["volrel"].mean()})
    return out
