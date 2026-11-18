import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    allb = []
    for coin, ws in data["bars"].items():
        # coin mean daily return over all windows
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in ws]).dropna()
        cm = cr.mean()
        for w, b in ws.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1)/b["close"] - 1
            b["ret1"] = b["close"].pct_change()
            b["mad60"] = b["ret1"].abs().rolling(60, min_periods=20).mean()
            b["z"] = b["ret1"]/b["mad60"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["nxt"]
            b["coin"] = coin; b["win"] = w; b["cm"] = cm
            sd20 = b["ret1"].rolling(20).std()
            b["vr"] = sd20/sd20.rolling(100, min_periods=40).mean()
            b["ret5"] = b["close"]/b["close"].shift(5)-1
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            allb.append(b)
            d = data["days"][coin][w]
            rows.append(dict(coin=coin, win=w, book=d["book_return"].sum(), hold=d["coin_return"].sum(), n=len(d)))
    B = pd.concat(allb)
    per = pd.DataFrame(rows)
    out["per_window_sum"] = per.groupby("win")[["book","hold"]].sum()
    # book daily
    D = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            dd = d.copy(); dd["coin"]=coin; dd["win"]=w; D.append(dd)
    D = pd.concat(D)
    s = lambda x: x.mean()/x.std()*np.sqrt(365)
    out["sharpe"] = pd.DataFrame({"book":D.groupby("coin")["book_return"].apply(s),"hold":D.groupby("coin")["coin_return"].apply(s),
                                  "bookmean":D.groupby("coin")["book_return"].mean(),"holdmean":D.groupby("coin")["coin_return"].mean()})
    out["exposure_share"] = (B["pos"].abs()>1e-6).mean()
    out["mean_pos_when_in"] = B.loc[B["pos"].abs()>1e-6,"pos"].mean()
    B["mkt"] = B["pos"]*B["cm"]
    out["gain_split"] = pd.Series({"gain_mean":B["gain"].mean(),"market_part":B["mkt"].mean(),"timing":(B["gain"]-B["mkt"]).mean()})
    act = B[B["pos"].abs()>1e-6].dropna(subset=["nxt"])
    act["zb"] = pd.cut(-act["z"], [-np.inf,0,0.5,1,1.5,2,3,np.inf])
    g = act.groupby("zb")
    out["by_fall_z"] = pd.DataFrame({"n":g.size(),"nxt_mean":g["nxt"].mean(),"t":g["nxt"].apply(lambda x: x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan),
                                     "pos":g["pos"].mean(),"gain":g["gain"].mean()})
    act["vrb"] = pd.qcut(act["vr"], 4)
    g = act.groupby("vrb")
    out["by_volratio"] = pd.DataFrame({"n":g.size(),"nxt":g["nxt"].mean(),"gain":g["gain"].mean()})
    act["r20b"] = pd.qcut(act["ret20"], 4)
    g = act.groupby("r20b")
    out["by_ret20"] = pd.DataFrame({"n":g.size(),"nxt":g["nxt"].mean(),"gain":g["gain"].mean(),"t":g["nxt"].apply(lambda x: x.mean()/x.std()*np.sqrt(len(x)))})
    # all bars: next-day return by fall z, all regimes
    B2 = B.dropna(subset=["nxt","z"]).copy()
    B2["zb"] = pd.cut(-B2["z"], [-np.inf,0,0.5,1,1.5,2,3,np.inf])
    B2["inreg"] = B2["regime"]=="mean_reversion"
    out["all_bars_fall_by_regime"] = B2.groupby(["inreg","zb"])["nxt"].agg(["size","mean"])
    # trades
    T = pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"] = pd.Series({"n":len(T),"dur_days_mean":T["duration_minutes"].mean()/1440,"pl":T["profit_loss_percent"].mean(),"net":T["net_profit_loss_percent"].mean(),"comm":T["total_commission"].mean()})
    # turnover
    B["turn"] = (B["pos"]-B["previous_allocation"]).abs()
    out["turnover_mean"] = B["turn"].mean()
    out["pos_change_nonzero_share"] = (B["turn"]>1e-6).mean()
    return out
