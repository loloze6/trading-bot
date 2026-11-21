import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; lr = np.log(cl).diff()
            alloc = b["postRebalance_current_allocation"].fillna(0)
            nxt = cl.shift(-1)/cl - 1
            kij = (b["high"].rolling(26).max()+b["low"].rolling(26).min())/2
            ten = (b["high"].rolling(9).max()+b["low"].rolling(9).min())/2
            vol20 = lr.rolling(20).std()*np.sqrt(365)
            r10 = cl/cl.shift(10)-1
            r3 = cl/cl.shift(3)-1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            held = alloc > 0
            # entry index of each holding spell
            start = held & ~held.shift(1, fill_value=False)
            spell = start.cumsum()
            entry_close = cl.where(start).groupby(spell).transform("first")
            entry_vol = vol20.where(start).groupby(spell).transform("first")
            age = held.groupby(spell).cumsum()
            df = pd.DataFrame(dict(coin=c, window=w, year=yr, alloc=alloc, nxt=nxt,
                                   gain=alloc*nxt, ddentry=cl/entry_close-1,
                                   vskij=cl/kij-1, tk=ten/kij-1, r10=r10, r3=r3,
                                   volratio=vol20/entry_vol, age=age))
            recs.append(df[held])
    H = pd.concat(recs).dropna(subset=["nxt"])
    out["n_held_bars"] = len(H)
    def grp(col, q=5):
        k = pd.qcut(H[col], q, labels=False, duplicates="drop")
        g = H.groupby(k).agg(n=("nxt","size"), lo=(col,"min"), hi=(col,"max"),
                             nxt_mean=("nxt","mean"), nxt_sd=("nxt","std"), gain=("gain","mean"))
        g["t"] = g.nxt_mean/(g.nxt_sd/np.sqrt(g.n))
        return g.drop(columns="nxt_sd")
    for col in ["ddentry","vskij","tk","r10","r3","volratio","age"]:
        out["held_by_"+col] = grp(col)
    out["held_by_year"] = H.groupby("year").agg(n=("nxt","size"), nxt=("nxt","mean"), gain=("gain","sum"))
    # below kijun vs above, and with ddentry deep
    H["below_kij"] = H.vskij < 0
    out["below_kij_split"] = H.groupby("below_kij").agg(n=("nxt","size"), nxt=("nxt","mean"), gain_sum=("gain","sum"))
    a = H.loc[H.vskij<0,"nxt"].dropna(); bb = H.loc[H.vskij>=0,"nxt"].dropna()
    out["below_minus_above_t"] = float(stats.ttest_ind(a, bb, equal_var=False).statistic)
    # worst 5% of book gain bars: their state
    q = H.gain.quantile(0.05)
    out["worst_bars_state"] = H[H.gain<=q][["ddentry","vskij","tk","r10","volratio","age"]].median()
    out["all_bars_state"] = H[["ddentry","vskij","tk","r10","volratio","age"]].median()
    return out
