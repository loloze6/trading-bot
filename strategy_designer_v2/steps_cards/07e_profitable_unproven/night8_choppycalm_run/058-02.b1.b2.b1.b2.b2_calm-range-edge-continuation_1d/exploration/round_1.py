import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily returns: per day mean over coins
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
        "hold_mean": bk.coin_return.mean()})
    g = bk.groupby("win").book_return
    out["book_by_window"] = pd.DataFrame({"mean": g.mean(), "n": g.size(), "sharpe": g.mean()/g.std()*np.sqrt(365),
        "hold_mean": bk.groupby("win").coin_return.mean()})
    # per coin contribution (sum of coin book returns / n days of book)
    cc = D.groupby("coin").book_return.agg(["mean","size","sum"])
    cc["share_of_total"] = cc["sum"]/cc["sum"].sum()
    out["by_coin"] = cc
    # bar-level: position gain, side, trend profile, market rise
    B = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            b["r1"] = b.close.shift(-1)/b.close - 1
            b["pos"] = b.postRebalance_current_allocation
            b["gain"] = b.pos*b.r1
            b["tr60"] = b.close/b.close.shift(60) - 1
            b["rp"] = b["debug_info.components.range_pos.last_history_value"]
            for h in [1,3,5,10,20]:
                b[f"f{h}"] = b.close.shift(-h)/b.close - 1
            b["coin"] = c; b["win"] = w; b["i"] = np.arange(len(b))
            B.append(b)
    B = pd.concat(B, ignore_index=True)
    mu = B.groupby("coin").r1.mean()
    B["mkt"] = B.pos*B.coin.map(mu)
    B["timing"] = B.gain - B.mkt
    B["side"] = np.sign(B.pos).map({1:"long",-1:"short",0:"flat"})
    B["trend"] = pd.cut(B.tr60, [-np.inf,-0.1,0.1,np.inf], labels=["falling","choppy","rising"])
    s = B.groupby("side")[["gain","mkt","timing"]].agg(["sum","mean","count"])
    out["by_side_gain"] = s
    t = B[B.pos!=0].groupby(["trend","side"])[["gain","timing"]].agg(["sum","mean","count"])
    out["by_trend_side"] = t
    # trades concentration
    T = pd.concat([tr.assign(coin=c) for c in data["trades"] for w,tr in data["trades"][c].items()])
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10_sum": p.head(10).sum(), "top20_sum": p.head(20).sum(),
        "long_sum": T[T.side=="LONG"].net_profit_loss_percent.sum(), "short_sum": T[T.side=="SHORT"].net_profit_loss_percent.sum(),
        "n_long": (T.side=="LONG").sum(), "n_short": (T.side=="SHORT").sum()})
    # horizon: signed excess by forecast sign, non-overlapping grid per h, in calm (forecast!=0)
    res = {}
    for h in [1,3,5,10,20]:
        g2 = B[(B.i % h == 0) & (B.forecast != 0)].dropna(subset=[f"f{h}"]).copy()
        m = B[B.i % h == 0].groupby("coin")[f"f{h}"].mean()
        g2["x"] = np.sign(g2.forecast)*(g2[f"f{h}"] - g2.coin.map(m))
        for sd in [1,-1]:
            x = g2[np.sign(g2.forecast)==sd].x
            res[(h, "long" if sd>0 else "short")] = [x.mean(), x.mean()/x.std()*np.sqrt(len(x)), len(x)]
        x = g2.x; res[(h,"all")] = [x.mean(), x.mean()/x.std()*np.sqrt(len(x)), len(x)]
    out["horizon_signed_excess"] = pd.DataFrame(res, index=["mean","t","n"]).T
    # by trend profile at 5d
    g5 = B[(B.i % 5 == 0) & (B.forecast != 0)].dropna(subset=["f5"]).copy()
    m5 = B[B.i%5==0].groupby("coin").f5.mean()
    g5["x"] = np.sign(g5.forecast)*(g5.f5 - g5.coin.map(m5))
    g5["sd"] = np.where(g5.forecast>0,"long","short")
    gg = g5.groupby(["trend","sd"]).x
    out["5d_by_trend_side"] = pd.DataFrame({"mean": gg.mean(), "n": gg.size(), "t": gg.mean()/gg.std()*np.sqrt(gg.size())})
    # range position quintiles raw, 5d and 10d excess (not signed)
    g5["q"] = pd.qcut(g5.rp, 5, labels=False, duplicates="drop")
    g10 = B[(B.i % 10 == 0) & (B.forecast != 0)].dropna(subset=["f10"]).copy()
    m10 = B[B.i%10==0].groupby("coin").f10.mean()
    g10["e"] = g10.f10 - g10.coin.map(m10)
    g10["q"] = pd.qcut(g10.rp, 5, labels=False, duplicates="drop")
    g5["e"] = g5.f5 - g5.coin.map(m5)
    out["rp_quintile"] = pd.DataFrame({"rp_mean": g5.groupby("q").rp.mean(), "e5": g5.groupby("q").e.mean(),
        "n5": g5.groupby("q").size(), "e10": g10.groupby("q").e.mean(), "n10": g10.groupby("q").size()})
    out["rp_quintile_by_trend_e5"] = g5.groupby(["trend","q"]).e.mean().unstack()
    return out
