def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; prow = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            if n < 200: continue
            lr = np.log(c)
            ret1 = pd.Series(np.r_[np.nan, np.diff(lr)])
            sd1 = ret1.rolling(168).std()
            vol = sd1*np.sqrt(24)
            vol30 = ret1.rolling(720).std()*np.sqrt(24)
            z = pd.Series(lr).diff(24)/vol
            p1 = ret1/sd1
            ts = pd.to_datetime(b["timestamp"])
            hr = ts.dt.hour.values; yr = ts.dt.year.values
            pos = b["postRebalance_current_allocation"].values
            r1f = np.r_[c[1:]/c[:-1]-1, np.nan]
            for i in range(n):
                prow.append((coin, w, pos[i]*r1f[i], vol.iloc[i], pos[i]))
            fwd24 = np.r_[lr[24:]-lr[:-24], [np.nan]*24]
            for i in range(0, n, 24):
                rows.append((coin, w, yr[i], z.iloc[i], fwd24[i], vol.iloc[i], vol.iloc[i]/vol30.iloc[i] if vol30.iloc[i]>0 else np.nan))
            fwd1 = np.r_[lr[1:]-lr[:-1], np.nan]
            if w == list(wins.keys())[0]: pass
            b2 = pd.DataFrame({"coin":coin,"w":w,"yr":yr,"hr":hr,"p1":p1.values,"f1":fwd1})
            rows_h = b2
            out.setdefault("_h", []).append(rows_h)
    T = lambda x: x.mean()/x.std()*np.sqrt(len(x))
    df = pd.DataFrame(rows, columns=["coin","w","yr","z","fwd","vol","vratio"]).dropna()
    df["fwd"] -= df.groupby("coin")["fwd"].transform("mean")
    df["s"] = -df["z"]*df["fwd"]
    df["vq"] = df.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False))
    df["rq"] = df.groupby("coin")["vratio"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["rev24_z_by_vol_coin_t"] = df.groupby(["coin","vq"])["s"].apply(T).unstack()
    out["rev24_z_by_vol_year_t"] = df.groupby(["yr","vq"])["s"].apply(T).unstack()
    out["rev24_by_volratio"] = df.groupby("rq")["s"].agg(["size","mean",T])
    hv = df[df.vq==2].copy(); hv["zq"]=pd.qcut(hv["z"],5,labels=False)
    out["highvol_zquint_fwd"] = hv.groupby("zq").agg(n=("fwd","size"),z=("z","mean"),fwd=("fwd","mean"),t=("fwd",T))
    lv = df[df.vq==0].copy(); lv["zq"]=pd.qcut(lv["z"],5,labels=False)
    out["lowvol_zquint_fwd"] = lv.groupby("zq").agg(n=("fwd","size"),z=("z","mean"),fwd=("fwd","mean"),t=("fwd",T))
    P = pd.DataFrame(prow, columns=["coin","w","g","vol","pos"]).dropna()
    P["vq"] = P.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["book_gross_by_vol"] = P.groupby("vq").agg(g=("g","mean"),abspos=("pos",lambda x: x.abs().mean()))
    H = pd.concat(out.pop("_h")).dropna()
    H["f1"] -= H.groupby("coin")["f1"].transform("mean")
    H["s"] = -H["p1"]*H["f1"]
    H["pq"] = pd.qcut(H["p1"].abs(),5,labels=False)
    out["rev1h_by_absmove_quint"] = H.groupby("pq").agg(n=("s","size"),absp=("p1",lambda x:x.abs().mean()),s=("s","mean"),t=("s",T))
    out["rev1h_t_by_coin_year"] = H.groupby(["coin","yr"])["s"].apply(T).unstack()
    hh = H[H.hr.isin([13,20,21])]
    out["hour_ret_t_coin"] = hh.groupby(["coin","hr"])["f1"].apply(T).unstack()
    out["hour_ret_t_year"] = hh.groupby(["yr","hr"])["f1"].apply(T).unstack()
    return out
