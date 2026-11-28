import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    coinmean = {}
    for coin, wins in bars.items():
        for H in [1,2,3,5,10]:
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c)-H, H):
                    allr.append(c[i+H]/c[i]-1)
            coinmean[(coin,H)] = np.mean(allr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            sd = pd.Series(r).rolling(30).std().shift(1).values
            n = len(c)
            # down streak ending at t
            streak = np.zeros(n); 
            for i in range(1,n):
                streak[i] = streak[i-1]+1 if r[i] < 0 else 0
            for i in range(1, n):
                up = r[i] > 0
                prev_run = streak[i-1] if up else 0
                # depth of prior run
                k = int(prev_run)
                depth = np.nan
                if k>0 and i-k-1 >= 0 and not np.isnan(sd[i]):
                    depth = (1 - c[i-1]/c[i-1-k]) / sd[i]
                d = dict(coin=coin, w=w, i=i, prof=df["regime"].iloc[i] != "chop",
                         up=up, prev_run=prev_run, cur_down=streak[i], depth=depth,
                         r1=r[i], year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                         day=str(df["timestamp"].iloc[i])[:10])
                for H in [1,2,3,5,10]:
                    d[f"f{H}"] = (c[i+H]/c[i]-1 - coinmean[(coin,H)]) if (i+H < n) else np.nan
                    d[f"g{H}"] = (i % H == 0)
                rows.append(d)
    D = pd.DataFrame(rows)
    P = D[D.prof]
    def summ(sub, H):
        s = sub[sub[f"g{H}"]].dropna(subset=[f"f{H}"])
        if len(s) < 3: return pd.Series(dict(n=len(s), mean=np.nan, t=np.nan))
        g = s.groupby("day")[f"f{H}"].sum()
        m = s[f"f{H}"].mean()
        t = g.mean()/(g.std(ddof=1)/np.sqrt(len(g)))
        return pd.Series(dict(n=len(s), days=len(g), mean=m, t=t))
    out = {}
    groups = {
        "all_profile": P,
        "break_ge2": P[P.up & (P.prev_run>=2)],
        "break_ge3": P[P.up & (P.prev_run>=3)],
        "break_eq1": P[P.up & (P.prev_run==1)],
        "up_other": P[P.up & (P.prev_run==0)],
        "down_day_any": P[~P.up],
        "down_streak1": P[P.cur_down==1],
        "down_streak2": P[P.cur_down==2],
        "down_streak_ge3": P[P.cur_down>=3],
    }
    tab = []
    for name, g in groups.items():
        for H in [1,2,3,5,10]:
            s = summ(g, H); s["grp"]=name; s["H"]=H; tab.append(s)
    out["by_group_H"] = pd.DataFrame(tab).set_index(["grp","H"]).round(4)
    B = P[P.up & (P.prev_run>=2)].copy()
    B5 = B[B.g5].dropna(subset=["f5","depth"])
    B5["dq"] = pd.qcut(B5.depth, 4, labels=False, duplicates="drop")
    out["break_by_depth_q"] = B5.groupby("dq").agg(n=("f5","size"), depth=("depth","mean"), f5=("f5","mean")).round(4)
    out["break_by_runlen"] = B5.groupby(B5.prev_run.clip(upper=5)).agg(n=("f5","size"), f5=("f5","mean")).round(4)
    out["break_by_coin"] = B5.groupby("coin").agg(n=("f5","size"), f5=("f5","mean")).round(4)
    out["break_by_year"] = B5.groupby("year").agg(n=("f5","size"), f5=("f5","mean")).round(4)
    B5["r1q"] = pd.qcut(B5.r1, 3, labels=False)
    out["break_by_upday_size"] = B5.groupby("r1q").agg(n=("f5","size"), r1=("r1","mean"), f5=("f5","mean")).round(4)
    # down streak, depth graded: profile down days at grid 5
    Dn = P[(P.cur_down>=2) & P.g5].dropna(subset=["f5"])
    out["down_streak_by_len"] = Dn.groupby(Dn.cur_down.clip(upper=5)).agg(n=("f5","size"), f5=("f5","mean")).round(4)
    # all profile days by previous-day return quantile
    A = P[P.g5].dropna(subset=["f5","r1"]).copy()
    A["q"] = pd.qcut(A.r1/1, 5, labels=False)
    out["profile_by_r1_quintile"] = A.groupby("q").agg(n=("f5","size"), r1=("r1","mean"), f5=("f5","mean")).round(4)
    return out
