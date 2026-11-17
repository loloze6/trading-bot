def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    samp = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r1 = c.shift(-1) / c - 1
            a = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            ret14 = c / c.shift(14) - 1
            ret60 = c / c.shift(60) - 1
            f7 = c.shift(-7) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "a": a, "r1": r1, "g": a * r1, "fee": fee,
                               "fc": b["forecast"], "ret14": ret14, "ret60": ret60, "f7": f7})
            rows.append(df)
            samp.append(df.iloc[::7])
    d = pd.concat(rows)
    s = pd.concat(samp).dropna(subset=["f7", "fc"])
    d["side"] = np.where(d.a > 0, "long", np.where(d.a < 0, "short", "flat"))
    out["by_side"] = d.groupby("side").agg(n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"),
                                           mean_a=("a", "mean"), mean_r1=("r1", "mean"), fee_sum=("fee", "sum"))
    out["total_gain_vs_fee"] = pd.Series({"gross_sum": d.g.sum(), "fee_sum": d.fee.sum(), "mean_abs_a": d.a.abs().mean(),
                                          "mean_a": d.a.mean(), "share_short": (d.a < 0).mean()})
    s["fq"] = pd.qcut(s.fc, 5, labels=False)
    out["fc_quint_f7"] = s.groupby("fq").agg(n=("f7", "size"), fc=("fc", "mean"), f7=("f7", "mean"),
                                             hit=("f7", lambda x: (x > 0).mean()))
    # by 60-day trend state
    d["tr"] = np.where(d.ret60 > 0, "up60", np.where(d.ret60 <= 0, "down60", "na"))
    out["side_by_trend"] = d.groupby(["tr", "side"]).agg(n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"))
    out["coin_gain"] = d.groupby(["coin", "side"]).g.sum().unstack()
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["w"] = w; t["coin"] = coin; dd.append(t)
    D = pd.concat(dd)
    D["wn"] = D.w.str[1:].astype(int)
    bk = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    eq = (1 + bk.book_return).cumprod(); dn = eq / eq.cummax() - 1
    heq = (1 + bk.coin_return).cumprod(); hdn = heq / heq.cummax() - 1
    out["book_vs_hold"] = pd.Series({"book_mean": bk.book_return.mean(), "hold_mean": bk.coin_return.mean(),
                                     "book_sh": bk.book_return.mean() / bk.book_return.std() * np.sqrt(365),
                                     "hold_sh": bk.coin_return.mean() / bk.coin_return.std() * np.sqrt(365),
                                     "book_mdd": dn.min(), "hold_mdd": hdn.min(), "corr": bk.corr().iloc[0, 1]})
    # drawdown episode
    trough = dn.idxmin(); peak = eq.loc[:trough].idxmax()
    ep = bk.loc[peak:trough]
    out["dd_episode"] = pd.Series({"peak_w": peak[0], "trough_w": trough[0], "days": len(ep),
                                   "book_cum": (1 + ep.book_return).prod() - 1, "hold_cum": (1 + ep.coin_return).prod() - 1})
    out["book_by_window"] = bk.groupby(level=0).agg(book=("book_return", "mean"), hold=("coin_return", "mean"))
    return out
