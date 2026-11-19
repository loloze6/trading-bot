def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []; caseRows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            r1 = b["close"].shift(-1)/b["close"] - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            gross = a*r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            turn = (a - b["previous_allocation"].fillna(0)).abs()
            hr = pd.to_datetime(b["timestamp"]).dt.hour
            rows.append(pd.DataFrame({"coin": c, "gross": gross, "fee": fee, "turn": turn,
                                      "a": a, "hour": hr, "fc": b["forecast"], "r1": r1}))
            # 2-bar grid cases with forecast>0
            idx = np.arange(0, len(b)-2, 2)
            r2 = b["close"].values[idx+2]/b["close"].values[idx]-1
            fc = b["forecast"].values[idx]
            caseRows.append(pd.DataFrame({"coin": c, "fc": fc, "r2": r2}))
    df = pd.concat(rows); cs = pd.concat(caseRows)
    per_coin = df.groupby("coin").agg(gross_mean=("gross","mean"), fee_mean=("fee","mean"),
                                      turn_mean=("turn","mean"), share_long=("a", lambda x:(x>0).mean()))
    per_coin["net"] = per_coin.gross_mean - per_coin.fee_mean
    tot = pd.Series({"gross_per_bar": df.gross.mean(), "fee_per_bar": df.fee.mean(),
                     "turn_per_bar": df.turn.mean(), "mean_alloc_when_long": df.a[df.a>0].mean()})
    by_hour = df.groupby("hour").agg(gross=("gross","mean"), fee=("fee","mean"), turn=("turn","mean"),
                                     alloc=("a","mean"), r1=("r1","mean"))
    cs = cs.dropna()
    cm = cs.groupby("coin").r2.transform("mean")
    cs["ex"] = cs.r2 - cm
    act = cs[cs.fc > 0].copy()
    act["q"] = pd.qcut(act.fc.rank(method="first"), 5, labels=False)
    q = act.groupby("q").agg(n=("ex","size"), mean_ex=("ex","mean"), mean_r2=("r2","mean"), fc=("fc","mean"))
    d = pd.concat([days[c][w].assign(coin=c, win=w) for c in days for w in days[c]])
    dd = d.groupby("coin").agg(book=("book_return","mean"), coin_ret=("coin_return","mean"))
    return {"total": tot, "per_coin": per_coin, "by_hour": by_hour, "quintiles": q, "days": dd}
