def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wd in data["bars"].items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            prev = np.r_[np.nan, c[1:] / c[:-1] - 1]
            run = np.zeros(n); cnt = 0
            for i in range(1, n):
                if prev[i] > 0:
                    run[i] = cnt; cnt = 0
                elif prev[i] < 0:
                    cnt += 1; run[i] = -1
                else:
                    cnt = 0
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            back20 = np.r_[[np.nan] * 20, c[20:] / c[:-20] - 1]
            back10 = np.r_[[np.nan] * 10, c[10:] / c[:-10] - 1]
            dvol = pd.Series(prev).rolling(20).std().values
            for i in range(n):
                rows.append(dict(coin=coin, w=w, i=i, ts=b["timestamp"].iloc[i], fc=b["forecast"].iloc[i],
                                 reg=b["regime"].iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i],
                                 run=run[i], up=prev[i], r1=r1[i], back20=back20[i], back10=back10[i], dvol=dvol[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["r1"].mean()
    df["x1"] = df["r1"] - df["coin"].map(drift)
    df["z20"] = df["back20"] / (df["dvol"] * np.sqrt(20))
    prof = df[df.reg == "unknown"].copy()
    cuts = prof["back20"].quantile([1/3, 2/3]).values
    prof["b20q"] = pd.cut(prof.back20, [-np.inf, cuts[0], cuts[1], np.inf], labels=["low", "mid", "high"])
    prof["sig"] = prof.fc < 0
    def summ(g, col="x1"):
        s = g[col].dropna()
        return pd.Series({"n": len(s), "mean_short": -s.mean(), "t": -s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["profile_by_b20_sig"] = prof.groupby(["b20q", "sig"]).apply(summ).round(4)
    out["b20_cuts"] = pd.Series(cuts).round(4)
    cs = prof[prof.sig].copy()
    cs["z20q"] = pd.qcut(cs.z20, 3, labels=["zlow", "zmid", "zhigh"])
    out["cases_by_z20"] = cs.groupby("z20q").apply(summ).round(4)
    cs["runb"] = np.where(cs.run >= 3, "3+", "2")
    out["cases_run_x_b20"] = cs.groupby(["runb", "b20q"]).apply(summ).round(4)
    # losing cases: what they looked like
    cs["loss"] = cs.x1 > 0.04
    out["bigloss_vs_rest"] = cs.groupby("loss")[["back20", "back10", "up", "run", "alloc", "dvol"]].mean().round(4)
    # how many coins shorted on same day
    cs["day"] = pd.to_datetime(cs.ts).dt.floor("D")
    nper = cs.groupby("day").coin.transform("count")
    cs["ncoins"] = np.where(nper >= 3, "3+", np.where(nper == 2, "2", "1"))
    out["cases_by_ncoins_sameday"] = cs.groupby("ncoins").apply(summ).round(4)
    # trades: net vs gross
    tl = []
    for coin, wd in data["trades"].items():
        for w, t in wd.items():
            tl.append(t.assign(coin=coin, w=w))
    T = pd.concat(tl)
    out["trades"] = pd.Series({"n": len(T), "gross_mean": T.profit_loss_percent.mean(), "net_mean": T.net_profit_loss_percent.mean(),
                               "mean_days": T.duration_minutes.mean() / 1440, "win_share": (T.net_profit_loss_percent > 0).mean()}).round(4)
    return out
