def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    daily = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r1 = b["close"].shift(-1)/b["close"]-1
            pos = b["postRebalance_current_allocation"].fillna(0)
            gain = pos*r1
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).clip(lower=0)/b["total_portfolio_value"]
            cl = b["close"]
            m30 = cl/cl.shift(720)-1
            w7 = cl/cl.shift(168)-1
            d1 = cl/cl.shift(24)-1
            hi30 = cl/cl.rolling(720, min_periods=200).max()-1
            vol = r1.shift(1).rolling(168).std()
            f24 = cl.shift(-24)/cl-1
            df = pd.DataFrame({"coin":c,"win":w,"pos":pos,"gain":gain,"fee":fee,"m30":m30,"w7":w7,"d1":d1,"hi30":hi30,"vol":vol,"f24":f24,"fc":b["forecast"],"yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
            d = data["days"][c][w][["day","book_return","coin_return"]].copy()
            d["coin"]=c; d["win"]=w; daily.append(d)
    A = pd.concat(rows, ignore_index=True)
    D = pd.concat(daily, ignore_index=True)
    out["gross_hourly_gain_mean"] = A["gain"].mean()
    out["fee_hourly_mean"] = A["fee"].mean()
    out["share_bars_long"] = (A["pos"]>0).mean()
    out["mean_pos_when_long"] = A.loc[A.pos>0,"pos"].mean()
    # book
    D["wn"] = D["win"].str[1:].astype(int)
    bk = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().reset_index().sort_values(["wn","day"])
    eq = (1+bk["book_return"]).cumprod()
    dd = eq/eq.cummax()-1
    bk["dd"]=dd.values
    out["book_maxdd"]=dd.min()
    # per window book stats
    pw = bk.groupby("wn").agg(book=("book_return","mean"),coin=("coin_return","mean"),mindd=("dd","min"),n=("book_return","size"))
    out["per_window"]=pw
    # gain by coin
    out["per_coin"]=A.groupby("coin").agg(gain=("gain","mean"),fee=("fee","mean"),long=("pos",lambda x:(x>0).mean()))
    # state buckets on 24h grid, long bars only
    G = A[(A.index % 24)==0].copy()
    G = G[G.pos>0].dropna(subset=["f24"])
    G["pg"]=G["pos"]*G["f24"]
    for v in ["m30","w7","d1","hi30","vol","fc"]:
        q = pd.qcut(G[v].rank(method="first"),5,labels=False)
        t = G.groupby(q)["pg"].agg(["mean","count","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["vmean"]=G.groupby(q)[v].mean()
        out["long_by_"+v]=t
    out["by_year"]=A.groupby("yr").agg(gain=("gain","mean"),fee=("fee","mean"),long=("pos",lambda x:(x>0).mean()))
    return out
