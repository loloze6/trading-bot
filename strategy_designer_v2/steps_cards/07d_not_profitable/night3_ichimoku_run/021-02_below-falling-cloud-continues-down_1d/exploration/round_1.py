import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    H = 26
    # coin mean 26-bar return on grid
    rows = []
    for coin in bars:
        allr = []
        for w, b in bars[coin].items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i+H]/c[i]-1)
        mu = np.mean(allr); sd = np.std(allr)
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            tenkan = (hi.rolling(9).max()+lo.rolling(9).min())/2
            kijun = (hi.rolling(26).max()+lo.rolling(26).min())/2
            sa = ((tenkan+kijun)/2).shift(26)
            sb = ((hi.rolling(52).max()+lo.rolling(52).min())/2).shift(26)
            bottom = np.minimum(sa, sb); top = np.maximum(sa, sb)
            mid = (sa+sb)/2
            thick = (top-bottom)/c
            dist = (c-bottom)/c
            r26p = c/c.shift(26)-1
            r7p = c/c.shift(7)-1
            r90p = c/c.shift(90)-1
            vol = c.pct_change().rolling(30).std()
            f = b["forecast"]
            for i in range(0, len(c)-H, H):
                if f.iloc[i] < 0:
                    ret = c.iloc[i+H]/c.iloc[i]-1
                    rows.append(dict(coin=coin, w=w, ex=-(ret-mu), tot=-ret, absf=abs(f.iloc[i]),
                                     thick=thick.iloc[i], dist=dist.iloc[i], r26=r26p.iloc[i], r7=r7p.iloc[i],
                                     r90=r90p.iloc[i], vol=vol.iloc[i], mu=mu, z=-(ret-mu)/sd))
    d = pd.DataFrame(rows)
    out["n_cases"] = len(d)
    out["by_coin"] = d.groupby("coin").agg(n=("ex","size"), ex=("ex","mean"), tot=("tot","mean"), mu=("mu","first"))
    def qt(col):
        dd = d.dropna(subset=[col]).copy()
        dd["q"] = pd.qcut(dd[col], 4, labels=False, duplicates="drop")
        g = dd.groupby("q").agg(lo=(col,"min"), hi=(col,"max"), n=("ex","size"), ex=("ex","mean"), tot=("tot","mean"))
        g["t_tot"] = dd.groupby("q")["tot"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        return g
    for col in ["absf","thick","dist","r26","r7","r90","vol"]:
        out["q_"+col] = qt(col)
    # book daily by window
    bw = []
    for coin in days:
        for w, dd in days[coin].items():
            bw.append(dict(w=w, coin=coin, br=dd["book_return"].mean(), cr=dd["coin_return"].mean()))
    bw = pd.DataFrame(bw)
    out["book_by_window"] = bw.groupby("w")[["br","cr"]].mean().sort_values("br")
    return out
