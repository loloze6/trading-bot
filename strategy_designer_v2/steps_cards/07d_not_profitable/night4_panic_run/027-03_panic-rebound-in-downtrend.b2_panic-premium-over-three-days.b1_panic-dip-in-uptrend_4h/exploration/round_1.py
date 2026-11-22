def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # --- book: exposure, trades
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            d = data["days"][c][w]
            rows.append(dict(coin=c, w=w, expo=a.abs().mean(), inpos=(a.abs() > 1e-6).mean(),
                             act=(b["forecast"].fillna(0) != 0).mean(),
                             regime_mr=(b["regime"] == "mean_reversion").mean(),
                             bookret=d["book_return"].mean(), coinret=d["coin_return"].mean()))
    r = pd.DataFrame(rows)
    out["book_by_coin"] = r.groupby("coin")[["expo", "inpos", "act", "regime_mr", "bookret", "coinret"]].mean()
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t):
                t = t.copy(); t["coin"] = c; tr.append(t)
    tr = pd.concat(tr)
    g = tr.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
                               gross=("profit_loss_percent", "mean"),
                               net=("net_profit_loss_percent", "mean"),
                               hold_h=("duration_minutes", lambda x: x.mean() / 60),
                               winshare=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades_by_coin"] = g
    out["trades_all"] = pd.Series(dict(n=len(tr), gross=tr.profit_loss_percent.mean(),
                                       net=tr.net_profit_loss_percent.mean(),
                                       t_net=stats.ttest_1samp(tr.net_profit_loss_percent, 0).statistic,
                                       hold_h=tr.duration_minutes.mean() / 60))
    # --- cases from prices under broader situations
    H = [18, 42, 84]
    recs = []
    drift = {h: {} for h in H}; sd = {h: {} for h in H}
    for c in data["bars"]:
        for h in H:
            rs = []
            for w, b in data["bars"][c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs); drift[h][c] = rs.mean(); sd[h][c] = rs.std()
        for w, b in data["bars"][c].items():
            cl = b["close"]; rng = (b["high"] - b["low"]) / cl
            ratio = rng.rolling(6).mean() / rng.rolling(180).mean()
            ret6 = cl / cl.shift(6) - 1
            vol6 = ret6.abs().rolling(180).mean()
            prior = cl.shift(6) / cl.shift(186) - 1
            df = pd.DataFrame(dict(ratio=ratio.values, ret6=ret6.values, depth=(-ret6 / vol6).values,
                                   prior=prior.values, pos=np.arange(len(cl))))
            for h in H:
                df[f"x{h}"] = (cl.shift(-h) / cl - 1).values - drift[h][c]
                df[f"s{h}"] = df[f"x{h}"] / sd[h][c]
            df["coin"] = c; df["w"] = w
            df = df[(df.ratio >= 1.5) & (df.ret6 < 0)].dropna(subset=["ratio", "prior", "depth"])
            df["cell"] = df.pos // 18
            recs.append(df.groupby("cell").head(1))
    k = pd.concat(recs)
    k["rbin"] = pd.cut(k.ratio, [1.5, 2, 3, 100], right=False)
    k["pbin"] = np.where(k.prior > 0, "prior_up", "prior_down")
    k["dbin"] = pd.cut(k.depth, [-1, 1, 2, 3, 100])
    def summ(gr):
        o = {"n": len(gr)}
        for h in H:
            x = gr[f"x{h}"].dropna()
            o[f"m{h}"] = x.mean(); o[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
            o[f"str{h}"] = gr[f"s{h}"].mean()
        return pd.Series(o)
    out["by_ratio_prior"] = k.groupby(["rbin", "pbin"], observed=True).apply(summ)
    out["by_ratio_depth"] = k.groupby(["rbin", "dbin"], observed=True).apply(summ)
    out["by_coin_ratio2plus"] = k[k.ratio >= 2].groupby("coin").apply(summ)
    return out
