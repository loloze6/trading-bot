import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].dropna().copy()
            dd["coin"] = c; dd["win"] = w
            rows.append(dd)
    D = pd.concat(rows)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_overall"] = pd.Series({"mean": bk.book_return.mean(), "sd": bk.book_return.std(),
        "sharpe": bk.book_return.mean()/bk.book_return.std()*np.sqrt(365), "n_days": len(bk),
        "hold_mean": bk.coin_return.mean(),
        "hold_sharpe": bk.coin_return.mean()/bk.coin_return.std()*np.sqrt(365)})
    g = bk.groupby("win")
    out["book_by_window"] = pd.DataFrame({"mean": g.book_return.mean(), "n": g.size(),
        "sharpe": g.book_return.mean()/g.book_return.std()*np.sqrt(365), "hold_mean": g.coin_return.mean()})
    cc = D.groupby("coin").book_return.agg(["mean","size","sum"])
    cc["share_of_total"] = cc["sum"]/cc["sum"].sum()
    out["by_coin"] = cc

    B = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            b["r1"] = b.close.shift(-1)/b.close - 1
            b["pos"] = b.postRebalance_current_allocation.fillna(0)
            b["gain"] = b.pos*b.r1
            b["tr60"] = b.close/b.close.shift(60) - 1
            hi = b.high.rolling(20, min_periods=20).max(); lo = b.low.rolling(20, min_periods=20).min()
            b["rp"] = 2*(b.close - lo)/(hi - lo) - 1
            for h in [1,3,5,10,20]:
                b[f"f{h}"] = b.close.shift(-h)/b.close - 1
            b["coin"] = c; b["win"] = w; b["i"] = np.arange(len(b))
            B.append(b)
    B = pd.concat(B, ignore_index=True)
    mu = B.groupby("coin").r1.mean()
    B["mkt"] = B.pos*B.coin.map(mu)
    B["timing"] = B.gain - B.mkt
    B["side"] = np.sign(B.pos).map({1.0:"long",-1.0:"short",0.0:"flat"})
    B["trend"] = pd.cut(B.tr60, [-np.inf,-0.1,0.1,np.inf], labels=["falling","choppy","rising"])
    out["by_side_gain"] = B.groupby("side")[["gain","mkt","timing"]].agg(["sum","mean","count"])
    out["by_trend_side"] = B[B.pos!=0].groupby(["trend","side"], observed=True)[["gain","timing"]].agg(["sum","mean","count"])
    out["by_coin_side_gainsum"] = B[B.pos!=0].groupby(["coin","side"]).gain.sum().unstack()

    T = pd.concat([tr.assign(coin=c) for c in data["trades"] for w,tr in data["trades"][c].items() if len(tr)])
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10_sum": p.head(10).sum(), "top20_sum": p.head(20).sum(),
        "long_sum": T[T.side=="LONG"].net_profit_loss_percent.sum(), "short_sum": T[T.side=="SHORT"].net_profit_loss_percent.sum(),
        "n_long": (T.side=="LONG").sum(), "n_short": (T.side=="SHORT").sum(), "win_rate": (p>0).mean()})

    res = {}
    for h in [1,3,5,10,20]:
        m = B[B.i % h == 0].groupby("coin")[f"f{h}"].mean()
        g2 = B[(B.i % h == 0) & (B.forecast != 0)].dropna(subset=[f"f{h}"]).copy()
        g2["x"] = np.sign(g2.forecast)*(g2[f"f{h}"] - g2.coin.map(m))
        for sd, nm in [(1,"long"),(-1,"short"),(0,"all")]:
            x = g2.x if sd==0 else g2[np.sign(g2.forecast)==sd].x
            res[(h, nm)] = [x.mean(), x.mean()/x.std()*np.sqrt(len(x)), len(x)]
    out["horizon_signed_excess"] = pd.DataFrame(res, index=["mean","t","n"]).T

    m5 = B[B.i%5==0].groupby("coin").f5.mean()
    g5 = B[(B.i % 5 == 0) & (B.forecast != 0)].dropna(subset=["f5","rp"]).copy()
    g5["e"] = g5.f5 - g5.coin.map(m5)
    g5["x"] = np.sign(g5.forecast)*g5.e
    g5["sd"] = np.where(g5.forecast>0,"long","short")
    gg = g5.groupby(["trend","sd"], observed=True).x
    out["5d_by_trend_side"] = pd.DataFrame({"mean": gg.mean(), "n": gg.size(), "t": gg.mean()/gg.std()*np.sqrt(gg.size())})
    g5["q"] = pd.cut(g5.rp, [-1.01,-0.6,-0.2,0.2,0.6,1.01], labels=["b0","b1","mid","t1","t0"])
    gq = g5.groupby("q", observed=True).e
    out["rp_bucket_e5"] = pd.DataFrame({"e5": gq.mean(), "n": gq.size(), "t": gq.mean()/gq.std()*np.sqrt(gq.size())})
    out["rp_bucket_by_trend_e5"] = g5.groupby(["trend","q"], observed=True).e.mean().unstack()
    out["rp_bucket_by_trend_n"] = g5.groupby(["trend","q"], observed=True).e.size().unstack()
    # all bars (incl. agitated) 5d excess by rp bucket, to compare calm vs agitated
    a5 = B[(B.i % 5 == 0)].dropna(subset=["f5","rp"]).copy()
    a5["e"] = a5.f5 - a5.coin.map(m5)
    a5["calm"] = np.where(a5.forecast != 0, "calm", "other")
    a5["q"] = pd.cut(a5.rp, [-1.01,-0.6,-0.2,0.2,0.6,1.01], labels=["b0","b1","mid","t1","t0"])
    out["rp_bucket_calm_vs_other_e5"] = a5.groupby(["calm","q"], observed=True).e.mean().unstack()
    out["rp_bucket_calm_vs_other_n"] = a5.groupby(["calm","q"], observed=True).e.size().unstack()
    # by year of the 5d signed excess
    g5["yr"] = pd.to_datetime(g5.timestamp).dt.year
    gy = g5.groupby("yr").x
    out["5d_signed_by_year"] = pd.DataFrame({"mean": gy.mean(), "n": gy.size(), "t": gy.mean()/gy.std()*np.sqrt(gy.size())})
    return out
