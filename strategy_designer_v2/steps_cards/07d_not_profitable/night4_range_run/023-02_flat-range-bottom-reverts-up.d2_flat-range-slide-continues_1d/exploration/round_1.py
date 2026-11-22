def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # coin mean daily return over all windows, and mean 5-bar return on grid
    rows = []; book_rows = []
    grid = []
    for c in bars:
        cr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = cr.mean()
        g5 = []
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"].values
            idx = np.arange(0, len(b)-5, 5)
            g5 += list(cl[idx+5]/cl[idx]-1)
        d5 = np.mean(g5)
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            alloc = b["postRebalance_current_allocation"].fillna(0)
            nxt = cl.shift(-1)/cl - 1
            gain = alloc*nxt
            dy = days[c][w]
            book_rows.append(dict(coin=c, window=w, book_mean=dy["book_return"].mean(),
                                  drift_part=(alloc.mean()*mu), timing=(gain - alloc*mu).mean(),
                                  short_share=(alloc<0).mean()))
            r60 = cl/cl.shift(60)-1
            r90 = cl/cl.shift(90)-1
            r10 = cl/cl.shift(10)-1
            fwd = cl.shift(-5)/cl-1
            rng = hi.rolling(30).max()-lo.rolling(30).min()
            pos = (cl - lo.rolling(30).min())/rng
            for i in range(0, len(b)-5, 5):
                if b.loc[i,"regime"]=="mean_reversion":
                    grid.append(dict(coin=c, window=w, f=b.loc[i,"forecast"], fwd=fwd[i], ex=fwd[i]-d5,
                                     r60=r60[i], r90=r90[i], r10=r10[i], pos=pos[i],
                                     vol=b.loc[i,"sizing_realised_vol"], alloc=alloc[i]))
    br = pd.DataFrame(book_rows)
    out["book_by_coin"] = br.groupby("coin")[["book_mean","drift_part","timing","short_share"]].mean()
    bw = br.groupby("window")[["book_mean","drift_part","timing"]].mean()
    out["book_by_window"] = bw
    g = pd.DataFrame(grid).dropna(subset=["fwd"])
    g["fb"] = pd.cut(g["f"], [-21,-10,-5,-2,-0.001,0.001], labels=["<-10","-10..-5","-5..-2","-2..0","0"])
    out["fwd_by_forecast"] = g.groupby("fb").agg(n=("fwd","size"), fwd=("fwd","mean"), ex=("ex","mean"))
    s = g[g.f<0].copy()
    for col in ["r60","r90","pos","vol","r10"]:
        s[col+"_q"] = pd.qcut(s[col], 4, labels=False, duplicates="drop")
        out["short_fwd_by_"+col] = s.groupby(col+"_q").agg(n=("fwd","size"), lo=(col,"min"), hi=(col,"max"), fwd=("fwd","mean"), ex=("ex","mean"))
    out["short_by_coin"] = s.groupby("coin").agg(n=("fwd","size"), fwd=("fwd","mean"), ex=("ex","mean"))
    s["year_w"]=s["window"]
    out["short_by_window"] = s.groupby("window").agg(n=("fwd","size"), fwd=("fwd","mean"))
    return out
