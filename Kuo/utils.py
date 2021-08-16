import matplotlib.pyplot as plt
import ast

class Instance:
	def __init__(self, m, h, b, n, rA, rB, s, p, d, cD, cT):
		self.m = m
		self.h = h
		self.b = b
		self.n = n
		self.rA = rA
		self.rB = rB
		self.s = s
		self.p = p
		self.d = d
		self.cD = cD
		self.cT = cT
	
class Solution:
	def __init__(self, s, p, b, sol, obj, obj_none, h, result_no_maintenance, result=[], d=[]):
		self.s = s
		self.p = p
		self.b = b
		self.sol = sol
		self.obj = obj
		self.obj_none = obj_none
		self.h = h
		self.result_no_maintenance = result_no_maintenance
		self.result = result
		self.d = d
'''
Read instance .txt file to get the parameters

input: file path
output: instance object
'''
def read_instance(file_path, output_obj=False):
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
	
	if not output_obj: return m, h, b, n, rA, rB, s, p, d, cD, cT
	
	inst = Instance(m, h, b, n, rA, rB, s, p, d, cD, cT)
	return inst
	
'''
Read solution .txt file to get the parameters and solutions
(1 solution only)

input: .txt file path (6 lines expected)
output: solution object
'''
def read_solution(file_path):
	with open(file_path, 'r') as f:
		s = ast.literal_eval(f.readline())
		p = ast.literal_eval(f.readline())
		b = ast.literal_eval(f.readline())
		h = ast.literal_eval(f.readline())
		obj = ast.literal_eval(f.readline())
		sol = ast.literal_eval(f.readline())
		
	return Solution(s, p, b, sol, obj, h)
	
def visualize(inst):
	s = inst.s
	p = inst.p
	b = inst.b
	sol = list(inst.sol)
	result_no_maintenance = inst.result_no_maintenance
	result = inst.result
	
	m = len(s) - 1

	fig, gnt = plt.subplots(1, 2)
	gnt[0].set_ylim(0, 5*(m + 1)) 
	gnt[0].set_xlim(0, 1000)
	gnt[0].set_xlabel('Time') 
	gnt[0].set_ylabel('No maintenance') 
	gnt[0].set_yticks([5 * i for i in range(1, m + 1)])
	gnt[0].set_yticklabels(['M' + str(i) for i in range(m, 0, -1)])
	gnt[0].title.set_text('obj = ' + str(inst.obj_none))
	
	for i in range(m):
		color = (0.078, 0.73, 0.1, 1)
		for j in range(len(result_no_maintenance[i])):
			if result_no_maintenance[i][j][2]: color = "pink"
			elif color == (0.078, 0.73, 0.1, 1): color = (0.078, 0.73, 0.1, 0.5)
			elif color == (0.078, 0.73, 0.1, 0.5): color = (0.078, 0.73, 0.1, 1)
			gnt[0].broken_barh([(result_no_maintenance[i][j][0], result_no_maintenance[i][j][1] - result_no_maintenance[i][j][0])], (5 * (m - i - 1) + 4, 2), facecolors=color)
	
	gnt[0].grid(True)
	
	if (len(result)) == 0:
		sol = list(inst.sol)
		gnt[1].set_ylim(0, 5*(m + 1)) 
		gnt[1].set_xlim(0, 1000)
		gnt[1].set_xlabel('Time') 
		gnt[1].set_ylabel('Suggested Maintenance') 
		gnt[1].set_yticks([5 * i for i in range(1, m + 1)])
		gnt[1].set_yticklabels(['M' + str(i) for i in range(m, 0, -1)])
		gnt[1].title.set_text('obj = ' + str(inst.obj))
		
		for i in range(1, m + 1):
			maintenance = False
			if len(sol) != 0 and sol[0][0] == i:
				maintenance = True
			
			if not maintenance:
				color = (0.078, 0.73, 0.1, 1)
				for j in range(1, len(s[i])):
					if color == (0.078, 0.73, 0.1, 0.5): color = (0.078, 0.73, 0.1, 1)
					elif color == (0.078, 0.73, 0.1, 1): color = (0.078, 0.73, 0.1, 0.5)
					gnt[1].broken_barh([(s[i][j], p[i][j])], (5 * (m - i) + 4, 2), facecolors=color) 
			
			else:
				cur = 0
				maintained = False
				color = (0.078, 0.73, 0.1, 1)
				for j in range(1, len(s[i])):
					if not maintained:
						if j == sol[0][1]:
							gnt[1].broken_barh([(cur, b)], (5 * (m - i) + 4, 2), facecolors='pink')
							cur += b
							sol.pop(0)
							maintained = True
					
					if cur < s[i][j]:
						cur = s[i][j]
					
					if color == (0.078, 0.73, 0.1, 0.5): color = (0.078, 0.73, 0.1, 1)
					elif color == (0.078, 0.73, 0.1, 1): color = (0.078, 0.73, 0.1, 0.5)
					gnt[1].broken_barh([(cur, p[i][j])], (5 * (m - i) + 4, 2), facecolors=color)
					cur += p[i][j]		
		
		gnt[1].grid(True)

	else:
		gnt[1].set_ylim(0, 5*(m + 1)) 
		gnt[1].set_xlim(0, 1000)
		gnt[1].set_xlabel('Time') 
		gnt[1].set_ylabel('Suggested maintenance') 
		gnt[1].set_yticks([5 * i for i in range(1, m + 1)])
		gnt[1].set_yticklabels(['M' + str(i) for i in range(m, 0, -1)])
		gnt[1].title.set_text('obj = ' + str(inst.obj))
		
		for i in range(m):
			color = (0.078, 0.73, 0.1, 1)
			for j in range(len(result[i])):
				if result[i][j][2]: color = "pink"
				elif color == (0.078, 0.73, 0.1, 1): color = (0.078, 0.73, 0.1, 0.5)
				elif color == (0.078, 0.73, 0.1, 0.5): color = (0.078, 0.73, 0.1, 1)
				elif color == "pink": color = (0.078, 0.73, 0.1, 0.5)
				gnt[1].broken_barh([(result[i][j][0], result[i][j][1] - result[i][j][0])], (5 * (m - i - 1) + 4, 2), facecolors=color)
		gnt[1].grid(True)
		
	if len(inst.d) != 0:
		for i in range(1, m + 1):
			for j in range(1, len(inst.d[i])):
				gnt[0].annotate("d" + str(j), (inst.d[i][j], 5 * (m - i) + 6),
							xytext=(inst.d[i][j], 5 * (m - i) + 8), textcoords='data',
							arrowprops=dict(facecolor='black', arrowstyle="->",
											connectionstyle="arc,rad=10"),
							fontsize=10,
							horizontalalignment='right', verticalalignment='top')
				gnt[1].annotate("d" + str(j), (inst.d[i][j], 5 * (m - i) + 6),
							xytext=(inst.d[i][j], 5 * (m - i) + 8), textcoords='data',
							arrowprops=dict(facecolor='black', arrowstyle="->",
											connectionstyle="arc,rad=10"),
							fontsize=10,
							horizontalalignment='right', verticalalignment='top')
	
	
	
	plt.savefig('schedule.png')
	plt.show()

def feasible(s, p, b, sol, h):
	if len(sol) != 0:
		load_dict = {}
		machine_occupy_dict = {}
		maintenance_starts = []
		for i in sol:
			maintenance_starts.append((s[i[0]][i[1] - 1]))
		
		for i in range(len(sol)):
			for j in range(maintenance_starts[i], maintenance_starts[i] + b):
				if j not in load_dict:
					load_dict[j] = 1
				else: load_dict[j] += 1
				
				if j not in machine_occupy_dict:
					machine_occupy_dict[j] = [sol[i]]
				else:
					machine_occupy_dict[j].append(sol[i])

		if sorted(list(load_dict.values()), reverse=True)[0] > h:
			for i in sorted(load_dict.items(), key=lambda x: x[0]):
				if i[1] > h: return False, machine_occupy_dict[i[0]]

	return True, []

def feasible_result(result, h):
	sol = []
	load_dict = {}
	machine_occupy_dict = {}
	
	for i in range(len(result)):
		for j in range(len(result[i])):
			if result[i][j][2]: sol.append((i + 1, j + 1, result[i][j][0], result[i][j][1]))
	
	for i in sol:
		for j in range(i[2], i[3]):
			if j not in load_dict:
				load_dict[j] = 1
			else: load_dict[j] += 1
			
			if j not in machine_occupy_dict:
				machine_occupy_dict[j] = [(i[0], i[1])]
			else:
				machine_occupy_dict[j].append((i[0], i[1]))
				
	if sorted(list(load_dict.values()), reverse=True)[0] > h:
		for i in sorted(load_dict.items(), key=lambda x: x[0]):
			if i[1] > h: return False, machine_occupy_dict[i[0]]
	
	return True, []
		
def machine_not_duplicate(x):
	machines = [i[0] for i in x]
	return len(machines) == len(set(machines))