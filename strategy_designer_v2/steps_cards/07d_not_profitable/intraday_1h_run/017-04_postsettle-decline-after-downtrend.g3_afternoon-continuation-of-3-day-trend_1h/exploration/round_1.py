def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []; hour_rows = []; slot = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            b["hour"] = ts.dt.hour
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            b["gross"] = a * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["turn"] = (a - b["previous_allocation"].fillna(0)).abs()
            b["c"] = c; b["w"] = w
            hour_rows.append(b[["c", "w", "hour", "gross", "fee", "turn", "forecast"]].assign(absalloc=a.abs()))
            # slot cases: bar stamped 15:00
            s = b[b["hour"] == 15].copy()
            idx = s.index
            pos = b.index.get_indexer(idx)
            ok = pos + 2 < len(b)
            s = s[ok]; pos = pos[ok]
            s["r2"] = b["close"].values[pos + 2] / b["close"].values[pos] - 1
            s["alloc"] = a.values[pos]
            s["fee2"] = b["fee"].values[pos] + b["fee"].values[pos + 2]
            s["g2"] = s["alloc"] * s["r2"]
            slot.append(s[["c", "w", "r2", "alloc", "fee2", "g2", "forecast"]])
    H = pd.concat(hour_rows); S = pd.concat(slot)
    byhour = H.groupby("hour").agg(gross=("gross", "mean"), fee=("fee", "mean"), turn=("turn", "mean"), absalloc=("absalloc", "mean"))
    byhour = byhour[(byhour.absalloc > 1e-6) | (byhour.fee > 1e-7)]
    S["net"] = S["g2"] - S["fee2"]
    S["sgnf"] = np.sign(S["forecast"])
    percoin = S.groupby("c").agg(n=("g2", "size"), gross=("g2", "mean"), fee=("fee2", "mean"), net=("net", "mean"), absalloc=("alloc", lambda x: x.abs().mean()))
    S["fq"] = pd.qcut(S["forecast"].abs().rank(method="first"), 3, labels=["low", "mid", "high"])
    byq = S.groupby("fq").agg(gross=("g2", "mean"), fee=("fee2", "mean"), net=("net", "mean"), absalloc=("alloc", lambda x: x.abs().mean()), signed_r2=("r2", lambda x: 0))
    byq["signed_r2"] = S.groupby("fq").apply(lambda d: (np.sign(d["forecast"]) * d["r2"]).mean())
    bys = S.groupby("sgnf").agg(n=("g2", "size"), gross=("g2", "mean"), fee=("fee2", "mean"), net=("net", "mean"), mean_r2=("r2", "mean"))
    tot = pd.Series({"gross_mean_per_slot": S.g2.mean(), "t_gross": stats.ttest_1samp(S.g2.dropna(), 0).statistic,
                     "fee_mean_per_slot": S.fee2.mean(), "net_mean": S.net.mean(), "n": len(S),
                     "fee_rate_per_unit_turn": H.fee.sum() / H.turn.sum()})
    D = pd.concat([d.assign(c=c) for c in days for w, d in days[c].items()])
    dd = pd.Series({"book_daily_mean": D.book_return.mean(), "coin_daily_mean": D.coin_return.mean()})
    return {"totals": tot, "byhour": byhour, "percoin": percoin, "by_forecast_third": byq, "by_sign": bys, "daily": dd}
