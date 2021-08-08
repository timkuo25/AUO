from utils import read_instance
import time

def algo1_public(m=0, h=0, b=0, n=[], rA=[], rB=[], s=[], p=[], d=[], cD=1, cT=1):
	c_none = float()
	sol = []
	obj = float()
	candidate = "none"
	x = [[0]]
	for i in range(1, m + 1):
		x.append([0] * (n[i] + 1))

	# defect cost
	for i in range(1, m + 1):
		c_none += rB[i] * sum(p[i])
	c_none *= cD
	
	# tardiness
	for i in range(1, m + 1):
		for j in range(1, n[i] + 1):
			tardiness = max(0, s[i][j] + p[i][j] - d[i][j])
			c_none += cT * tardiness
	obj = c_none
	
	for i in range(1, m + 1):
		for j in range(1, n[i] + 1):
			cost = 0
			
			for k in range(1, m + 1):
				if k != i:
					# defect cost
					cost += rB[k] * sum(p[k])
					
					# tardiness cost
					tardiness = 0
					for l in range(1, n[k] + 1):
						tardiness += max(0, s[k][l] + p[k][l] - d[k][l])
					cost += cT * tardiness
		
				else:
					# defect cost
					cost += rB[k] * sum(p[k][:j]) + rA[k] * sum(p[k][j:])
					
					# tardiness cost
					tardiness = 0
					cur = 0
					for l in range(1, n[k] + 1):
						if l == j:
							cur += b
						if cur < s[k][l]:
							cur = s[k][l]
						cur += p[k][l]
						tardiness += max(0, cur - d[k][l])

					cost += cT * tardiness

			if cost < obj:
				obj = cost
				candidate = (i, j)
	return obj

# 給雪燕的，只輸出opt和running time	
def algo1(instance_path):
	m, h, b, n, rA, rB, s, p, d, cD, cT = read_instance(instance_path)
	start_time = time.time()
	opt = algo1_public(m, h, b, n, rA, rB, s, p, d, cD, cT)
	running_time = time.time() - start_time
	
	return opt, running_time


