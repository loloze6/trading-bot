def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df[["timestamp","close","volume"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.reset_index(drop=True)
            c = d["close"].values.astype(float)
            n = len(c)
            def ret(k, fwd=False):
                r = np.full(n, np.nan)
                if fwd:
                    r[:n-k] = c[k:]/c[:n-k]-1
                else:
                    r[k:] = c[k:]/c[:-k]-1
                return r
            e = pd.DataFrame({"coin":coin,"w":w,
                "hour":((d["timestamp"]+pd.Timedelta(hours=1)).dt.hour).values,
                "wd":d["timestamp"].dt.weekday.values,
                "year":d["timestamp"].dt.year.values,
                "pos":np.arange(n)})
            for k in (2,8,24,72):
                e[f"p{k}"] = ret(k)
            for k in (2,8,24,72):
                e[f"f{k}"] = ret(k, True)
            lr = np.log(c[1:]/c[:-1]); lr = np.r_[np.nan, lr]
            e["vol24"] = pd.Series(lr).rolling(24).std().values
            e["vol720"] = pd.Series(lr).rolling(720, min_periods=200).std().values
            e["vrel"] = d["volume"].values/pd.Series(d["volume"].values).rolling(168,min_periods=48).median().values
            rows.append(e)
    E = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon, non-overlapping grid
    for k in (2,8,24,72):
        g = E[E.pos % k == 0].groupby("coin")[f"f{k}"].mean()
        E[f"x{k}"] = E[f"f{k}"] - E["coin"].map(g)
        E[f"z{k}"] = E[f"p{k}"] / (E["vol720"]*np.sqrt(k))
    # 1. By close hour: contrarian 2h after 2h pre-move, top quintile |z|
    res = []
    for h in range(24):
        s = E[(E.hour == h)].dropna(subset=["z2","x2"])
        q = s["z2"].abs() >= s["z2"].abs().quantile(0.8)
        cr = -np.sign(s["z2"])*s["x2"]
        t = cr.mean()/(cr.std()/np.sqrt(len(cr)))
        ct = cr[q]; tt = ct.mean()/(ct.std()/np.sqrt(len(ct)))
        res.append([h, len(cr), cr.mean()*100, t, ct.mean()*100, tt, s.loc[q,"x2"].abs().mean()*100])
    out["contrarian 2h by close hour (%, all; top quintile |z|)"] = pd.DataFrame(res, columns=["hour","n","mean_all","t_all","mean_topq","t_topq","absmove_topq"]).round(3)
    # 2. pre k / fwd h grid, all hours, non-overlapping on grid of max(k,h) and graded by quintile of z
    res = []
    for k in (2,8,24,72):
        for h in (2,8,24,72):
            m = max(k,h)
            s = E[E.pos % m == 0].dropna(subset=[f"z{k}",f"x{h}"])
            cr = -np.sign(s[f"z{k}"])*s[f"x{h}"]
            a = s[f"z{k}"].abs()
            top = cr[a >= a.quantile(0.9)]; bot = cr[a <= a.quantile(0.5)]
            tt = top.mean()/(top.std()/np.sqrt(len(top)))
            res.append([k,h,len(cr),cr.mean()*100, cr.mean()/(cr.std()/np.sqrt(len(cr))), top.mean()*100, tt, bot.mean()*100])
    out["contrarian pre k -> fwd h (top decile |z|)"] = pd.DataFrame(res, columns=["k","h","n","mean","t","top10_mean","top10_t","bot50_mean"]).round(3)
    # 3. 24h momentum/reversal by vol regime (vol720 tercile per coin)
    s = E[E.pos % 24 == 0].dropna(subset=["z24","x24","vol720"]).copy()
    s["vt"] = s.groupby("coin")["vol720"].transform(lambda v: pd.qcut(v,3,labels=False))
    s["cr"] = -np.sign(s["z24"])*s["x24"]
    s["big"] = s["z24"].abs() >= s["z24"].abs().quantile(0.8)
    g = s[s.big].groupby("vt")["cr"].agg(["count","mean","std"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"])); g["mean"]*=100
    out["contrarian 24h->24h big moves by vol tercile"] = g.round(3)
    # 4. volume spike graded: next 8h abs move vs vrel quintile, and directional after volume spike
    s = E[E.pos % 8 == 0].dropna(subset=["vrel","x8","z8"]).copy()
    s["vq"] = pd.qcut(s["vrel"],5,labels=False)
    s["cr"] = -np.sign(s["z8"])*s["x8"]
    g = s.groupby("vq")["cr"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"])); g["mean"]*=100
    out["contrarian 8h->8h by volume quintile"] = g.round(3)
    # 5. weekday and hour-of-day drift (1h forward, from 2h grid of 24)
    s = E[E.pos % 24 == 0].dropna(subset=["x24"])
    g = s.groupby("wd")["x24"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"])); g["mean"]*=100
    out["24h drift-removed by weekday"] = g.round(3)
    # 6. book: daily return by year and by coin
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            x = d[["day","book_return","coin_return"]].copy(); x["coin"]=coin; D.append(x)
    D = pd.concat(D); D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book daily by coin (%)"] = (D.groupby("coin")[["book_return","coin_return"]].mean()*100).round(4)
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    out["trades"] = pd.DataFrame({"n":[len(T)],"mean_gross":[T.profit_loss_percent.mean()],"mean_net":[T.net_profit_loss_percent.mean()],"med_dur_min":[T.duration_minutes.median()]}).round(4)
    return out
