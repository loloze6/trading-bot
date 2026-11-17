def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["r1"] = b.close.shift(-1)/b.close - 1
            b["r0"] = b.close/b.close.shift(1) - 1
            vol = b.r0.rolling(20).std()
            b["z"] = b.r0/vol
            b["r20p"] = b.close/b.close.shift(20)-1
            b["vol20"] = vol
            b["vol120m"] = vol.rolling(120, min_periods=40).median()
            b["vratio"] = b.vol20/b.vol120m
            b["coin"]=c; b["w"]=w; b["widx"]=int(w[1:])
            br.append(b)
    B = pd.concat(br, ignore_index=True)
    cm = B.groupby("coin").r0.mean()
    B["mu"] = B.coin.map(cm)
    a = B.postRebalance_current_allocation
    B["g"] = a*B.r1
    B["fee"] = (B.total_portfolio_value - B.postRebalance_total_value)/B.total_portfolio_value
    B["net"] = B.g - B.fee
    B["dalloc"] = (B.postRebalance_current_allocation - B.previous_allocation).abs()
    act = B[B.regime=="mean_reversion"].copy()
    act["side"] = np.sign(act.postRebalance_current_allocation)
    # side x z sign, net
    act["zs"] = np.where(act.z<0,"down","up")
    act["zq3"] = pd.qcut(act.z.abs(), 3, labels=["small","mid","large"])
    out["net_by_dir_size"] = act.groupby(["zs","zq3"]).agg(n=("g","size"), gross=("g","mean"), fee=("fee","mean"),
        net=("net","mean"), next_minus_mu=("r1", lambda x: (x - act.loc[x.index,"mu"]).mean()))
    # up large days by 20-day trend
    up = act[act.zs=="up"].copy()
    up["tr"] = pd.qcut(up.r20p, 3, labels=["low","mid","high"])
    out["up_days_by_trend"] = up.groupby(["tr","zq3"]).agg(n=("g","size"), net=("net","mean"),
        next_minus_mu=("r1", lambda x: (x - up.loc[x.index,"mu"]).mean()))
    # fees vs change size
    act["dq"] = pd.qcut(act.dalloc.rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["fee_by_change"] = act.groupby("dq").agg(dalloc=("dalloc","mean"), fee=("fee","mean"), gross=("g","mean"))
    # vol ratio level within active
    act["vq"] = pd.qcut(act.vratio, 4)
    out["by_volratio"] = act.groupby("vq").agg(n=("g","size"), gross=("g","mean"), net=("net","mean"))
    # drawdowns: book daily chain
    rows=[]
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dd["widx"]=int(w[1:]); rows.append(dd)
    D = pd.concat(rows)
    bk = D.groupby(["widx","day"])[["book_return","coin_return"]].mean().dropna().reset_index().sort_values(["widx","day"])
    eq = (1+bk.book_return).cumprod()
    dd = eq/eq.cummax()-1
    bk["dd"]=dd.values
    out["max_dd"] = float(dd.min())
    # drawdown episodes: book return on days in bottom 5% vs coin return
    q = bk.book_return.quantile(0.05)
    worst = bk[bk.book_return<=q]
    out["worst_days"] = pd.Series({"n":len(worst),"book":worst.book_return.mean(),"coin":worst.coin_return.mean(),
        "share_coin_up":(worst.coin_return>0).mean()})
    # book daily by coin daily return quintile
    bk["cq"]=pd.qcut(bk.coin_return,5)
    out["book_by_coin_day"] = bk.groupby("cq").agg(n=("book_return","size"), book=("book_return","mean"))
    # window-level drawdown in deepest window
    wdd = bk.groupby("widx").apply(lambda x: ((1+x.book_return).cumprod()/(1+x.book_return).cumprod().cummax()-1).min())
    out["window_maxdd"] = wdd.describe()
    return out
