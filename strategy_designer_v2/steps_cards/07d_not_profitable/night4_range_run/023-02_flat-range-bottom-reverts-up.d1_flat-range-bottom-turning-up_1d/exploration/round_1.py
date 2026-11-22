import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    # Book daily returns per window (mean over coins per day)
    per_win = {}
    for c in coins:
        for w, d in days[c].items():
            per_win.setdefault(w, []).append(d.set_index("day")[["book_return","coin_return"]].add_suffix("_"+c))
    book_rows = []
    chain = []
    for w in sorted(per_win, key=lambda x: int(x[1:])):
        df = pd.concat(per_win[w], axis=1)
        br = df[[k for k in df.columns if k.startswith("book_return")]].mean(axis=1)
        cr = df[[k for k in df.columns if k.startswith("coin_return")]].mean(axis=1)
        book_rows.append(dict(window=w, n=br.notna().sum(), book_mean=br.mean(), hold_mean=cr.mean(),
                              book_sum=br.sum(), hold_sum=cr.sum()))
        chain.append(br.dropna())
    bw = pd.DataFrame(book_rows).set_index("window")
    out["book_by_window"] = bw
    s = pd.concat(chain, ignore_index=True)
    v = (1+s).cumprod(); dd = v/v.cummax()-1
    out["book_overall"] = pd.Series(dict(mean=s.mean(), std=s.std(), maxdd=dd.min(), n=len(s),
                                        share_days_nonzero=(s.abs()>1e-9).mean()))
    # Allocation stats and gain decomposition
    rows = []
    allg = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            b["r1"] = b["close"].shift(-1)/b["close"]-1
            b["gain"] = b["postRebalance_current_allocation"]*b["r1"]
            b["coin"]=c; b["window"]=w
            allg.append(b[["coin","window","close","forecast","regime","postRebalance_current_allocation","r1","gain"]])
    G = pd.concat(allg)
    mu = G.groupby("coin")["r1"].mean()
    G["mkt"] = G["postRebalance_current_allocation"]*G["coin"].map(mu)
    inpos = G["postRebalance_current_allocation"].abs()>1e-6
    out["by_coin"] = G.groupby("coin").apply(lambda g: pd.Series(dict(
        share_in=(g.postRebalance_current_allocation.abs()>1e-6).mean(),
        mean_alloc_in=g.loc[g.postRebalance_current_allocation.abs()>1e-6,"postRebalance_current_allocation"].mean(),
        gain_mean=g.gain.mean(), mkt_mean=g.mkt.mean(), timing=g.gain.mean()-g.mkt.mean(),
        coin_r1_mean=g.r1.mean())))
    out["regime_share"] = G["regime"].value_counts(normalize=True)
    # Forecast buckets: 5-bar forward on grid
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"].values; f = b["forecast"].values
            for i in range(0, len(b)-5, 5):
                recs.append((c, w, f[i], cl[i+5]/cl[i]-1, b["regime"].values[i]))
    R = pd.DataFrame(recs, columns=["coin","window","f","r5","regime"])
    m5 = R.groupby("coin")["r5"].mean()
    sd5 = R.groupby("coin")["r5"].std()
    R["ex"] = R["r5"]-R["coin"].map(m5)
    R["z"] = R["ex"]/R["coin"].map(sd5)
    act = R[R.f>0].copy()
    act["q"] = pd.qcut(act.f.rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["fcst_quartiles_5d"] = act.groupby("q").agg(n=("r5","size"), f=("f","mean"), total=("r5","mean"), ex=("ex","mean"), strength=("z","mean"))
    sl = stats.linregress(act.f, act.ex)
    out["size_of_idea"] = pd.Series(dict(n=len(act), total=act.r5.mean(), unusual=act.ex.mean(),
            strength=act.z.mean(), t_mean=stats.ttest_1samp(act.ex,0).statistic, slope_t=sl.slope/sl.stderr,
            drift5_mean=m5.mean(), usual5=sd5.mean()))
    mr = R[R.regime=="mean_reversion"]
    out["mr_regime_all_5d"] = mr.groupby(mr.f>0).agg(n=("r5","size"), total=("r5","mean"), ex=("ex","mean"))
    # Trades
    T = pd.concat([t.assign(coin=c) for c in coins for w,t in trades[c].items()])
    out["trades"] = pd.Series(dict(n=len(T), gross=T.profit_loss_percent.mean(), net=T.net_profit_loss_percent.mean(),
        win=(T.net_profit_loss_percent>0).mean(), dur_days=T.duration_minutes.mean()/1440,
        worst=T.net_profit_loss_percent.min(), p10=T.net_profit_loss_percent.quantile(.1)))
    return out
