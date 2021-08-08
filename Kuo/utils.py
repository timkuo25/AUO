import matplotlib.pyplot as plt
import ast

'''
Read instance .txt file to get the parameters

input: file path
output: all the parameters
'''
def read_instance(file_path):
	m = int()
	h = int()
	b = int()
	n = []
	cD = 1
	cT = 1

	rA = [0]
	rB = [0]

	s = [[0]]
	p = [[0]]
	d = [[0]]
	with open(file_path, 'r') as f:
		# m, h, b, n
		line = f.readline().split()
		m, h, b = [int(i) for i in line]
		
		line = f.readline().split()
		n = [0] + [int(i) for i in line]
		
		# rA, rB
		for _ in range(m):
			line = f.readline().split()
			rA.append(float(line[1]))
			rB.append(float(line[2]))

		for i in range(1, 1 + m):
			s_i = [0]
			p_i = [0]
			d_i = [0]
			for _ in range(n[i]):
				line = f.readline().split()
				s_i.append(int(line[2]))
				p_i.append(int(line[3]))
				d_i.append(int(line[4]))
			s.append(s_i)
			p.append(p_i)
			d.append(d_i)
	return m, h, b, n, rA, rB, s, p, d, cD, cT	

'''
Read solution .txt file to get the parameters and solutions
(1 solution only)

input: .txt file path (6 lines expected)
output: s, p, b, h, opt, sol
'''
def read_solution(file_path):
	with open(file_path, 'r') as f:
		s = ast.literal_eval(f.readline())
		p = ast.literal_eval(f.readline())
		b = ast.literal_eval(f.readline())
		h = ast.literal_eval(f.readline())
		opt = ast.literal_eval(f.readline())
		sol = ast.literal_eval(f.readline())
	return s, p, b, h, opt, sol
	
'''
Plot a solution

input: s, p, b, sol
'''
def visualizer(s, p, b, sol):
	m = len(s) - 1
	
	fig, gnt = plt.subplots()
	gnt.set_ylim(0, 5*(m + 1)) 
	gnt.set_xlim(0, 500)
	gnt.set_xlabel('Time') 
	gnt.set_ylabel('Machine') 
	gnt.set_yticks([5 * i for i in range(1, m + 1)])
	gnt.set_yticklabels(['M' + str(i) for i in range(m, 0, -1)]) 
	
	for i in range(1, m + 1):
		maintenance = False
		if len(sol) != 0 and sol[0][0] == i:
			maintenance = True
		
		if not maintenance:
			gnt.broken_barh([(s[i][j], p[i][j]) for j in range(1, len(s[i]))], (5 * (m - i) + 3, 4), facecolors =('green')) 
		
		else:
			cur = 0
			maintained = False
			for j in range(1, len(s[i])):
				if not maintained:
					if j == sol[0][1]:
						gnt.broken_barh([(cur, b)], (5 * (m - i) + 3, 4), facecolors =('pink'))
						cur += b
						sol.pop(0)
						maintained = True
				
				if cur < s[i][j]:
					cur = s[i][j]
					
				gnt.broken_barh([(cur, p[i][j])], (5 * (m - i) + 3, 4), facecolors =('green'))
				cur += p[i][j]		
	
	gnt.grid(True)
	plt.show()

'''
Check solution feasibility

input: s, p, b, sol, h
output: True (feasible)/ False (infeasible)
'''
def feasibility_checker(s, p, b, sol, h):
	#s, p shape check
	if len(s) != len(p): return False
	for i in range(len(s)):
		if len(s[i]) != len(p[i]): return False

	# h constraint
	if len(sol) != 0:
		load_dict = {}
		maintenance_starts = []
		for i in sol:
			maintenance_starts.append((s[i[0]][i[1] - 1]))
			
		for i in maintenance_starts:
			for j in range(i, i + 60):
				if j not in load_dict:
					load_dict[j] = 1
				else: load_dict += 1
		if sorted(list(load_dict.values()), reverse=True)[0] > h: return False
	
	return True