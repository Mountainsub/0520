
import pandas as pd
import numpy as np
import time 
import sys
import os
import ctypes
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


import datetime

from lib.ddeclient import DDEClient
from price_logger import ClientHolder 
from price_logger import LastNPerfTime
from init import keisan

class plot_time:
    def __init__(self):
        self.hdffilename = "./data/sum.hdf5"
        self.store = pd.HDFStore(self.hdffilename)
        self.key_name2 = "timecase"

    

    def hozon2(self, data_dict):
        #print("OK")
        self.store.append(self.key_name2, data_dict)
      

        

    

    
    


if __name__ == "__main__":
    
    # コマンドライン上の出力文字に色を付ける
    ENABLE_PROCESSED_OUTPUT = 0x0001
    ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    MODE = ENABLE_PROCESSED_OUTPUT + ENABLE_WRAP_AT_EOL_OUTPUT + ENABLE_VIRTUAL_TERMINAL_PROCESSING
    
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    kernel32.SetConsoleMode(handle, MODE)

    
    calc = 0
    
    object_pass = "value"
    dde = DDEClient("rss", "1306.T")
    
    st = pd.HDFStore("./data/sum.hdf5")
    

    currently = datetime.datetime.now()
    year = currently.year
    month = currently.month
    day = currently.day        
    price = 0
    total_interest = 0
    holder = plot_time()
    fail_count = 0
    syokichi = 8035813130
    while True:
        calc = 0
        x = 0
        Boolean = False
        for i in range(18):
            cycle = 0
            idx = i *126
            object_pass = "classidx_"+ str(idx)
            filename = "./data/"+str(idx).zfill(3)+"_2.hdf5"
            try:
                with pd.HDFStore(filename) as store:
                    temp =store.get(object_pass)
            except:
                pass
            else:
                end = temp.tail(1)
                
                # 更新中に取得した場合など値の取得を誤ったとき、一からやりなおすのも面倒なので
                # 取得をやりなおす。tempはDataframe形式で最新の126個分の計算値が入っている。
                while cycle<=2:
                    try:
                        v = float(end["total"])
                    except:
                        v = 0
                        end = temp.tail(1)
                        cycle += 1
                    else:
                        break
                # どうしても取得できなかった時は、「番号, attention, 現在時刻」を出力して、0からやり直す。  BooleanがTrueの時はやり直しますよ、の意。 
                if v==0:
                    now = datetime.datetime.now()
                    print(i, "attention", now)
                    Boolean = True    
                else:
                    print(i, '{:.2f}'.format(v))
                    x += 1
                if Boolean:
                    break
                
                

                
                calc += v
        
        if x != 18:
            Boolean = True
        print(calc)
        
        
        if Boolean:
            print("足し算のミス")
            pass
            #continue
        
        dict = {"total": [calc]}
                
        dict = pd.DataFrame(dict)

        
        

        
        
        now = datetime.datetime.now()
        total = calc
        calc /=  syokichi
        
        
        topix = dde.request("現在値").decode("sjis")
        topix_a = dde.request("最良売気配値").decode("sjis")
        topix_b = dde.request("最良買気配値").decode("sjis")
        topix_c = dde.request("最良売気配数量").decode("sjis")
        topix_d = dde.request("最良買気配数量").decode("sjis")
        
        print("取得時刻:"+str(now),"計算値:" + str(calc))
        #syokichi += calc  -float(topix)
        # 格納する値、左から順に　現在時刻、計算したトピックス、取得したトピックスの指標、1976年の加重総計額、ここまでの利益総額、取得に失敗した回数
        data_dict = {"time":[str(now)], "calc":[calc],"topix":[topix], "topix_a":[topix_a], "topix_b":[topix_b],"topix_c":[topix_c], "topix_d":[topix_d],"total":[total]}
        st.append("consequence",pd.DataFrame(data_dict), index=False)


        """
        temp = pd.datetime(year, month, day, 14, 58)
        if now > temp:
            
            print("end") 
        
        # 売り
        if calc > topix_a:
            if inventory >= admissible_M:
                continue
            else:
                order = "buy"
                quantity = inventory
                inventory += quantity 
        elif calc < topix_b:
            if inventory <= float(topix_d):
                continue
            else:
                order = "sell"
                order_p = topix_a
                quantity = inventory
                inventory -= quantity
        else:
            if inventory >= admissible_M:
                order_p = topix_a
                order = "sell"
                order_q = admissible_M - admissible_m 
                inventory -= order_q
            else:
                order_q = admissible_M - admissible_m
                order  = "buy"
                order_p= topix_b
                inventory += order_q
                if 



        # 買い
        if topix_d > :
            ddffg
        """
        