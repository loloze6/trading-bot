def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    winrows = []
    for coin, ws in data["bars"].items():
        allc = []
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r1 = c.shift(-1) / c - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            gain = pos * r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            low30 = c.rolling(30, min_periods=10).min().shift(1)
            high30 = c.rolling(30, min_periods=10).max()
            dd = c / high30 - 1
            ret10p = c / c.shift(10) - 1
            r10 = c.shift(-10) / c - 1
            # run length of consecutive new-low bars
            nl = (c < low30).astype(int)
            run = nl.groupby((nl != nl.shift()).cumsum()).cumsum()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "r1": r1, "gain": gain, "fee": fee,
                               "dd": dd, "ret10p": ret10p, "r10": r10, "run": run, "active": pos != 0,
                               "fc": b["forecast"]})
            rows.append(df)
            d = data["days"][coin][w]
            winrows.append({"coin": coin, "w": w, "book_mean": d["book_return"].mean(),
                            "coin_mean": d["coin_return"].mean(),
                            "book_sum": d["book_return"].sum(), "coin_sum": d["coin_return"].sum(),
                            "active_bars": int((pos != 0).sum())})
    A = pd.concat(rows)
    W = pd.DataFrame(winrows)
    out["by_window"] = W.groupby("w")[["book_sum", "coin_sum", "active_bars"]].sum().round(4)
    act = A[A.active & A.r1.notna()]
    out["active_summary"] = pd.Series({
        "n_active": len(act), "mean_gain": act.gain.mean(), "mean_fee_all_bars": A.fee.mean(),
        "mean_r1_active": act.r1.mean(), "mean_r1_all": A.r1.mean(), "mean_pos": act.pos.mean(),
        "sum_gain": act.gain.sum(), "sum_fee": A.fee.sum()})
    act = act.copy()
    act["dd_q"] = pd.qcut(act.dd, 4, labels=["deep", "q2", "q3", "mild"])
    out["by_dd_quartile"] = act.groupby("dd_q").agg(n=("gain", "size"), gain=("gain", "mean"),
                                                   r1=("r1", "mean"), r10=("r10", "mean"))
    act["run_b"] = pd.cut(act.run, [0, 1, 2, 4, 100])
    out["by_run_length"] = act.groupby("run_b").agg(n=("gain", "size"), gain=("gain", "mean"),
                                                   r1=("r1", "mean"), r10=("r10", "mean"))
    act["p10_q"] = pd.qcut(act.ret10p, 4, labels=["p10_most_down", "q2", "q3", "p10_least_down"])
    out["by_prior10"] = act.groupby("p10_q").agg(n=("gain", "size"), gain=("gain", "mean"),
                                                 r1=("r1", "mean"), r10=("r10", "mean"), dd=("dd", "mean"))
    act["year"] = 0
    out["by_coin"] = act.groupby("coin").agg(n=("gain", "size"), gain=("gain", "mean"), r10=("r10", "mean"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = pd.Series({"n": len(T), "mean_pl": T.profit_loss_percent.mean(),
                               "mean_net": T.net_profit_loss_percent.mean(),
                               "win": (T.profit_loss_percent > 0).mean(),
                               "mean_dur_days": T.duration_minutes.mean() / 1440})
    return out
