def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    recs = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True).copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["alloc"] = b["postRebalance_current_allocation"]
            b["next1"] = b["close"].shift(-1) / b["close"] - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["fc"] = b["forecast"]
            b["coin"] = coin; b["w"] = w; b["i"] = range(len(b))
            recs.append(b[["coin", "w", "i", "alloc", "next1", "ret20", "fc"]])
    B = pd.concat(recs).dropna(subset=["next1"])
    cost = 0.0019 / 2
    def book(pos):
        x = B[["coin", "w", "i"]].copy()
        x["pos"] = pos.values
        x["chg"] = x.groupby(["coin", "w"])["pos"].diff().abs().fillna(x["pos"].abs())
        x["g"] = x["pos"] * B["next1"].values - x["chg"] * cost
        d = x.groupby(["w", "i"])["g"].mean()
        inpos = (x["pos"] != 0).mean()
        sh = d.mean() / d.std() * np.sqrt(365)
        ordered = pd.concat([d.loc[w] for w in sorted(d.index.get_level_values(0).unique(), key=lambda s: int(s[1:]))])
        v = (1 + ordered).cumprod()
        dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(v)) - 1
        return pd.Series({"mean": d.mean(), "mean_in_pos": d.mean() / inpos, "share_in_pos": inpos,
                          "sharpe": sh, "yearly": yr, "maxdd": dd, "calmar": yr / -dd if dd < 0 else np.nan,
                          "turnover": x["chg"].mean()})
    out = {}
    a = B["alloc"]
    up = (B["ret20"] > 0)
    out["books"] = pd.DataFrame({
        "actual_net": book(a),
        "long_only": book(a.clip(lower=0)),
        "long_only_x3": book(3 * a.clip(lower=0)),
        "long_uptrend": book(a.clip(lower=0).where(up, 0)),
        "long_uptrend_x3": book(3 * a.clip(lower=0).where(up, 0)),
        "hold_1x": book(pd.Series(1.0, index=B.index)),
        "hold_uptrend_only": book(pd.Series(1.0, index=B.index).where(up, 0)),
    }).T
    # actual book drawdown composition: days in worst 5% book days, side held
    B["g"] = B["alloc"] * B["next1"]
    d = B.groupby(["w", "i"]).agg(g=("g", "mean"), coin=("next1", "mean"),
                                  long_share=("alloc", lambda s: (s > 0).mean()))
    thr = d["g"].quantile(0.05)
    out["worst_days"] = pd.DataFrame({"worst5pct": d[d.g <= thr].mean(), "all": d.mean()})
    return out
