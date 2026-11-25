def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["r60"] = b["close"]/b["close"].shift(60)-1
            lr = np.log(b["close"]).diff()
            b["vol10"] = lr.rolling(10).std()
            b["vol60"] = lr.rolling(60, min_periods=30).std()
            rng = b["high"]-b["low"]
            b["mult"] = rng/rng.shift(1).rolling(30, min_periods=20).mean()
            b["clv"] = (b["high"]-b["close"])/rng.replace(0,np.nan)
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["ret1"]
            b["coin"]=coin; b["w"]=w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["ret1"].transform("mean")
    B["ex"] = B["ret1"]-mu
    # book daily returns
    D=[]
    for coin, ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D)
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wn"]=bk["w"].str[1:].astype(int)
    bk=bk.sort_values(["wn","day"]).dropna()
    v=(1+bk["book_return"]).cumprod(); dd=v/v.cummax()-1
    bk["dd"]=dd.values
    out["book_dd_by_window"]=bk.groupby("wn").agg(book=("book_return","sum"),hold=("coin_return","sum"),mindd=("dd","min"),corr=("book_return",lambda s: np.nan))
    out["corr_book_hold"]=float(bk["book_return"].corr(bk["coin_return"]))
    out["beta_book_hold"]=float(np.polyfit(bk["coin_return"],bk["book_return"],1)[0])
    out["max_dd"]=float(dd.min())
    # position stats
    out["pos_desc"]=B["pos"].describe()
    out["fc_desc"]=B["forecast"].describe()
    # gain by forecast quintile
    B["fq"]=pd.qcut(B["forecast"].rank(method="first"),5,labels=False)
    g=B.dropna(subset=["ret1"]).groupby("fq")
    out["by_fq"]=pd.DataFrame({"fc":g["forecast"].mean(),"pos":g["pos"].mean(),"ex":g["ex"].mean(),"ret":g["ret1"].mean(),"gain":g["gain"].mean(),"n":g.size(),
        "t_ex":g["ex"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))})
    # by trend state of 20d return
    B["tr"]=pd.cut(B["r20"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    B["top"]=B["fq"]>=3
    g=B.dropna(subset=["ret1","tr"]).groupby(["tr","top"])
    out["by_trend_top"]=pd.DataFrame({"ret":g["ret1"].mean(),"ex":g["ex"].mean(),"gain":g["gain"].mean(),"pos":g["pos"].mean(),"n":g.size(),
        "t":g["ret1"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))})
    B["vr"]=B["vol10"]/B["vol60"]
    B["vq"]=pd.qcut(B["vr"],3,labels=False)
    g=B.dropna(subset=["ret1","vq"]).groupby(["vq","top"])
    out["by_volratio_top"]=pd.DataFrame({"ret":g["ret1"].mean(),"gain":g["gain"].mean(),"n":g.size(),
        "t":g["ret1"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))})
    # mult x clv grid
    B["mq"]=pd.qcut(B["mult"],3,labels=False); B["cq"]=pd.qcut(B["clv"],3,labels=False)
    g=B.dropna(subset=["ret1","mq","cq"]).groupby(["mq","cq"])
    out["grid_mult_clv"]=pd.DataFrame({"ret":g["ret1"].mean(),"n":g.size(),"t":g["ret1"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))})
    # gain on worst book days: share from low-forecast positions
    worst = bk.nsmallest(30,"book_return")[["w","day"]]
    W = B.merge(worst,on=["w","day"])
    out["worst30_days_prev_state"]=pd.Series({"mean_fc":W["forecast"].mean(),"mean_pos":W["pos"].mean(),"all_fc":B["forecast"].mean(),"all_pos":B["pos"].mean(),
        "mean_r20":W["r20"].mean(),"all_r20":B["r20"].mean(),"mean_vr":W["vr"].mean(),"all_vr":B["vr"].mean()})
    # gain share: low fc days
    B["fpos"]=B["forecast"]>0
    out["gain_split_top_vs_rest"]=B.dropna(subset=["gain"]).groupby("top")["gain"].agg(["mean","std","count"])
    return out
