def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for H in (7, 26):
        drift = {}
        for c in bars:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl) - H, H):
                    rs.append(cl[i+H]/cl[i]-1)
            drift[c] = (np.mean(rs), np.std(rs))
        for c in bars:
            for w, b in bars[c].items():
                cl = b["close"].astype(float).values; hi = b["high"].astype(float).values; lo = b["low"].astype(float).values
                r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
                n = len(cl)
                for i in range(0, n - H, H):
                    f = cl[i+H]/cl[i]-1 - drift[c][0]
                    d = dict(H=H, coin=c, win=w, fwd=f, fz=f/drift[c][1],
                             fc=float(b["forecast"].iloc[i]),
                             alloc=float(b["postRebalance_current_allocation"].iloc[i]))
                    d["r7"] = cl[i]/cl[i-7]-1 if i >= 7 else np.nan
                    d["r26"] = cl[i]/cl[i-26]-1 if i >= 26 else np.nan
                    if i >= 25:
                        mid = (hi[i-25:i+1].max()+lo[i-25:i+1].min())/2
                        rng = hi[i-25:i+1].max()-lo[i-25:i+1].min()
                        d["pos26"] = (cl[i]-mid)/rng if rng > 0 else np.nan
                    else: d["pos26"] = np.nan
                    d["vol30"] = np.nanstd(r1[max(1,i-29):i+1]) if i >= 15 else np.nan
                    d["r1"] = r1[i]
                    d["rng1"] = (hi[i]-lo[i])/cl[i]
                    d["volchg"] = (np.nanstd(r1[max(1,i-6):i+1]) / d["vol30"]) if i >= 15 else np.nan
                    rows.append(d)
    df = pd.DataFrame(rows)
    res = []
    for H in (7, 26):
        g = df[df.H == H]
        for feat in ["r7", "r26", "pos26", "vol30", "r1", "rng1", "volchg", "fc"]:
            s = g[[feat, "fz", "fwd"]].dropna()
            if feat == "fc": s = s[s.fc != 0]
            if len(s) < 30: continue
            # rank within coin to make graded per coin
            sc = g.loc[s.index].groupby("coin")[feat].rank(pct=True)
            rho, p = stats.spearmanr(sc, s["fz"])
            top = s["fwd"][sc > 0.8]; bot = s["fwd"][sc <= 0.2]
            t = stats.ttest_ind(top, bot, equal_var=False).statistic
            npos = sum(stats.spearmanr(g.loc[s.index][g.loc[s.index].coin == c][feat], s["fz"][g.loc[s.index].coin == c])[0] > 0 for c in bars)
            res.append(dict(H=H, feat=feat, n=len(s), rho=rho, p=p, top20=top.mean(), bot20=bot.mean(), t_top_bot=t, coins_rho_pos=npos))
    out["feature_vs_fwd"] = pd.DataFrame(res).round(4)
    # weekday of daily coin returns
    dd = pd.concat([days[c][w].assign(coin=c) for c in days for w in days[c]])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["weekday"] = dd.groupby("wd")["coin_return"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))]).round(5)
    # book: by position sign, coin return next day
    bb = pd.concat([bars[c][w][["close", "postRebalance_current_allocation", "regime"]].assign(nxt=lambda x: x.close.shift(-1)/x.close-1, coin=c) for c in bars for w in bars[c]])
    bb["short"] = bb.postRebalance_current_allocation < 0
    out["next_day_by_short"] = bb.groupby("short")["nxt"].agg(["mean", "count"])
    out["regime_share"] = bb.regime.value_counts(normalize=True)
    # by year, 26-day cases of forecast<0
    g = df[(df.H == 26) & (df.fc < 0)].copy()
    out["active_cases_by_coin"] = g.groupby("coin")["fwd"].agg(["mean", "count"]).round(4)
    return out
