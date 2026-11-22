def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    H = 18
    out = {}
    fz = []; mk = []; bk = []; tim = []
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); sd = np.std(allr)
        dmean = pd.concat([d["coin_return"] for d in days[coin].values()]).mean()
        for w, b in wins.items():
            fc = b["forecast"].values; al = b["postRebalance_current_allocation"].values
            fz.append(pd.DataFrame(dict(f0=(fc == 0), short=(al < 0))))
            ts = pd.to_datetime(b["timestamp"])
            ald = pd.Series(al, index=ts).resample("1D").last()
            d = days[coin][w].copy()
            d["alloc_prev"] = ald.shift(1).values[:len(d)] if len(ald) == len(d) else np.nan
            d["mkt"] = d["alloc_prev"] * dmean
            d["coin"] = coin; d["w"] = w
            bk.append(d)
            c = b["close"].values; n = len(c)
            tr180 = pd.Series(c).pct_change(180).values
            vf = b["debug_info.components.vol_fade.last_history_value"].values
            for g in range(0, n - H, H):
                cand = np.where(fc[g:g+H] <= -2)[0]
                if len(cand) == 0: continue
                i = g + cand[0]
                if i + H >= n or np.isnan(tr180[i]): continue
                ret = c[i+H]/c[i]-1
                rows.append(dict(tr=tr180[i]/ (sd*np.sqrt(10)), vf=vf[i], u=-(ret-drift)))
    f = pd.concat(fz)
    out["forecast0_vs_short"] = pd.Series(dict(share_f0=f.f0.mean(), share_short_when_f0=f.short[f.f0].mean()))
    B = pd.concat(bk)
    B = B.dropna(subset=["book_return"])
    out["book_decomp"] = pd.Series(dict(book_mean=B.book_return.mean(), market_part=B.mkt.mean(), coin_mean=B.coin_return.mean(),
        timing=B.book_return.mean()-B.mkt.mean()))
    # worst days: coin return during them
    B["bq"] = pd.qcut(B.book_return.rank(method="first"), 10, labels=False)
    out["by_book_decile"] = B.groupby("bq")[["book_return","coin_return","alloc_prev"]].mean()
    df = pd.DataFrame(rows)
    df["trq"] = pd.qcut(df.tr.rank(method="first"), 10, labels=False)
    g = df.groupby("trq")
    out["unusual_by_30d_trend_decile"] = pd.DataFrame(dict(n=g.u.size(), tr=g.tr.mean(), u=g.u.mean(), t=g.u.mean()/(g.u.std()/np.sqrt(g.u.size()))))
    low = df[df.tr < df.tr.median()].copy()
    low["vq"] = pd.qcut(low.vf.rank(method="first"), 4, labels=False)
    g = low.groupby("vq")
    out["lowtrend_by_volfade_q"] = pd.DataFrame(dict(n=g.u.size(), u=g.u.mean(), t=g.u.mean()/(g.u.std()/np.sqrt(g.u.size()))))
    return out
