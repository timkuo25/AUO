import matplotlib.pyplot as plt
import ast

class Instance:
	def __init__(self, m, h_bar, n, rA, rB, h, b, s, p, d, cD, cT):
		self.m = m
		self.h_bar = h_bar
		self.n = n
		self.rA = rA
		self.rB = rB
		self.h = h
		self.b = b
		self.s = s
		self.p = p
		self.d = d
		self.cD = cD
		self.cT = cT
	
class Solution:
	def __init__(self, s, p, b, sol, obj, h, h_bar, result=[], d=[]):
		self.s = s
		self.p = p
		self.b = b
		self.sol = sol
		self.obj = obj
		self.h = h
		self.h_bar = h_bar
		self.result = result
		self.d = d
'''
Read instance .txt file to get the parameters

input: file path
output: instance object
'''
def read_instance(file_path, output_obj=False):
	m = int()
	h_bar = int()
	n = []
	cD = 1
	cT = 1

	rA = [0]
	rB = [0]
	h = [0]
	b = [0]
	
	s = [[0]]
	p = [[0]]
	d = [[0]]
	
	with open(file_path, 'r') as f:
		# m
		line = f.readline().split()
		m, h_bar = [int(i) for i in line]
		
		line = f.readline().split()
		n = [0] + [int(i) for i in line]
		
		# rA, rB, h, b
		for _ in range(m):
			line = f.readline().split()
			rA.append(float(line[1]))
			rB.append(float(line[2]))
			h.append(int(line[3]))
			b.append(int(line[4]))

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
	
	if not output_obj: return m, h_bar, n, rA, rB, h, b, s, p, d, cD, cT
	
	inst = Instance(m, h_bar, n, rA, rB, h, b, s, p, d, cD, cT)
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
	
def generate_no_maintenance_result(inst):
	s = inst.s
	p = inst.p
	b = inst.b
	return [[(s[i][j], s[i][j] + p[i][j], False) for j in range(1, len(s[i]))] for i in range(1, len(s))]
	
def generate_result(s, p, b, sol):	
	m = len(sol)
	result = []
	
	for i in range(1, m + 1):
		target = sol[i - 1]
		n_i = len(s[i]) - 1
		result_i = []
		
		cur = 0
		for j in range(1, n_i + 1):
			if target == j:
				result_i.append((cur, cur + b[i], True))
				cur += b[i]

			if cur < s[i][j]: cur = s[i][j]
			result_i.append((cur, cur + p[i][j], False))
			cur += p[i][j]
		
		result.append(result_i)
	
	return result

def visualize_result(result_no_maintenance, obj_no_maintenance, result, obj, d = []):
	m = len(result)

	fig, gnt = plt.subplots(1, 2)
	
	if len(result_no_maintenance) != 0:
		gnt[0].set_ylim(0, 5*(m + 1)) 
		gnt[0].set_xlim(0, 1500)
		gnt[0].set_xlabel('Time') 
		gnt[0].set_ylabel('Result') 
		gnt[0].set_yticks([5 * i for i in range(1, m + 1)])
		gnt[0].set_yticklabels(['M' + str(i) for i in range(m, 0, -1)])
		gnt[0].title.set_text('obj = ' + str(obj_no_maintenance))
		
		for i in range(m):
			color = (0.078, 0.73, 0.1, 1)
			for j in range(len(result_no_maintenance[i])):
				if result_no_maintenance[i][j][2]: color = "pink"
				elif color == (0.078, 0.73, 0.1, 1): color = (0.078, 0.73, 0.1, 0.5)
				elif color == (0.078, 0.73, 0.1, 0.5): color = (0.078, 0.73, 0.1, 1)
				elif color == "pink": color = (0.078, 0.73, 0.1, 0.5)
				gnt[0].broken_barh([(result_no_maintenance[i][j][0], result_no_maintenance[i][j][1] - result_no_maintenance[i][j][0])], (5 * (m - i - 1) + 4, 2), facecolors=color)
		
		gnt[0].grid(True)
	
	
	if len(d) != 0:
		for i in range(1, m + 1):
			for j in range(1, len(d[i])):
				gnt[0].annotate("d" + str(j), (d[i][j], 5 * (m - i) + 6),
							xytext=(d[i][j], 5 * (m - i) + 8), textcoords='data',
							arrowprops=dict(facecolor='black', arrowstyle="->",
											connectionstyle="arc,rad=10"),
							fontsize=10,
							horizontalalignment='right', verticalalignment='top')
				gnt[1].annotate("d" + str(j), (d[i][j], 5 * (m - i) + 6),
							xytext=(d[i][j], 5 * (m - i) + 8), textcoords='data',
							arrowprops=dict(facecolor='black', arrowstyle="->",
											connectionstyle="arc,rad=10"),
							fontsize=10,
							horizontalalignment='right', verticalalignment='top')
	
	
	gnt[1].set_ylim(0, 5*(m + 1)) 
	gnt[1].set_xlim(0, 1800)
	gnt[1].set_xlabel('Time') 
	gnt[1].set_ylabel('Result') 
	gnt[1].set_yticks([5 * i for i in range(1, m + 1)])
	gnt[1].set_yticklabels(['M' + str(i) for i in range(m, 0, -1)])
	gnt[1].title.set_text('obj = ' + str(obj))
	
	for i in range(m):
		color = (0.078, 0.73, 0.1, 1)
		for j in range(len(result[i])):
			if result[i][j][2]: color = "pink"
			elif color == (0.078, 0.73, 0.1, 1): color = (0.078, 0.73, 0.1, 0.5)
			elif color == (0.078, 0.73, 0.1, 0.5): color = (0.078, 0.73, 0.1, 1)
			elif color == "pink": color = (0.078, 0.73, 0.1, 0.5)
			gnt[1].broken_barh([(result[i][j][0], result[i][j][1] - result[i][j][0])], (5 * (m - i - 1) + 4, 2), facecolors=color)
	
	gnt[1].grid(True)
	
	
	if len(d) != 0:
		for i in range(1, m + 1):
			for j in range(1, len(d[i])):
				gnt[0].annotate("d" + str(j), (d[i][j], 5 * (m - i) + 6),
							xytext=(d[i][j], 5 * (m - i) + 8), textcoords='data',
							arrowprops=dict(facecolor='black', arrowstyle="->",
											connectionstyle="arc,rad=10"),
							fontsize=10,
							horizontalalignment='right', verticalalignment='top')
				gnt[1].annotate("d" + str(j), (d[i][j], 5 * (m - i) + 6),
							xytext=(d[i][j], 5 * (m - i) + 8), textcoords='data',
							arrowprops=dict(facecolor='black', arrowstyle="->",
											connectionstyle="arc,rad=10"),
							fontsize=10,
							horizontalalignment='right', verticalalignment='top')
	
	plt.savefig('schedule2.png')
	plt.show()

def calculate_result_cost(result, d, rA, rB, cD, cT):
	defect_cost = 0
	tardiness_cost = 0
	
	for i in range(len(result)):
		maintained = False
		j = 0
		
		for item in result[i]:
			if not item[2]:
				tardiness_cost += max(0, item[1] - d[i + 1][j + 1])
				if maintained:
					defect_cost += rA[i + 1] * (item[1] - item[0])
				else:
					defect_cost += rB[i + 1] * (item[1] - item[0])
				j += 1
			else:
				maintained = True
		#print(tardiness_cost, defect_cost)
	return cD * defect_cost + cT * tardiness_cost

def feasible_result(result, h, h_bar):
	sol = []
	load_dict = {}
	machine_occupy_dict = {}
	
	for i in range(len(result)):
		for j in range(len(result[i])):
			if result[i][j][2]: sol.append((i + 1, j + 1, result[i][j][0], result[i][j][1]))

	for i in sol:
		for j in range(i[2], i[3]):
			if j not in load_dict:
				load_dict[j] = h[i[0]]
			else: load_dict[j] += h[i[0]]
			
			if j not in machine_occupy_dict:
				machine_occupy_dict[j] = [(i[0], i[1])]
			else:
				machine_occupy_dict[j].append((i[0], i[1]))			
	
	if len(sorted(list(load_dict.values()), reverse=True)) == 0: return True, []
	
	if sorted(list(load_dict.values()), reverse=True)[0] > h_bar:
		for i in sorted(load_dict.items(), key=lambda x: x[0]):
			if i[1] > h_bar: return False, machine_occupy_dict[i[0]]
	
	return True, []
	
	