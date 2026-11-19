import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df[["timestamp","close","volume","postRebalance_current_allocation"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.reset_index(drop=True)
            c = d["close"]
            d["r1"] = c.shift(-1)/c - 1
            d["r2"] = c.shift(-2)/c - 1
            d["r4"] = c.shift(-4)/c - 1
            d["r24f"] = c.shift(-24)/c - 1
            d["p24"] = c/c.shift(24) - 1
            d["p4"] = c/c.shift(4) - 1
            lr = np.log(c).diff()
            d["vol24"] = lr.rolling(24).std()
            d["vol_rel"] = d["volume"]/d["volume"].rolling(168, min_periods=48).median()
            d["hour"] = d["ts"].dt.hour
            d["wd"] = d["ts"].dt.weekday
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            # standardized past 24h return by coin-window using trailing vol
            d["z24"] = d["p24"] / (d["vol24"]*np.sqrt(24))
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # coin mean 1h return
    A["ex1"] = A["r1"] - A.groupby("coin")["r1"].transform("mean")
    A["ex2"] = A["r2"] - A.groupby("coin")["r2"].transform("mean")
    out = {}
    # hour of day mean excess 1h return (all bars non overlapping at h=1)
    g = A.dropna(subset=["ex1"]).groupby("hour")["ex1"]
    out["hour_ex1_bp"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    # hour of day relative volume
    out["hour_volrel"] = A.groupby("hour")["vol_rel"].median()
    # per hour: slope of next 2h excess return on z24 (one case per day per hour)
    res = []
    for h, s in A.dropna(subset=["ex2","z24"]).groupby("hour"):
        sl = stats.linregress(s["z24"], s["ex2"])
        res.append((h, sl.slope*1e4, sl.slope/sl.stderr, len(s)))
    out["hour_slope_ex2_on_z24"] = pd.DataFrame(res, columns=["hour","slope_bp","t","n"]).set_index("hour")
    # 24h grid: next 24h vs past 24h z, quintiles
    G = A[(A["pos"] % 24 == 0)].dropna(subset=["r24f","z24"]).copy()
    G["ex24"] = G["r24f"] - G.groupby("coin")["r24f"].transform("mean")
    G["q"] = pd.qcut(G["z24"], 5, labels=False)
    gg = G.groupby("q")["ex24"]
    out["daily_rev_by_z24_q"] = pd.DataFrame({"mean_bp": gg.mean()*1e4, "t": gg.mean()/(gg.std()/np.sqrt(gg.count())), "n": gg.count()})
    # 1h: after big 1h move (|z|) next 1h, by sign quintile of last 1h return z
    A["z1"] = np.log(A["close"]).groupby([A["coin"],A["win"]]).diff() / A["vol24"]
    B = A.dropna(subset=["z1","ex1"]).copy()
    B["q"] = pd.qcut(B["z1"], 10, labels=False)
    gb = B.groupby("q")["ex1"]
    out["next1h_by_last1h_decile"] = pd.DataFrame({"mean_bp": gb.mean()*1e4, "t": gb.mean()/(gb.std()/np.sqrt(gb.count())), "n": gb.count()})
    # weekday
    gw = A.dropna(subset=["ex1"]).groupby("wd")["ex1"]
    out["wd_ex1_bp"] = pd.DataFrame({"mean_bp": gw.mean()*1e4, "t": gw.mean()/(gw.std()/np.sqrt(gw.count()))})
    return out
