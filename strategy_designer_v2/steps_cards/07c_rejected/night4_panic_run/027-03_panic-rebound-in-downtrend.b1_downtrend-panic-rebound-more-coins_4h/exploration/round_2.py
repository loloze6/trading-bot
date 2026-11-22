def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [6, 18, 42, 84]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            rng = (hi - lo).rolling(180, min_periods=90).mean()
            drop = (hi.rolling(6, min_periods=6).max() - c) / rng
            prior = c.shift(6) / c.shift(186) - 1
            f = df["forecast"].astype(float).fillna(0)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for h in H:
                idx = np.arange(0, n - h, h)
                if len(idx) == 0: continue
                fwd = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": h, "fwd": fwd,
                    "drop": drop.values[idx], "prior": prior.values[idx], "fc": f.values[idx],
                    "year": yr.values[idx]}))
    a = pd.concat(rows, ignore_index=True)
    a["drift"] = a.groupby(["coin", "h"])["fwd"].transform("mean")
    a["ex"] = a["fwd"] - a["drift"]
    a = a.dropna(subset=["drop", "prior", "ex"])
    a["side"] = np.where(a["prior"] < 0, "neg", "pos")
    a["dd"] = a.groupby(["h", "side"])["drop"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    def summ(g):
        x = g["ex"]; n = len(x)
        return pd.Series({"n": n, "mean_ex": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "mean_drop": g["drop"].mean()})
    out = {}
    out["h18_42_side_dropdecile"] = a[a.h.isin([18, 42])].groupby(["h", "side", "dd"]).apply(summ).round(4)
    pos18 = a[(a.h == 18) & (a.side == "pos") & (a.dd >= 8)]
    out["pos_h18_top2dec_year"] = pos18.groupby("year").apply(summ).round(4)
    out["pos_h18_top2dec_coin_share_pos"] = pd.Series({"coins": pos18.coin.nunique(),
        "share_coins_mean_pos": (pos18.groupby("coin")["ex"].mean() > 0).mean()})
    act = a[(a.fc > 0)]
    act["fq"] = act.groupby("h")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["active_fc_tercile"] = act.groupby(["h", "fq"]).apply(summ).round(4)
    neg = a[a.side == "neg"].copy()
    neg["pq"] = neg.groupby("h")["prior"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["neg_dd5to8_by_priorTercile"] = neg[neg.dd.between(3, 7)].groupby(["h", "pq"]).apply(summ).round(4)
    return out
