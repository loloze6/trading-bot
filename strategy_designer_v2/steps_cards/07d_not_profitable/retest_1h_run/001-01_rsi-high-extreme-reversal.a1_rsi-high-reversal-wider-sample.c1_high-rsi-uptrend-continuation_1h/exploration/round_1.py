def explore(data):
    import numpy as np, pandas as pd
    rows=[]; drow=[]; grid=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            r=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].fillna(0)
            g=a*r
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            turn=(a-b["previous_allocation"].fillna(0)).abs()
            rsi=50-b["debug_info.components.rsi14d.last_history_value"]
            df=pd.DataFrame({"coin":c,"w":w,"g":g,"fee":fee,"a":a,"turn":turn,"r":r,"regime":b["regime"],"rsi":rsi,"fc":b["forecast"]})
            rows.append(df)
            d=data["days"][c][w]
            drow.append(pd.DataFrame({"coin":c,"w":w,"br":d["book_return"],"cr":d["coin_return"]}))
            # grid 240
            cl=b["close"].values; n=len(cl)
            for i in range(0,n-240,240):
                grid.append({"coin":c,"fc":b["forecast"].iloc[i],"rsi":rsi.iloc[i],"f240":cl[i+240]/cl[i]-1,"tr":b["regime"].iloc[i]=="trending"})
    A=pd.concat(rows); D=pd.concat(drow); G=pd.DataFrame(grid)
    out={}
    out["per bar totals"]=pd.Series({"gross mean/bar":A.g.mean(),"fee mean/bar":A.fee.mean(),"turnover/bar":A.turn.mean(),"mean |alloc|":A.a.abs().mean(),"share long bars":(A.a>0).mean(),"share short bars":(A.a<0).mean(),"share trending":(A.regime=="trending").mean()})
    A["side"]=np.sign(A.a)
    out["by side"]=A.groupby("side").agg(n=("g","size"),gross=("g","mean"),fee=("fee","mean"),turn=("turn","mean"))
    A["rsib"]=pd.cut(A.rsi,[0,40,45,50,55,60,65,100])
    out["by rsi bin"]=A.groupby("rsib").agg(n=("g","size"),gross=("g","mean"),fee=("fee","mean"),alloc=("a","mean"),r=("r","mean"))
    out["by coin"]=A.groupby("coin").agg(gross=("g","mean"),fee=("fee","mean"),turn=("turn","mean"))
    D=D.dropna()
    out["daily"]=pd.Series({"book mean":D.br.mean(),"book sd":D.br.std(),"coin mean":D.cr.mean()})
    A["fcb"]=pd.cut(A.fc,[-21,-10,-5,-1e-9,1e-9,5,10,21])
    out["by forecast bin"]=A.groupby("fcb").agg(n=("g","size"),gross=("g","mean"),fee=("fee","mean"),r=("r","mean"))
    T=G[G.tr]; T["rb"]=pd.cut(T.rsi,[0,45,50,55,60,100]); T["fb"]=pd.cut(T.fc,[-21,-5,0,5,21])
    out["grid by rsi"]=T.groupby("rb").f240.agg(["count","mean"])
    out["grid by forecast"]=T.groupby("fb").f240.agg(["count","mean"])
    out["corr fc rsi"]=float(A[A.regime=="trending"][["fc","rsi"]].corr().iloc[0,1])
    return out
