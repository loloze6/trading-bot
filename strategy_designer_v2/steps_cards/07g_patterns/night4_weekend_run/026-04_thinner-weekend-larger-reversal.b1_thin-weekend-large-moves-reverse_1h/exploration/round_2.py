def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    tf = lambda x: x.mean()/x.std()*np.sqrt(len(x))
    rows = []; hrows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close"]].reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"].values; n = len(c)
            lr = np.full(n, np.nan); lr[1:] = np.log(c[1:]/c[:-1])
            for h in (12,24,48):
                pos = np.arange(h, n-h, h)
                if len(pos)==0: continue
                past = c[pos]/c[pos-h]-1; fut = c[pos+h]/c[pos]-1
                rv = np.array([np.nanstd(lr[max(1,p-23):p+1]) for p in pos])
                rv7 = np.array([np.nanstd(lr[max(1,p-167):p+1]) for p in pos])
                rows.append(pd.DataFrame({"coin":coin,"w":w,"h":h,"past":past,"fut":fut,"rv":rv,"rv7":rv7,
                                          "year":ts.dt.year.values[pos]}))
            # 20-22 UTC block return per day: close at hour 22 start / close at hour 19 start -> covers bars 20,21 returns? use close[t at hour 21]/close[t at hour 19]
            hh = ts.dt.hour.values
            i19 = np.where(hh==19)[0]
            for i in i19:
                if i+2 < n and hh[i+2]==21:
                    hrows.append((coin, w, ts.dt.year.values[i], ts.dt.weekday.values[i], c[i+2]/c[i]-1,
                                  np.nanstd(lr[max(1,i-23):i+1])))
    M = pd.concat(rows).dropna()
    # drift per coin per h
    M["drift"] = M.groupby(["coin","h"])["fut"].transform("mean")
    M["usual"] = M.groupby(["coin","h"])["fut"].transform("std")
    M["against"] = -np.sign(M["past"])*(M["fut"]-M["drift"])
    M["total_against"] = -np.sign(M["past"])*M["fut"]
    M["zp"] = M["past"]/M.groupby(["coin","h"])["past"].transform("std")
    M["zf"] = (M["fut"]-M["drift"])/M["usual"]
    M["vq"] = M.groupby(["coin","h"])["rv"].transform(lambda x: pd.qcut(x,5,labels=False))
    t=[]
    for (h,q),g in M.groupby(["h","vq"]):
        r = stats.linregress(g["zp"],g["zf"])
        t.append((h,q,r.slope,r.slope/r.stderr,len(g),g["against"].mean(),g["total_against"].mean(),(g["against"]/g["usual"]).mean()))
    out["slope_by_h_volquintile"] = pd.DataFrame(t,columns=["h","volq","slope","t","n","unusual_against","total_against","strength"])
    # top vol quintile, 24h: by |zp| tercile
    g = M[(M.h==24)&(M.vq==4)].copy()
    g["aq"] = pd.qcut(g["zp"].abs(),3,labels=False)
    a = g.groupby("aq")["against"].agg(["mean","count",tf]); a.columns=["unusual_against","n","t"]
    out["h24_topvol_by_absmove_tercile"]=a
    # robustness by year and coin, h24 top 2 vol quintiles
    g2 = M[(M.h==24)&(M.vq>=3)]
    t=[]
    for key,gg in list(g2.groupby("year"))+list(g2.groupby("coin")):
        r = stats.linregress(gg["zp"],gg["zf"]); t.append((str(key),r.slope,r.slope/r.stderr,len(gg),gg["against"].mean()))
    out["h24_highvol_by_year_coin"]=pd.DataFrame(t,columns=["group","slope","t","n","unusual_against"])
    # relative vol (24h vol over 7d vol) as grading
    M["relv"] = M["rv"]/M["rv7"]
    M["rq"] = M.groupby(["coin","h"])["relv"].transform(lambda x: pd.qcut(x,5,labels=False))
    t=[]
    for q,gg in M[M.h==24].groupby("rq"):
        r = stats.linregress(gg["zp"],gg["zf"]); t.append((q,r.slope,r.slope/r.stderr,len(gg),gg["against"].mean()))
    out["h24_by_relvol_quintile"]=pd.DataFrame(t,columns=["relvq","slope","t","n","unusual_against"])
    # 20-21 UTC
    H = pd.DataFrame(hrows,columns=["coin","w","year","wd","r","rv"])
    t=[]
    for key,gg in list(H.groupby("year"))+list(H.groupby("coin"))+list(H.groupby("wd")):
        t.append((str(key),gg["r"].mean(),tf(gg["r"]),len(gg)))
    out["ret_19to21close_by_year_coin_wd"]=pd.DataFrame(t,columns=["group","mean","t","n"])
    H["vq"]=H.groupby("coin")["rv"].transform(lambda x: pd.qcut(x,3,labels=False))
    a=H.groupby("vq")["r"].agg(["mean","count",tf]); a.columns=["mean","n","t"]
    out["ret_20_21_by_vol_tercile"]=a
    return out
