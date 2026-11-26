import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    coin_mean14 = {}
    coin_mean1 = {}
    for c, ws in bars.items():
        r14 = []; r1 = []
        for w, b in ws.items():
            cl = b["close"].values
            n = len(cl)
            for i in range(0, n - 14, 14):
                r14.append(cl[i+14]/cl[i]-1)
            r1 += list(cl[1:]/cl[:-1]-1)
        coin_mean14[c] = np.mean(r14) if r14 else np.nan
        coin_mean1[c] = np.mean(r1)
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            lr = cl.pct_change()
            sd30 = lr.rolling(30, min_periods=20).std()
            s7 = (cl/cl.shift(7)-1)/(sd30*np.sqrt(7))
            s1 = lr/sd30
            ret60 = cl/cl.shift(60)-1
            f14 = cl.shift(-14)/cl-1
            f3 = cl.shift(-3)/cl-1
            rng = (b["high"]-b["low"])/cl
            clv = (cl-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n-14, 14):
                rows.append(dict(coin=c, win=w, i=i, day=ts[i].normalize(), regime=b["regime"][i],
                                 s7=s7[i], s1=s1[i], ret60=ret60[i], sd30=sd30[i],
                                 x14=f14[i]-coin_mean14[c], f14=f14[i], fc=b["forecast"][i],
                                 clv=clv[i], wd=ts[i].dayofweek, year=ts[i].year))
    g = pd.DataFrame(rows).dropna(subset=["x14"])
    out = {}
    out["regime counts"] = g["regime"].value_counts()
    def tab(d, col, q=5):
        d = d.dropna(subset=[col]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        a = d.groupby("b").agg(n=("x14","size"), lo=(col,"min"), hi=(col,"max"), mx14=("x14","mean"), sd=("x14","std"))
        a["t"] = a["mx14"]/(a["sd"]/np.sqrt(a["n"]))
        return a.round(4)
    inp = g[g.regime=="unknown"]; outp = g[g.regime!="unknown"]
    out["in profile: x14 by s7 quintile"] = tab(inp, "s7")
    out["out profile: x14 by s7 quintile"] = tab(outp, "s7")
    out["all: x14 by s7 quintile"] = tab(g, "s7")
    out["all: x14 by ret60 quintile"] = tab(g, "ret60")
    out["all: x14 by sd30 quintile"] = tab(g, "sd30")
    out["all: x14 by s1 quintile"] = tab(g, "s1")
    out["all: x14 by close-location quintile"] = tab(g, "clv")
    # trend buckets x s7 sign
    g["trend"] = np.where(g.ret60>0.10,"rising",np.where(g.ret60<-0.10,"falling","choppy"))
    g["s7q"] = pd.qcut(g["s7"],3,labels=["low","mid","high"])
    a = g.groupby(["trend","s7q"]).agg(n=("x14","size"), mx14=("x14","mean"), sd=("x14","std"))
    a["t"] = a["mx14"]/(a["sd"]/np.sqrt(a["n"]))
    out["trend x s7 tercile"] = a.round(4)
    # daily: weekday and after large moves, all bars
    d_rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; lr = cl.pct_change(); sd30 = lr.rolling(30,min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            d_rows.append(pd.DataFrame(dict(coin=c, wd=ts.dt.dayofweek, s1=lr/sd30,
                 nx=lr.shift(-1)-coin_mean1[c], alloc=b["postRebalance_current_allocation"],
                 regime=b["regime"])))
    dd = pd.concat(d_rows).dropna(subset=["nx"])
    a = dd.groupby("wd")["nx"].agg(["size","mean","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["size"]))
    out["next-day excess by weekday"] = a.round(5)
    out["next-day excess by s1 decile"] = tab(dd.rename(columns={"nx":"x14"}), "s1", 10)
    # book
    br = []
    for c, ws in days.items():
        for w, d in ws.items():
            br.append(d.assign(coin=c, win=w))
    bd = pd.concat(br).dropna(subset=["book_return"])
    bd["year"] = pd.to_datetime(bd["day"]).dt.year
    a = bd.groupby("year").agg(n=("book_return","size"), book=("book_return","mean"), coin=("coin_return","mean"))
    out["book by year"] = a
    a = bd.groupby("coin").agg(n=("book_return","size"), book=("book_return","mean"), coin=("coin_return","mean"))
    out["book by coin"] = a
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=c))
    if tr:
        T = pd.concat(tr)
        T["efq"] = pd.qcut(T["entry_forecast"],4,labels=False,duplicates="drop")
        out["trades by entry forecast quartile"] = T.groupby("efq").agg(n=("net_profit_loss_percent","size"),
             ef=("entry_forecast","mean"), pnl=("net_profit_loss_percent","mean"), win=("net_profit_loss_percent", lambda x:(x>0).mean())).round(3)
    return out
