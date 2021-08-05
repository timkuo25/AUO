# In[]
import random
from pathlib import Path
from random import choice
import numpy as np
import pandas as pd

# 一個情境會有多少測資
file_num = 30
m = 2
# resource limit(同一個時間所能維修的最大機台數量)
h = 1
# 維修所需時間
b = 60
# numbers of jobs (每個機台會有幾個工作)
#n = 10


scenario = 'benchmark_new'
# # 定義路徑及檔名
prefix = scenario  # problem 編號
folder_name = "testdata_0805_final_2/" + prefix
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
        n_list.append(random.randint(5,10))
        n = n_list[j]
        r_a.append(round(random.uniform(0.02, 0.1),2))
        r_b.append(round(random.uniform(0.1, 0.2),2))

        temp_pt = [0]
        for i in range(n):
            temp_pt.append(random.randint(30,90))
        pt.append(temp_pt)

        temp_job = [0]
        for i in range(n):
            temp_job.append(i+1)
        job.append(temp_job)
        
        temp_s = [0]
        for i in range(n):
            #idle = np.random.choice([0,20], size=1, p=[0.75,0.25])
            temp_s.append(int(temp_s[i])+int(pt[j][i])+int(np.random.choice([0,20], size=1, p=[0.75,0.25])))
        s.append(temp_s)

        temp_due= []
        for i in range(n): 
            temp_due.append(int(s[j][i+1])+int(pt[j][i+1]) + int(np.random.choice([20,b], size=1, p=[1-((1/n)/2),(1/n)/2])))
        due.append(temp_due)      
    
    for j in range(m):        
        file.write(str(j+1) + " " + str(r_a[j]) + " " + str(r_b[j]) + "\n")

    for j in range(m):
        n = n_list[j] 
        file.write(str(j+1) + " " + str(h) + " " + str(b) + " " + str(n) + "\n")              

    for j in range(m):
        n = n_list[j]            
        for i in range(n): 
            file.write(str(j+1) + " " + str(job[j][i+1]) + " " + str(s[j][i+1]) + " " + str(pt[j][i+1]) + " " + str(due[j][i]) + "\n")


    file.close()

# %%