# In[]
import random
from pathlib import Path
from random import choice
import numpy as np
import pandas as pd

# 一個情境會有多少測資
file_num = 1
m = 12
# resource limit(同一個時間所能維修的最大機台數量)
h = 6
# 維修所需時間
b = 60
# numbers of jobs (每個機台會有幾個工作)
#n = 10


#scenario = 'benchmark_new'
scenario = 'benchmark_12_6_40'
# # 定義路徑及檔名
prefix = scenario  # problem 編號
folder_name = "testdata_0818/" + prefix
Path(folder_name).mkdir(parents=True, exist_ok=True)
file_list = [str(i) for i in range(1, file_num + 1)]

for f in file_list:

    file = open(folder_name + "/" + prefix + "_" + f + ".txt", "w+")
    r_a = []
    r_b = []   
    n_list = []
    # pt = processing_time.values
    # s = start time
    # due = job due time(大於s+pt/由時候加上維修時間有時候不加)
    # job 流水號
    pt = []
    s = []
    due = []
    job = []
    
    
    for j in range(m):
        #假設n_max = 60
        x = -1
        n_max = 60
        while (x > n_max or x < 0):
            x = round(random.gauss(mu=int(n_max//2), sigma=int(n_max//6)))
            #print("test: " + str(x))
            n_temp = x

        n_list.append(n_temp)
        n = n_list[j]
        #print(n_list)
        r_a.append(round(random.uniform(0.02, 0.1),2))
        r_b.append(round(random.uniform(0.1, 0.2),2))

        temp_pt = [0]
        for i in range(n):
            x = -1
            while (x > 90 or x < 30):
                x = round(random.gauss(mu=60, sigma=int(30//3)))
                #print("test: " + str(x))
                pt_temp = x
            temp_pt.append(pt_temp)
        pt.append(temp_pt)
        #print(pt)

        temp_job = [0]
        for i in range(n):
            temp_job.append(i+1)
        job.append(temp_job)
        #print(job)
        
        temp_s = [0]
        for i in range(n):
            #idle = np.random.choice([0,20], size=1, p=[0.75,0.25])
            temp_s.append(int(temp_s[i])+int(pt[j][i])+int(np.random.choice([0,20], size=1, p=[0.75,0.25])))
        s.append(temp_s)
        #print(s)


        temp_due= []
        for i in range(n): 
            temp_due.append(int(s[j][i+1])+int(pt[j][i+1]) + int(np.random.choice([20,b], size=1, p=[1-((1/n)/2),(1/n)/2])))
        due.append(temp_due)
        #print(due)

    file.write(str(j+1) + " " + str(h) + " " + str(b) + "\n")   
    
    for j in range(m):
        n = n_list[j] 
        file.write(str(n) + " ")  

    file.write("\n") 

    for j in range(m):        
        file.write(str(j+1) + " " + str(r_a[j]) + " " + str(r_b[j]) + "\n")           

    for j in range(m):
        n = n_list[j]            
        for i in range(n): 
            file.write(str(j+1) + " " + str(job[j][i+1]) + " " + str(s[j][i+1]) + " " + str(pt[j][i+1]) + " " + str(due[j][i]) + "\n")


    file.close()

# %%