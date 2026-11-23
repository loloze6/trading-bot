import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []; grid = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            b["nret"] = b["close"].shift(-1)/b["close"] - 1
            b["ret1"] = b["close"].pct_change()
            rng = (b["high"]-b["low"])/b["close"]
            b["rr"] = rng / rng.rolling(30, min_periods=20).mean()
            b["f3"] = b["close"].shift(-3)/b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"]*b["nret"]
            b["coin"] = c; b["win"] = w; b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["prev_pos"] = b["pos"].shift(1)
            rows.append(b)
            grid.append(b.iloc[::3])
    A = pd.concat(rows); G = pd.concat(grid)
    m3 = G.groupby("coin")["f3"].mean()
    G["ex3"] = G["f3"] - G["coin"].map(m3)
    out = {}
    A["side"] = np.sign(A["pos"]).map({1:"long",-1:"short",0:"flat"})
    out["gain_by_side"] = A.groupby("side")["g"].agg(["count","mean","sum"])
    A["fcat"] = pd.cut(A["forecast"], [-21,-2,-0.01,0.01,2,4,21])
    out["gain_by_forecast_held"] = A.groupby("fcat")["g"].agg(["count","mean","sum"])
    A["ab"] = A["pos"].abs()
    out["mean_abs_pos"] = A["ab"].mean()
    # falling vs rising days by range ratio
    G["fall"] = G["ret1"] < 0
    G["rrq"] = pd.qcut(G["rr"], 5, labels=False)
    t = G.groupby(["fall","rrq"])["ex3"].agg(["count","mean"])
    t["t"] = G.groupby(["fall","rrq"])["ex3"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
    out["ex3_by_fall_rrquint"] = t
    # depth of fall (ret1 size) on falling days with wide range
    F = G[G["fall"]].copy()
    F["dq"] = pd.qcut(F["ret1"], 4, labels=False)
    out["fall_ex3_by_fallsizeq_x_wide"] = F.groupby(["dq", F["rr"]>1])["ex3"].agg(["count","mean"])
    # prior trend: 30-day return
    # book daily by year, drawdown
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"]=c; d["win"]=w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna().reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int); bk = bk.sort_values(["wn","day"])
    v = (1+bk["book_return"]).cumprod(); dd = v/v.cummax()-1
    bk["dd"] = dd.values
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"] = bk.groupby("year").agg(book=("book_return","sum"), coin=("coin_return","sum"), mindd=("dd","min"))
    out["book_by_window"] = bk.groupby("wn").agg(book=("book_return","sum"), coin=("coin_return","sum"))
    out["maxdd"] = float(dd.min())
    # gain by year side
    out["gain_year_side"] = A.groupby(["year","side"])["g"].sum().unstack()
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades_side"] = T.groupby("side")[["profit_loss_percent","net_profit_loss_percent"]].agg(["count","mean"])
    return out
