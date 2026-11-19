def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    out = {}
    # trades: gross vs net per trade
    tr = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    tr["dur_h"] = tr.duration_minutes / 60
    out["trades"] = pd.Series({"n": len(tr), "mean_gross_pct": tr.profit_loss_percent.mean(),
                               "mean_net_pct": tr.net_profit_loss_percent.mean(),
                               "median_dur_h": tr.dur_h.median(), "share_gross_pos": (tr.profit_loss_percent > 0).mean(),
                               "share_net_pos": (tr.net_profit_loss_percent > 0).mean()})
    tr["fq"] = pd.qcut(tr.entry_forecast.rank(method="first"), 5, labels=False)
    out["trades_by_entry_fc_q"] = tr.groupby("fq").agg(n=("profit_loss_percent", "size"),
        fc=("entry_forecast", "mean"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    # slow horizon rebound by fall depth, all hours
    for h in [24, 48]:
        recs = []
        for c in bars:
            for w, b in bars[c].items():
                s = b["close"].astype(float).reset_index(drop=True)
                ch = s.pct_change(72)
                z = (ch - ch.rolling(72, min_periods=20).mean()) / ch.rolling(72, min_periods=20).std()
                idx = np.arange(0, len(s) - h, h)
                r = s.values[idx + h] / s.values[idx] - 1
                recs.append(pd.DataFrame({"coin": c, "win": w, "fall": -z.values[idx], "r": r}))
        df = pd.concat(recs).dropna()
        df["ex"] = df.r - df.groupby("coin").r.transform("mean")
        pos = df[df.fall > 0].copy()
        pos["q"] = pd.qcut(pos.fall.rank(method="first"), 5, labels=False)
        g = pos.groupby("q").ex.agg(["size", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
        g["fall"] = pos.groupby("q").fall.mean()
        out[f"h{h}_ex_by_fall_q"] = g
        v = (pos.fall.clip(upper=np.sqrt(2) * 10 ** 0.5) ** 2 / 10) * pos.ex
        out[f"h{h}_weighted_t"] = pd.Series({"n": len(v), "t": v.mean() / (v.std() / np.sqrt(len(v))),
                                             "corr_fall_ex": stats.spearmanr(pos.fall, pos.ex)[0]})
    return out
