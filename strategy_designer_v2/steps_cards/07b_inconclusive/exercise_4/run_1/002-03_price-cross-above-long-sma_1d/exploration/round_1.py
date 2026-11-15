def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    fc = "debug_info.components.above_ma.last_history_value"
    # pooled mean daily return per coin
    mu = {}
    for c in bars:
        r = []
        for w, df in bars[c].items():
            r.append(df["close"].pct_change().dropna())
        mu[c] = pd.concat(r).mean()
    rows = []
    for H in [5, 10, 20, 40, 60]:
        for c in bars:
            for w, df in bars[c].items():
                cl = df["close"].values; f = df["forecast"].values
                raw = df[fc].values if fc in df else np.full(len(df), np.nan)
                al = df["postRebalance_current_allocation"].values
                for i in range(0, len(df) - H, H):
                    ex = cl[i+H]/cl[i]-1 - H*mu[c]
                    rows.append((H, c, w, f[i], raw[i], al[i], ex))
    R = pd.DataFrame(rows, columns=["H","coin","win","f","raw","al","ex"])
    out = {}
    # by horizon: above vs below SMA
    g = []
    for H, d in R.groupby("H"):
        a = d[d.f > 0].ex; b = d[d.f <= 0].ex
        rawpos = d[d.raw > 0].ex; rawneg = d[d.raw <= 0].ex
        g.append(dict(H=H, n_on=len(a), mean_on=a.mean(), t_on=stats.ttest_1samp(a,0).statistic,
                      share_on=(a>0).mean(), n_off=len(b), mean_off=b.mean(),
                      welch_on_off=stats.ttest_ind(a,b,equal_var=False).statistic,
                      n_rawpos=len(rawpos), mean_rawpos=rawpos.mean(), mean_rawneg=rawneg.mean(),
                      welch_raw=stats.ttest_ind(rawpos.dropna(),rawneg.dropna(),equal_var=False).statistic))
    out["by_horizon"] = pd.DataFrame(g).set_index("H")
    d20 = R[R.H == 20].copy()
    on = d20[d20.f > 0].copy()
    on["fq"] = pd.qcut(on.f.rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["on20_by_forecast_q"] = on.groupby("fq").agg(n=("ex","size"), f=("f","mean"), mean=("ex","mean"), med=("ex","median"), share=("ex", lambda x:(x>0).mean()))
    d20r = d20.dropna(subset=["raw"]).copy()
    d20r["rq"] = pd.qcut(d20r.raw.rank(method="first"), 6, labels=False)
    out["all20_by_raw_distance_sextile"] = d20r.groupby("rq").agg(n=("ex","size"), raw=("raw","mean"), mean=("ex","mean"), med=("ex","median"), share=("ex", lambda x:(x>0).mean()))
    out["on20_by_coin"] = on.groupby("coin").agg(n=("ex","size"), mean=("ex","mean"), med=("ex","median"), share=("ex", lambda x:(x>0).mean()))
    off = d20[d20.f <= 0]
    out["off20_by_coin"] = off.groupby("coin").agg(n=("ex","size"), mean=("ex","mean"))
    wn = on.copy(); wn["wi"] = wn.win.str[1:].astype(int)
    wn["wg"] = pd.cut(wn.wi, [0,6,12,18,24], labels=["w1-6","w7-12","w13-18","w19-24"])
    out["on20_by_window_group"] = wn.groupby("wg").agg(n=("ex","size"), mean=("ex","mean"), med=("ex","median"), share=("ex", lambda x:(x>0).mean()))
    # book decomposition
    br = []; tm = []
    for c in days:
        allr = pd.concat([d["coin_return"] for d in days[c].values()]).dropna().mean()
        for w, dd in days[c].items():
            b = bars[c][w].copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            x = dd.copy(); x["day"] = pd.to_datetime(x["day"]).dt.floor("D")
            x["al_prev"] = x["day"].map(al).shift(1)
            x = x.dropna(subset=["book_return","al_prev"])
            x["mkt"] = x.al_prev * allr
            x["coin"] = c
            br.append(x[["coin","book_return","mkt","al_prev","coin_return"]])
    B = pd.concat(br)
    out["book_decomp"] = pd.Series(dict(mean_book=B.book_return.mean(), market_part=B.mkt.mean(),
                                       timing=B.book_return.mean()-B.mkt.mean(), mean_alloc=B.al_prev.mean()))
    out["book_by_coin"] = B.groupby("coin").agg(mean=("book_return","mean"), mkt=("mkt","mean"), alloc=("al_prev","mean"))
    return out
