import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 72
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            n = len(c)
            for i in range(0, n, H):
                if i - H < 0 or i + H >= n: continue
                past = c[i]/c[i-H]-1
                fwd = c[i+H]/c[i]-1
                hr = r1[i-H+1:i+1]
                top3g = np.sort(hr)[-3:].sum()
                top3l = np.sort(hr)[:3].sum()
                gshare = min(top3g/past, 1) if past > 0 else np.nan
                lshare = min(top3l/past, 1) if past < 0 else np.nan
                vol = np.nanstd(hr)
                fc = b["forecast"].iloc[i]
                al = b["postRebalance_current_allocation"].iloc[i]
                rows.append((coin, w, past, fwd, gshare, lshare, vol, fc, al))
    g = pd.DataFrame(rows, columns=["coin","w","past","fwd","gshare","lshare","vol","fc","al"])
    g["exc"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def summ(df, col):
        q = df.groupby(col, observed=True)["exc"]
        return pd.DataFrame({"n": q.size(), "mean_exc": q.mean(), "t": q.mean()/(q.std()/np.sqrt(q.size()))})
    g["past_q"] = pd.qcut(g["past"], 5, labels=False)
    out["fwd72_by_past72_quintile"] = summ(g, "past_q")
    up = g[g.past > 0].copy()
    up["gq"] = pd.qcut(up["gshare"].rank(method="first"), 5, labels=False)
    out["up_fwd_by_jumpshare_q"] = summ(up, "gq")
    dn = g[g.past < 0].copy()
    dn["lq"] = pd.qcut(dn["lshare"].rank(method="first"), 5, labels=False)
    out["down_fwd_by_lossshare_q"] = summ(dn, "lq")
    g["vq"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["fwd_by_vol_q"] = summ(g, "vq")
    # interaction: up moves by past size quintile x jump share half
    up["pq"] = pd.qcut(up["past"], 3, labels=False)
    up["gh"] = (up["gshare"] > up.groupby("pq")["gshare"].transform("median")).astype(int)
    out["up_pastsize_x_jumphalf"] = up.groupby(["pq","gh"])["exc"].agg(["size","mean"])
    # book decomposition
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            b = data["bars"][coin][w]
            ts = pd.to_datetime(b["timestamp"])
            a = b.groupby(ts.dt.floor("D"))["postRebalance_current_allocation"].mean().values
            dd.append(pd.DataFrame({"coin":coin,"w":w,"br":d["book_return"].values,"cr":d["coin_return"].values,
                                    "al_prev":np.r_[np.nan, a[:-1]] if len(a)==len(d) else np.nan}))
    D = pd.concat(dd)
    D["mu"] = D.groupby("coin")["cr"].transform("mean")
    D["mkt"] = D["al_prev"]*D["mu"]
    out["book_mean_daily"] = D["br"].mean()
    out["book_mkt_part"] = D["mkt"].mean()
    out["mean_alloc"] = D["al_prev"].mean()
    out["book_by_coin"] = D.groupby("coin")[["br","cr"]].mean()
    # hourly bars: hour/weekday mean return
    hrs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            gain = b["postRebalance_current_allocation"].shift(1)*r
            hrs.append(pd.DataFrame({"h":ts.dt.hour,"wd":ts.dt.weekday,"r":r,"gain":gain}))
    Hh = pd.concat(hrs).dropna()
    t = Hh.groupby("h")["r"].agg(["mean","std","size"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["size"]))
    out["ret_by_hour"] = t[["mean","t"]]
    t2 = Hh.groupby("wd")[["r","gain"]].mean()
    out["ret_gain_by_weekday"] = t2
    # trades
    tr = pd.concat([x for wins in data["trades"].values() for x in wins.values()])
    out["trades"] = tr.groupby("side")[["profit_loss_percent","net_profit_loss_percent","total_commission","duration_minutes"]].agg(["mean","count"]).T
    return out
