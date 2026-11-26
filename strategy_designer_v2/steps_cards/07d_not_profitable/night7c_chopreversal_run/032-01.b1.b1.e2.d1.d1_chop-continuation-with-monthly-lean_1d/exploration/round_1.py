def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            ret30 = c / c.shift(30) - 1
            ret7 = c / c.shift(7) - 1
            vol90 = r1.rolling(90, min_periods=60).std()
            pos = b["postRebalance_current_allocation"]
            v = b["postRebalance_total_value"]
            br = v / v.shift(1) - 1  # bar return of book
            gain_next = pos * (c.shift(-1) / c - 1)
            fwd7 = c.shift(-7) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "pos": pos,
                               "pos_prev": pos.shift(1), "br": br, "gain": gain_next,
                               "er": er, "ret30": ret30, "ret7": ret7, "vol30": vol30,
                               "volratio": vol30 / vol90, "fc": b["forecast"], "fwd7": fwd7,
                               "regime": b["regime"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["wn"] = A["w"].str[1:].astype(int)
    # portfolio daily: mean over coins per (w,i)
    P = A.groupby(["wn", "i"])["br"].mean().dropna().reset_index().sort_values(["wn", "i"])
    eq = (1 + P["br"]).cumprod()
    dd = eq / eq.cummax() - 1
    P["dd"] = dd.values
    out["max_dd"] = float(dd.min())
    out["yearly"] = float(eq.iloc[-1] ** (365 / len(P)) - 1)
    out["dd_by_window_min"] = P.groupby("wn")["dd"].min()
    # window returns
    out["window_ret"] = P.groupby("wn")["br"].apply(lambda x: (1 + x).prod() - 1)
    # attribution: gain by side, by vol bucket
    H = A[A["pos"].abs() > 1e-6].dropna(subset=["gain"]).copy()
    H["side"] = np.sign(H["pos"])
    out["gain_by_side"] = H.groupby("side")["gain"].agg(["mean", "count", "sum"])
    H["volq"] = pd.qcut(H["vol30"], 4, labels=False)
    out["gain_by_vol30q"] = H.groupby(["volq", "side"])["gain"].agg(["mean", "count"])
    H["vrq"] = pd.qcut(H["volratio"], 4, labels=False)
    out["gain_by_volratioq"] = H.groupby(["vrq", "side"])["gain"].agg(["mean", "count"])
    H["erq"] = pd.qcut(H["er"], 4, labels=False)
    out["gain_by_erq"] = H.groupby("erq")["gain"].agg(["mean", "count"])
    out["abs_pos_mean"] = H["pos"].abs().describe()
    out["regime_share_when_held"] = H["regime"].value_counts(normalize=True)
    out["gain_by_window_side"] = H.groupby(["wn", "side"])["gain"].sum().unstack()
    return out
