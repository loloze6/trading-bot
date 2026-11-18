def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    brows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy()
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1)/b["close"]-1
            g = pos*r1
            ret = b["close"].pct_change()
            vs = ret.rolling(20).std()
            z1 = ret/vs
            vol = b["volume"]/b["volume"].rolling(30).mean()
            # bars since forecast last >0
            f = b["forecast"].fillna(0)
            last = pd.Series(np.where(f>0, np.arange(len(f)), np.nan)).ffill().values
            since = np.arange(len(f)) - last
            r5 = b["close"].shift(-5)/b["close"]-1
            df = pd.DataFrame({"coin":c,"w":w,"pos":pos.values,"g":g.values,"r1":r1.values,
                               "f":f.values,"since":since,"z1":z1.values,"vol":vol.values,"r5":r5.values,
                               "fee_drop":(b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values,
                               "pos_i":np.arange(len(b))})
            rows.append(df)
        for w, d in data["days"][c].items():
            d = d.copy(); d["coin"]=c; d["w"]=w; brows.append(d)
    A = pd.concat(rows, ignore_index=True)
    D = pd.concat(brows, ignore_index=True)
    inpos = A[A.pos>0]
    out["exposure"] = pd.Series({"share bars long": (A.pos>0).mean(), "mean pos when long": inpos.pos.mean(),
                                 "mean gain per bar": A.g.mean(), "mean fee drop per bar": A.fee_drop.mean(),
                                 "coin mean r1": A.r1.mean()})
    # gain by bars since signal
    A["sb"] = A.since.clip(upper=6)
    t = A[A.pos>0].groupby("sb").agg(n=("g","size"), pos=("pos","mean"), r1=("r1","mean"), g=("g","mean"))
    out["by bars since last f>0 (long bars)"] = t
    # forward returns by forecast bucket, all bars, r1 and grid r5
    A["fb"] = pd.cut(A.f, [-0.01,0,0.5,2,5,20.1])
    out["r1 by forecast bucket"] = A.groupby("fb").agg(n=("r1","size"), r1=("r1","mean"), pos=("pos","mean"), g=("g","mean"))
    grid = A[A.pos_i%5==0]
    out["r5 grid by fb"] = grid.groupby("fb").agg(n=("r5","size"), r5=("r5","mean"))
    # book: daily returns by window
    bw = D.groupby("w").agg(book=("book_return","mean"), coin=("coin_return","mean"))
    bw["diff"]=bw.book-bw.coin
    out["by window"] = bw
    # market vs timing
    cm = D.groupby("coin").coin_return.mean()
    out["coin mean daily"] = cm
    # forecast>0 bars, z1 and 30d trend
    tr = data["trades"]
    T = pd.concat([tr[c][w].assign(coin=c) for c in tr for w in tr[c]], ignore_index=True)
    out["trades"] = pd.Series({"n":len(T),"mean pl":T.profit_loss_percent.mean(),"mean net":T.net_profit_loss_percent.mean(),
                               "mean dur days":T.duration_minutes.mean()/1440, "win":(T.net_profit_loss_percent>0).mean()})
    return out
