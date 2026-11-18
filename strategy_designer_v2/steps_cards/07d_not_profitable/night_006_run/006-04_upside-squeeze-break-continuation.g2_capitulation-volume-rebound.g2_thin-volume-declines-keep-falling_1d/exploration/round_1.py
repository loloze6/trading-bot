def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    daily = []
    for coin in data["bars"]:
        # coin mean daily return over all windows
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in data["days"][coin]]).dropna()
        mu = cr.mean()
        for w, b in data["bars"][coin].items():
            b = b.copy()
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1) / b["close"] - 1
            g = pos * r1
            ret5 = b["close"] / b["close"].shift(5) - 1
            ret30 = b["close"] / b["close"].shift(30) - 1
            fwd3 = b["close"].shift(-3) / b["close"] - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "r1": r1, "g": g,
                               "fc": b["forecast"], "ret5": ret5, "ret30": ret30,
                               "fee": (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"],
                               "mu": mu, "fwd3": fwd3, "i": np.arange(len(b))})
            rows.append(df)
            d = data["days"][coin][w]
            daily.append(pd.DataFrame({"coin": coin, "w": w, "br": d["book_return"], "cr": d["coin_return"]}))
    A = pd.concat(rows).dropna(subset=["r1"])
    D = pd.concat(daily).dropna()
    out["book_vs_hold"] = pd.Series({"book_mean": D.br.mean(), "hold_mean": D.cr.mean(),
                                     "book_sh": D.br.mean()/D.br.std()*np.sqrt(365), "hold_sh": D.cr.mean()/D.cr.std()*np.sqrt(365),
                                     "mean_pos": A.pos.mean(), "share_short": (A.pos < 0).mean(), "share_long": (A.pos > 0).mean(),
                                     "market_part": (A.pos*A.mu).mean(), "gross_gain": A.g.mean(), "fee_mean": A.fee.mean()})
    A["side"] = np.sign(A.pos)
    out["by_side"] = A.groupby("side").agg(n=("g", "size"), gain=("g", "mean"), r1=("r1", "mean"), pos=("pos", "mean"), fee=("fee", "mean"))
    A["fcq"] = pd.qcut(A.fc.where(A.fc != 0), 6, duplicates="drop")
    out["by_fc_bin"] = A.groupby("fcq", observed=True).agg(n=("g", "size"), gain=("g", "mean"), r1_ex=("r1", lambda x: (x - A.loc[x.index, "mu"]).mean()), pos=("pos", "mean"))
    A["trend30"] = np.sign(A.ret30)
    out["by_trend30_side"] = A.groupby(["trend30", "side"]).agg(n=("g", "size"), gain=("g", "mean"), r1=("r1", "mean"))
    out["by_coin"] = A.groupby("coin").agg(gain=("g", "mean"), mu=("mu", "first"), short=("pos", lambda x: (x < 0).mean()))
    D["year_w"] = D.w
    out["by_window"] = D.groupby("w").agg(book=("br", "mean"), hold=("cr", "mean")).T
    return out
