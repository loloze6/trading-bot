def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []; samp = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r1 = c.shift(-1) / c - 1
            a = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            ret14 = c / c.shift(14) - 1
            ret30 = c / c.shift(30) - 1
            f7 = c.shift(-7) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "a": a, "r1": r1, "g": a * r1, "fee": fee,
                               "fc": b["forecast"], "ret14": ret14, "ret30": ret30, "f7": f7})
            rows.append(df); samp.append(df.iloc[::7])
    d = pd.concat(rows); s = pd.concat(samp).dropna(subset=["f7", "fc"])
    cm = s.groupby("coin").f7.mean(); s["f7x"] = s.f7 - s.coin.map(cm)
    d["side"] = np.where(d.a > 0, "long", np.where(d.a < 0, "short", "flat"))
    d["tr30"] = np.where(d.ret30.isna(), "na", np.where(d.ret30 > 0, "up30", "down30"))
    out["side_by_tr30"] = d.groupby(["tr30", "side"]).agg(n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"), fee=("fee", "sum"))
    # forecast slope on each side separately
    res = {}
    for nm, sub in [("pos", s[s.fc > 0]), ("neg", s[s.fc < 0])]:
        sl = stats.linregress(sub.fc, sub.f7x)
        res[nm] = {"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr, "mean_f7x": sub.f7x.mean(),
                   "t_mean": stats.ttest_1samp(sub.f7x, 0).statistic}
    out["side_slope"] = pd.DataFrame(res).T
    # short samples by 30d trend: excess fwd
    s["tr30"] = np.where(s.ret30.isna(), "na", np.where(s.ret30 > 0, "up30", "down30"))
    out["neg_fc_by_tr30"] = s[s.fc < 0].groupby("tr30").agg(n=("f7", "size"), f7=("f7", "mean"), f7x=("f7x", "mean"))
    out["pos_fc_by_tr30"] = s[s.fc > 0].groupby("tr30").agg(n=("f7", "size"), f7=("f7", "mean"), f7x=("f7x", "mean"))
    # long-only book approximation: daily mean over coins of gain only when long, gross
    d["wn"] = d.w.str[1:].astype(int)
    d["idx"] = d.groupby(["coin", "w"]).cumcount()
    dl = d.copy(); dl["gl"] = np.where(dl.a > 0, dl.g, 0.0); dl["feel"] = np.where(dl.a > 0, dl.fee, 0)
    agg = dl.groupby(["wn", "idx"]).agg(g=("g", "mean"), gl=("gl", "mean"), fee=("fee", "mean"), feel=("feel", "mean"))
    agg = agg.dropna()
    def stat(x):
        eq = (1 + x).cumprod(); dn = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(x)) - 1
        return pd.Series({"mean": x.mean(), "sh": x.mean() / x.std() * np.sqrt(365), "mdd": dn, "calmar": yr / -dn})
    out["approx_books"] = pd.DataFrame({"both_net": stat(agg.g - agg.fee), "long_only_net": stat(agg.gl - agg.feel)}).T
    # fee per side
    out["fee_vs_gain_long_short"] = d.groupby("side").agg(gain=("g", "sum"), fee=("fee", "sum"), turnover=("a", lambda x: x.diff().abs().sum()))
    return out
