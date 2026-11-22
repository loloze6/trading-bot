import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume","forecast","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            d["ret1"] = d["close"].pct_change()
            d["ma"] = d["ret1"].abs().rolling(720, min_periods=240).mean()
            d["z"] = d["ret1"] / d["ma"]
            d["vr"] = d["volume"] / d["volume"].rolling(720, min_periods=240).mean()
            for h in (1,2,4,6):
                d[f"f{h}"] = d["close"].shift(-h)/d["close"] - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            ts = pd.to_datetime(d["timestamp"], utc=True)
            d["hour"] = ts.dt.hour; d["wd"] = ts.dt.weekday; d["year"] = ts.dt.year
            d["vol24"] = d["ret1"].rolling(24).std()
            d["vq"] = d["vol24"] / d["ret1"].rolling(720, min_periods=240).std()
            d["mom24"] = d["close"]/d["close"].shift(24)-1
            d["mom24z"] = d["mom24"]/(d["ma"]*np.sqrt(24))
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin per h
    drift = {h: A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean() for h in (1,2,4,6)}
    for h in (1,2,4,6):
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(drift[h])
    def tab(sub, h, key):
        s = sub[sub.pos % h == 0].dropna(subset=[f"x{h}", key])
        g = s.groupby(key, observed=True)[f"x{h}"]
        r = pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))})
        return r.round(2)
    A["zb"] = pd.cut(A["z"], [-np.inf,-4,-2.5,-1.5,1.5,2.5,4,np.inf])
    A["vb"] = pd.cut(A["vr"], [0,0.8,1.25,2,3,np.inf])
    # signed continuation: direction-signed fwd return for |z|>2.5 by volume bin
    for h in (2,4,6):
        s = A[(A.pos % h == 0) & (A.z.abs() > 2.5)].dropna(subset=[f"x{h}","vb"]).copy()
        s["sx"] = np.sign(s.z)*s[f"x{h}"]
        g = s.groupby("vb", observed=True)["sx"]
        out[f"big move signed cont h{h} by vol"] = pd.DataFrame({"n":g.size(),"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    out["h2 by z bin"] = tab(A, 2, "zb")
    out["h6 by z bin"] = tab(A, 6, "zb")
    out["h1 by hour"] = tab(A, 1, "hour")
    out["h1 by weekday"] = tab(A, 1, "wd")
    # 24h momentum z quintile -> 6h
    A["mq"] = pd.qcut(A["mom24z"], 5, labels=False, duplicates="drop")
    out["h6 by 24h mom quintile"] = tab(A, 6, "mq")
    A["volq"] = pd.qcut(A["vq"], 4, labels=False, duplicates="drop")
    s = A[(A.pos % 2 == 0)&(A.z.abs()>2)].dropna(subset=["x2","volq"]).copy(); s["sx"]=np.sign(s.z)*s.x2
    g = s.groupby("volq")["sx"]
    out["|z|>2 signed h2 by vol regime"] = pd.DataFrame({"n":g.size(),"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    # book
    D = pd.concat([df.assign(coin=c, win=w) for c, ws in data["days"].items() for w, df in ws.items()])
    out["book daily by coin"] = D.groupby("coin")[["book_return","coin_return"]].mean().mul(1e4).round(2)
    tr = pd.concat([df.assign(coin=c) for c, ws in data["trades"].items() for w, df in ws.items()])
    out["trades"] = tr.groupby("coin").agg(n=("side","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur=("duration_minutes","median")).round(3)
    return out
