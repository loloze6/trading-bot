def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    # book daily returns: mean across coins per day within window
    rows = []
    for c in coins:
        for w, d in data["days"][c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    book = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    out["book_mean_std"] = pd.Series({"book_mean":book.book_return.mean(),"book_std":book.book_return.std(),
        "hold_mean":book.coin_return.mean(),"hold_std":book.coin_return.std(),"ndays":len(book)})
    # per window book vs hold
    pw = book.groupby(level=0).agg(book_mean=("book_return","mean"),hold_mean=("coin_return","mean"),n=("book_return","size"))
    pw["book_sum"]=pw.book_mean*pw.n; pw["hold_sum"]=pw.hold_mean*pw.n
    out["per_window"]=pw.round(5)
    # drawdown of chained book
    eq = (1+book.book_return).cumprod()
    dd = eq/eq.cummax()-1
    out["maxdd"]=float(dd.min())
    # dd per window contribution: worst windows sum
    # bar level: position, gain, fee; decompose market vs timing
    brs=[]
    for c in coins:
        mu_all = []
        for w,b in data["bars"][c].items():
            r = b["close"].shift(-1)/b["close"]-1
            mu_all.append(r.dropna())
        mu = pd.concat(mu_all).mean()
        for w,b in data["bars"][c].items():
            x = b[["close","forecast","postRebalance_current_allocation","total_portfolio_value","postRebalance_total_value","high","low","volume"]].copy()
            x["r1"]=x.close.shift(-1)/x.close-1
            x["pos"]=x.postRebalance_current_allocation
            x["gain"]=x.pos*x.r1
            x["mkt"]=x.pos*mu
            x["fee"]=(x.total_portfolio_value-x.postRebalance_total_value)/x.total_portfolio_value
            x["coin"]=c; x["wn"]=int(w[1:])
            # 72h forward
            x["f72"]=x.close.shift(-72)/x.close-1
            x["ret240"]=x.close/x.close.shift(240)-1
            x["vol24"]=x.r1.shift(1).rolling(24).std()
            x["vol480"]=x.r1.shift(1).rolling(480).std()
            brs.append(x)
    B=pd.concat(brs)
    out["bar_decomp"]=pd.Series({"gain_mean_bar":B.gain.mean(),"mkt_part":B.mkt.mean(),"timing":B.gain.mean()-B.mkt.mean(),
        "fee_mean_bar":B.fee.mean(),"share_bars_long":(B.pos>0).mean(),"mean_pos":B.pos.mean(),"mean_pos_when_long":B.pos[B.pos>0].mean()})
    # by forecast bucket: gain per bar vs coin r1
    L=B[B.pos>0].copy()
    L["fq"]=pd.qcut(L.forecast.rank(method="first"),5,labels=False)
    g=L.groupby("fq").agg(n=("r1","size"),fc=("forecast","mean"),pos=("pos","mean"),r1=("r1","mean"),gain=("gain","mean"),fee=("fee","mean"))
    g["r1_t"]=L.groupby("fq").r1.apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))
    out["long_by_fq"]=g
    out["flat_r1"]=pd.Series({"flat_r1_mean":B.r1[B.pos==0].mean(),"long_r1_mean":L.r1.mean(),"all_r1":B.r1.mean()})
    # non-overlapping 72 grid excess by ratio vol24/vol480 among long
    G=[]
    for (c,w),x in B.groupby(["coin","wn"]):
        G.append(x.iloc[::72])
    G=pd.concat(G).dropna(subset=["f72"])
    mu72=G.groupby("coin").f72.mean()
    G["ex"]=G.f72-G.coin.map(mu72)
    GL=G[G.forecast>0].copy()
    GL["vr"]=GL.vol24/GL.vol480
    GL["vq"]=pd.qcut(GL.vr,4,labels=False)
    out["grid_long_by_volratio"]=GL.groupby("vq").agg(n=("ex","size"),ex=("ex","mean"),vr=("vr","mean"),t=("ex",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    GL["mq"]=pd.qcut(GL.ret240,4,labels=False)
    out["grid_long_by_ret240"]=GL.groupby("mq").agg(n=("ex","size"),ex=("ex","mean"),r240=("ret240","mean"),t=("ex",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    out["grid_flat_ex"]=pd.Series({"n":int((G.forecast==0).sum()),"ex":G.ex[G.forecast==0].mean()})
    # trades
    T=pd.concat([t.assign(coin=c) for c in coins for w,t in data["trades"][c].items()])
    out["trades"]=pd.Series({"n":len(T),"mean_pl":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean(),
        "med_dur_h":T.duration_minutes.median()/60,"sum_comm":T.total_commission.sum()})
    return out
