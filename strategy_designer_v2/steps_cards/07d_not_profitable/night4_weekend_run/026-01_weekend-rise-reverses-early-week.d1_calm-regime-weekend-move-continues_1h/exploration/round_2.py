def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            al = b["postRebalance_current_allocation"].values
            n = len(b)
            act = np.where((b["regime"].values == "trending") & (b["forecast"].abs().values >= 2))[0]
            for i in act:
                if i + 48 >= n or i - 168 < 0:
                    continue
                f = b["forecast"].iloc[i]
                s = np.sign(f)
                r48 = c[i+48]/c[i]-1
                pre = c[i-48]/c[i-168]-1
                # vol of prior 30d hourly returns relative within window
                hr = np.diff(np.log(c[max(0,i-720):i+1]))
                vol = hr.std()
                gain = np.nansum(al[i:i+48] * (c[i+1:i+49]/c[i:i+48]-1))
                rows.append(dict(coin=coin, win=w, f=f, s=s, sret=s*r48, pre_al=s*pre,
                                 pre_al_z=s*pre/(vol*np.sqrt(120)), gain=gain, alloc=abs(al[i])))
    d = pd.DataFrame(rows)
    def agg(g):
        return pd.Series(dict(n=len(g), mean_sret=g.sret.mean(),
                              t=g.sret.mean()/(g.sret.std()/np.sqrt(len(g))),
                              book_gain=g.gain.mean(), t_gain=g.gain.mean()/(g.gain.std()/np.sqrt(len(g))),
                              worst_gain=g.gain.min(), share_neg=(g.gain<0).mean()))
    d["preq"] = pd.qcut(d["pre_al_z"], 5, labels=False)
    out["by_prior5d_in_weekend_dir_quintile"] = d.groupby("preq").apply(agg)
    out["by_prior_quintile_and_side"] = d.groupby(["s","preq"]).apply(agg)
    out["corr_prez_sret"] = float(d[["pre_al_z","sret"]].corr().iloc[0,1])
    # worst case gains: what did prior look like
    w = d.nsmallest(60, "gain")
    out["worst60_cases"] = pd.Series(dict(mean_pre_al_z=w.pre_al_z.mean(), all_mean_pre_al_z=d.pre_al_z.mean(),
                                          share_pre_against=(w.pre_al<0).mean(), all_share_pre_against=(d.pre_al<0).mean(),
                                          share_short=(w.s<0).mean(), all_share_short=(d.s<0).mean(),
                                          mean_alloc=w.alloc.mean(), all_alloc=d.alloc.mean()))
    # book drawdown on the pooled daily chain
    dd = []
    for coin, ws in data["days"].items():
        for wn, x in ws.items():
            dd.append(x.assign(coin=coin, win=wn))
    D = pd.concat(dd)
    D["day"] = pd.to_datetime(D["day"])
    P = D.groupby(["win","day"])["book_return"].mean().dropna()
    order = sorted(P.index.get_level_values(0).unique(), key=lambda s: int(s[1:]))
    chain = pd.concat([P.loc[o] for o in order])
    v = (1+chain.values).cumprod()
    peak = np.maximum.accumulate(v)
    ddv = v/peak-1
    out["book_chain"] = pd.Series(dict(days=len(v), yearly=v[-1]**(365/len(v))-1, maxdd=ddv.min(),
                                       mean=chain.mean(), sd=chain.std()))
    wins = []
    for o in order:
        x = (1+P.loc[o]).cumprod().values
        wins.append(dict(win=o, ret=x[-1]-1, dd=(x/np.maximum.accumulate(x)-1).min()))
    out["by_window_ret_dd"] = pd.DataFrame(wins).set_index("win")
    return out
