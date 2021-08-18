# In[]
import random
from pathlib import Path
from random import choice
import numpy as np
import pandas as pd
import math

# 一個情境會有多少測資
file_num = 30

#benchmark =[m,h,n_max]
benchmark = [12,6,40]
marktype = ["L","H","M"]

m_list = [8,16]
# resource limit(同一個時間所能維修的最大機台數量)
h_list = [1,benchmark[0]] 
# 維修所需時間
b = 60
# numbers of jobs (每個機台最多有幾個工作)
n_list = [20,60]
# pt = processing_time.values
# s = start time
# due = job due time(大於s+pt/由時候加上維修時間有時候不加)
# job 流水號


def instance_generator(x,y,z,factor_s,marktype):
    m = x
    h = y
    n_max = z

    scenario = factor_s + '_' + marktype + '_' + str(m) + '_' + str(h) + '_' + str(n_max)
    # print(scenario)
    # # 定義路徑及檔名
    prefix = scenario  # problem 編號
    folder_name = "testdata_" + prefix
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    file_list = [str(i) for i in range(1, file_num + 1)]

    for f in file_list:

        file = open(folder_name + "/" + prefix + "_" + f + ".txt", "w+")
        r_a = []
        r_b = []
        pt = []
        s = []
        due = []
        job = []
        job_n = []
        
        for j in range(m):
            x = -1
            n_max = z
            while (x > n_max or x < 0):
                x = round(random.gauss(mu=int(n_max//2), sigma=int(n_max//6)))
                #print("test: " + str(x))
                n_temp = x
                
            job_n.append(n_temp)
            # print(j)
            # print(job_n)
            n = job_n[j]
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
        

        file.write(str(j+1) + " " + str(h) + " " + str(b) + "\n")   

        for j in range(m):
            n = job_n[j] 
            file.write(str(n) + " ")  

        file.write("\n") 

        for j in range(m):        
            file.write(str(j+1) + " " + str(r_a[j]) + " " + str(r_b[j]) + "\n")           

        for j in range(m):
            n = job_n[j]            
            for i in range(n): 
                file.write(str(j+1) + " " + str(job[j][i+1]) + " " + str(s[j][i+1]) + " " + str(pt[j][i+1]) + " " + str(due[j][i]) + "\n")


        file.close()

#benchmark
instance_generator(benchmark[0],benchmark[1],benchmark[2],"benchmark",marktype[2])

#factor_m
instance_generator(m_list[0],benchmark[1],benchmark[2],"m",marktype[0])
instance_generator(m_list[1],benchmark[1],benchmark[2],"m",marktype[1])

#factor_h
instance_generator(benchmark[0],h_list[0],benchmark[2],"h",marktype[0])
instance_generator(benchmark[0],h_list[1],benchmark[2],"h",marktype[1])

#factor_h
instance_generator(benchmark[0],benchmark[1],n_list[0],"n_max",marktype[0])
instance_generator(benchmark[0],benchmark[1],n_list[1],"n_max",marktype[1])


