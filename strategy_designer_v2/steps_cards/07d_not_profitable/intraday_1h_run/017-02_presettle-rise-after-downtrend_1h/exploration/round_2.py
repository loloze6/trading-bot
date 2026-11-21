import numpy as np, pandas as pd
def explore(data):
    out = {}
    eps = []
    days = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            ts = pd.to_datetime(b["timestamp"]); h = ts.dt.hour
            c = b["close"]
            ch72 = c/c.shift(72)-1
            z = (ch72 - ch72.rolling(72, min_periods=20).mean())/ch72.rolling(72, min_periods=20).std()
            d = pd.DataFrame({"coin":coin,"h":h,"z":z,"ch72":ch72,"fc":b["forecast"],
                              "r2":c.shift(-2)/c-1,"r1a":c.shift(-1)/c-1,"r1b":c.shift(-2)/c.shift(-1)-1,
                              "r6":c.shift(-6)/c-1,"r24":c.shift(-24)/c-1,
                              "pre2":c/c.shift(2)-1})
            eps.append(d[d["h"].isin([5,13,21])])
        for w, dd in data["days"][coin].items():
            days.append(dd.assign(coin=coin))
    E = pd.concat(eps)
    E["fall"] = E["ch72"]<0
    def tt(x): x=x.dropna(); return x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan
    g = E.groupby(["h","fall"]).agg(n=("r2","count"),r2=("r2","mean"),r1a=("r1a","mean"),r1b=("r1b","mean"),r6=("r6","mean"),r24=("r24","mean"))
    g["t_r2"]=E.groupby(["h","fall"])["r2"].apply(tt)
    out["episodes by hour and 3d sign"]=g
    F = E[E["fc"]>0].copy()
    F["q"]=pd.qcut(F["fc"],5,labels=False,duplicates="drop")
    q = F.groupby("q").agg(n=("r2","count"),fc=("fc","mean"),ch72=("ch72","mean"),r2=("r2","mean"),r6=("r6","mean"),r24=("r24","mean"),pre2=("pre2","mean"))
    q["t_r2"]=F.groupby("q")["r2"].apply(tt); q["t_r24"]=F.groupby("q")["r24"].apply(tt)
    out["active episodes by forecast quintile"]=q
    E["qa"]=pd.qcut(E["ch72"],5,labels=False)
    qa = E.groupby("qa").agg(n=("r2","count"),ch72=("ch72","mean"),r2=("r2","mean"),r6=("r6","mean"),r24=("r24","mean"))
    qa["t_r2"]=E.groupby("qa")["r2"].apply(tt)
    out["all episodes by raw 3d change quintile"]=qa
    D = pd.concat(days)
    out["daily book"]=pd.DataFrame({"mean_book":[D["book_return"].mean()],"mean_coin":[D["coin_return"].mean()],
        "n":[D["book_return"].count()]})
    return out
