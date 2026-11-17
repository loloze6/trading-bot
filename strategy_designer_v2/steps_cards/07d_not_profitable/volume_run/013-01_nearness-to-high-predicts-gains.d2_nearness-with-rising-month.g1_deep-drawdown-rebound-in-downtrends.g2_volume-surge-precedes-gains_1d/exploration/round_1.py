def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    windows = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    out = {}
    # book daily = mean over coins of book_return per day, within window
    rows = []
    for w in windows:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c; frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day")[["book_return","coin_return"]].mean().dropna()
        g["window"] = w
        rows.append(g)
    book = pd.concat(rows)
    eq = (1+book["book_return"]).cumprod()
    dd = eq/eq.cummax()-1
    book["dd"] = dd.values
    hold_eq = (1+book["coin_return"]).cumprod()
    hdd = hold_eq/hold_eq.cummax()-1
    n = len(book)
    yr = eq.iloc[-1]**(365/n)-1
    out["summary"] = pd.Series({"n_days":n,"yearly":yr,"maxdd":dd.min(),"calmar":yr/abs(dd.min()),
        "hold_yearly":hold_eq.iloc[-1]**(365/n)-1,"hold_maxdd":hdd.min(),
        "book_mean":book.book_return.mean(),"book_sd":book.book_return.std(),"hold_sd":book.coin_return.std()})
    # per window
    pw = book.groupby("window").agg(book_ret=("book_return",lambda x:(1+x).prod()-1),
                                    hold_ret=("coin_return",lambda x:(1+x).prod()-1),
                                    min_dd=("dd","min"))
    pw = pw.loc[windows]
    out["per_window"] = pw
    # per coin per-bar: allocation vs state
    recs=[]
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].copy()
            cl = b["close"]
            r1 = cl.pct_change()
            fwd = cl.shift(-1)/cl-1
            pos = b["postRebalance_current_allocation"]
            ret20 = cl/cl.shift(20)-1
            ret60 = cl/cl.shift(60)-1
            hi60 = b["high"].rolling(60,min_periods=20).max()
            near = cl/hi60-1
            vr = b["volume"]/b["volume"].rolling(20,min_periods=10).mean()
            vol20 = r1.rolling(20).std()
            recs.append(pd.DataFrame({"coin":c,"window":w,"pos":pos,"g":pos*fwd,"fwd":fwd,"r1":r1,
                "ret20":ret20,"ret60":ret60,"near":near,"vr":vr,"vol20":vol20,"fc":b["forecast"]}))
    A = pd.concat(recs).dropna(subset=["g"])
    out["pos_stats"] = A["pos"].describe()
    def bucket(col,q=5):
        x=A.dropna(subset=[col]).copy()
        x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("g","size"),mean_pos=("pos","mean"),
                    mean_gain=("g","mean"),sd_gain=("g","std"),mean_fwd=("fwd","mean"),
                    worst_gain_sum=("g",lambda s:s[s<0].sum()))
    out["by_ret20"]=bucket("ret20")
    out["by_ret60"]=bucket("ret60")
    out["by_near"]=bucket("near")
    out["by_vol20"]=bucket("vol20")
    out["by_vr"]=bucket("vr")
    out["by_r1"]=bucket("r1")
    return out
