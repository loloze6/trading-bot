def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 18, 42, 84]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            rng = (hi - lo).rolling(180, min_periods=90).mean()
            hh6 = hi.rolling(6, min_periods=6).max()
            drop = (hh6 - c) / rng
            rng6 = (hi.rolling(6).max() - lo.rolling(6).min()) / rng
            prior = c.shift(6) / c.shift(186) - 1
            ret6 = c / c.shift(6) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for h in H:
                idx = np.arange(0, n - h, h)
                if len(idx) == 0: continue
                fwd = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": h, "fwd": fwd,
                    "drop": drop.values[idx], "rng6": rng6.values[idx], "prior": prior.values[idx],
                    "ret6": ret6.values[idx], "year": yr.values[idx]}))
    a = pd.concat(rows, ignore_index=True)
    a["drift"] = a.groupby(["coin", "h"])["fwd"].transform("mean")
    a["ex"] = a["fwd"] - a["drift"]
    a = a.dropna(subset=["drop", "prior", "ex"])
    a["dq"] = a.groupby("h")["drop"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    a["side"] = np.where(a["prior"] < 0, "neg", "pos")
    def summ(g):
        x = g["ex"]; n = len(x)
        return pd.Series({"n": n, "mean_ex": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "mean_fwd": g["fwd"].mean()})
    out = {}
    out["by_h_side_dropq"] = a.groupby(["h", "side", "dq"]).apply(summ).round(4)
    b = a[a.h == 84]
    pan = b[b.dq == 4]
    out["h84_topdrop_side_year"] = pan.groupby(["side", "year"]).apply(summ).round(4)
    b2 = b.copy()
    b2["pq"] = pd.qcut(b2["prior"].rank(method="first"), 5, labels=False)
    out["h84_priorq_all"] = b2.groupby("pq").apply(summ).round(4)
    out["h84_priorq_topdrop"] = b2[b2.dq == 4].groupby("pq").apply(summ).round(4)
    out["h84_neg_topdrop_coin"] = pan[pan.side == "neg"].groupby("coin").apply(summ).round(4)
    return out
