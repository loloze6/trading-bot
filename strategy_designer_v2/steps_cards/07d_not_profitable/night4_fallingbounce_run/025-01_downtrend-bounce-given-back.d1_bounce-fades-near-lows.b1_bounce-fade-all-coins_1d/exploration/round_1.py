def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daily = []
    trades = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            z = r1 / sd20
            ret90 = c / c.shift(90) - 1
            low90 = c.rolling(90).min()
            D = (c / low90 - 1) * 100
            ret30 = c / c.shift(30) - 1
            f = b["forecast"].astype(float).fillna(0)
            pos = b["postRebalance_current_allocation"].astype(float).fillna(0)
            n = len(b)
            fw = {h: c.shift(-h) / c - 1 for h in (1, 2, 3, 5, 10)}
            sig = (f < -2) & (f.shift(1).fillna(0) >= -2)
            seen = set()
            for i in np.where(sig.values)[0]:
                cell = i // 5
                if cell in seen:
                    continue
                seen.add(cell)
                d = {"coin": coin, "w": w, "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "absf": -f.iloc[i], "z": z.iloc[i], "D": D.iloc[i], "ret90": ret90.iloc[i],
                     "ret30": ret30.iloc[i], "r1": r1.iloc[i], "sd20": sd20.iloc[i]}
                for h in fw:
                    d["s%d" % h] = -fw[h].iloc[i]
                rows.append(d)
            # coin drift per bar
            dd = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "nxt": c.shift(-1) / c - 1})
            daily.append(dd)
        for w, t in data["trades"].get(coin, {}).items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tt["w"] = w
                trades.append(tt)
    cs = pd.DataFrame(rows)
    out["n_cases"] = len(cs)
    def summ(g):
        res = {}
        for h in (1, 2, 3, 5, 10):
            x = g["s%d" % h].dropna()
            res["mean_s%d" % h] = x.mean()
            res["t_s%d" % h] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        res["n"] = len(g)
        return pd.Series(res)
    out["all_cases_total_short_move"] = summ(cs)
    cs["q_absf"] = pd.qcut(cs["absf"].rank(method="first"), 4, labels=False)
    out["by_absf_quartile"] = cs.groupby("q_absf").apply(summ)
    cs["q_ret90"] = pd.qcut(cs["ret90"].rank(method="first"), 4, labels=False)
    out["by_ret90_quartile"] = cs.dropna(subset=["ret90"]).groupby("q_ret90").apply(summ)
    cs["q_ret30"] = pd.qcut(cs["ret30"].rank(method="first"), 4, labels=False)
    out["by_ret30_quartile"] = cs.groupby("q_ret30").apply(summ)
    cs["q_D"] = pd.qcut(cs["D"].rank(method="first"), 4, labels=False)
    out["by_D_quartile"] = cs.groupby("q_D").apply(summ)
    cs["q_z"] = pd.qcut(cs["z"].rank(method="first"), 4, labels=False)
    out["by_z_quartile"] = cs.groupby("q_z").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["quartile_edges"] = cs[["absf", "ret90", "ret30", "D", "z"]].quantile([0.25, 0.5, 0.75])
    # book
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["w"] = w
            dl.append(dd)
    D_ = pd.concat(dl)
    bk = D_.groupby(["w", "day"])[["book_return", "coin_return"]].mean()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "count"]).sort_values(("book_return", "mean")).head(24)
    dly = pd.concat(daily)
    out["share_bars_short"] = (dly["pos"] < 0).mean()
    out["mean_pos_when_short"] = dly.loc[dly["pos"] < 0, "pos"].mean()
    if trades:
        T = pd.concat(trades)
        T["days"] = T["duration_minutes"] / 1440
        out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
                                             gross=("profit_loss_percent", "mean"),
                                             net=("net_profit_loss_percent", "mean"),
                                             days=("days", "mean"))
    return out
