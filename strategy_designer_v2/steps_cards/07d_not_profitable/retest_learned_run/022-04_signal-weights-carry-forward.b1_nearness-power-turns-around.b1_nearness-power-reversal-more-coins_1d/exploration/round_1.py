import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    days = data["days"]; bars = data["bars"]
    # windows in order
    wins = sorted({w for c in days for w in days[c]}, key=lambda s: int(s[1:]))
    # book daily returns: mean across coins per day within window
    rows = []
    for w in wins:
        frames = []
        for c in days:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        if not frames: continue
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna()
        g["win"] = w
        rows.append(g.reset_index())
    B = pd.concat(rows, ignore_index=True)
    B["eq"] = (1+B["book"]).cumprod()
    B["peak"] = B["eq"].cummax()
    B["dd"] = B["eq"]/B["peak"]-1
    # deepest falls: find top 3 drawdown episodes
    eps = []
    dd = B["dd"].values; i = 0; n = len(B)
    while i < n:
        if dd[i] < 0:
            j = i
            while j < n and dd[j] < 0: j += 1
            k = i + int(np.argmin(dd[i:j]))
            eps.append((dd[k], i, k, j))
            i = j
        else: i += 1
    eps = sorted(eps)[:5]
    ep_tab = []
    for (m, s, k, e) in eps:
        seg = B.iloc[max(s-1,0):k+1]
        ep_tab.append({"depth": m, "win_start": B.win.iloc[s], "win_trough": B.win.iloc[k],
                       "days_to_trough": k-s+1, "book_ret": (1+seg.book).prod()-1,
                       "hold_ret": (1+seg.hold).prod()-1, "year": str(B.day.iloc[k])[:4]})
    out["deepest_falls"] = pd.DataFrame(ep_tab)
    out["book_by_window"] = B.groupby("win", sort=False).agg(book_sum=("book","sum"), hold_sum=("hold","sum"), n=("book","size"))
    # per-bar position gains with conditions
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            r1 = b.close.shift(-1)/b.close-1
            a = b.postRebalance_current_allocation
            gain = a*r1
            ret30 = b.close/b.close.shift(30)-1
            ret5p = b.close/b.close.shift(5)-1
            hi90 = b.close.rolling(90, min_periods=30).max()
            near = b.close/hi90-1
            vol = b.close.pct_change().rolling(30).std()
            fwd5 = b.close.shift(-5)/b.close-1
            df = pd.DataFrame({"gain":gain,"a":a,"fc":b.forecast,"ret30":ret30,"ret5p":ret5p,
                               "near":near,"vol":vol,"r1":r1,"fwd5":fwd5})
            df["coin"]=c; df["win"]=w; df["pos"]=np.arange(len(b))
            recs.append(df)
    D = pd.concat(recs, ignore_index=True).dropna(subset=["gain"])
    D["side"] = np.sign(D.a)
    out["gain_by_side"] = D.groupby("side").gain.agg(["mean","count","std"])
    D["fcq"] = pd.qcut(D.fc.abs(), 4, labels=False, duplicates="drop")
    out["gain_by_absfc_q"] = D.groupby(["fcq"]).agg(gain=("gain","mean"), absa=("a",lambda x: x.abs().mean()), n=("gain","size"))
    D["trend"] = np.where(D.ret30>0, "up30", "down30")
    out["gain_side_trend"] = D.groupby(["side","trend"]).gain.agg(["mean","count"])
    D["volq"] = D.groupby("coin").vol.transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["gain_side_volq"] = D.groupby(["side","volq"]).gain.agg(["mean","count"])
    D["nearq"] = pd.qcut(D.near, 4, labels=False, duplicates="drop")
    out["gain_side_nearq"] = D.groupby(["side","nearq"]).gain.agg(["mean","count"])
    # grid 5-bar, signal times fwd5, by trend & side
    G = D[D.pos % 5 == 0].dropna(subset=["fwd5","ret30"])
    G["sg"] = np.sign(G.fc)*G.fwd5
    t = G.groupby(["side","trend"]).sg.agg(["mean","count","std"])
    t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["grid_signed5_side_trend"] = t
    out["book_stats"] = pd.Series({"mean":B.book.mean(),"std":B.book.std(),"maxdd":B.dd.min(),
                                   "share_long":(D.side>0).mean(),"share_short":(D.side<0).mean(),
                                   "mean_absalloc":D.a.abs().mean()})
    return out
