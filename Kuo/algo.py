from utils import read_instance, feasible, Solution, machine_not_duplicate
import time
from itertools import combinations

def algo(inst, mode="first_combinations", nth_best=2):
	m = inst.m
	h = inst.h
	b = inst.b
	n = inst.n
	rA = inst.rA
	rB = inst.rB
	s = inst.s
	p = inst.p
	d = inst.d
	cD = inst.cD
	cT = inst.cT
	
	#Parameter manipulation
	#b = 60
	cD = 3.8
	#cT = 1
	
	sol = []
	collision = []
	sol_value_dict = {}
	cost = [[0], [0]]
	obj = float()
	c_none_total = 0
	c_pick_total = 0
	
	for i in range(1, m + 1):
		candidate = None
		c_none = 0
		c_pick = 0

		# defect cost
		c_none += rB[i] * sum(p[i]) * cD
		
		# tardiness
		for j in range(1, n[i] + 1):
			c_none += cT * max(0, s[i][j] + p[i][j] - d[i][j])
			
		obj = c_none
		cost[0].append(c_none)

		for j in range(1, n[i] + 1):
			# defect cost
			c_pick += rB[i] * sum(p[i][:j]) + rA[i] * sum(p[i][j:])
			# tardiness
			tardiness = 0
			cur = 0
			for k in range(1, n[i] + 1):
				if k == j:
					cur += b
				if cur < s[i][k]:
					cur = s[i][k]
				cur += p[i][k]
				tardiness += max(0, cur - d[i][k])

			c_pick += cT * tardiness
			
			if c_pick < obj:
				obj = c_pick
				candidate = (i, j)
		
		#first best cost
		cost[1].append(obj)
		
		if candidate != None:
			sol_value_dict[candidate] = obj
			sol.append(candidate)
	
	fsb, collision = feasible(s, p, b, sol, h)
	
	if fsb:
		obj = sum(cost[1])
		solution = Solution(s, p, b, sol, obj, h)
		return solution
	
	if mode == "first_combinations":
		all_comb = []
		for i in range(len(sol) - 1):
			comb = list(combinations(sol, i + 1))
			for j in comb:
				j = list(j)
				all_comb.append(j)
		
		best_obj = float('inf')
		best_sol = []
		for comb in all_comb:
			sol = comb
			fsb, collision = feasible(s, p, b, sol, h)
			if fsb:
				# cost_none
				sol_cost = sum(cost[0])
				for i in sol:
					sol_cost = sol_cost - cost[0][i[0]] + sol_value_dict[i]

				if sol_cost < best_obj:
					best_obj = sol_cost
					best_sol = sol
		
		solution = Solution(s, p, b, best_sol, best_obj, h)
		return solution
		
	elif mode == "nth_combinations":
		sol_left = list(sol)
		for _ in range(1, nth_best):
			sol_round_n = []
			cost_n = list(cost[0])
			
			for s_ in sol_left:
				i = s_[0]
				obj = cost[0][i] # cost none of machine i
				prev_best = cost[-1][i]
				candidate = None
				
				for j in range(1, n[i] + 1):
					# defect cost
					c_pick = rB[i] * sum(p[i][:j]) + rA[i] * sum(p[i][j:])
				
					# tardiness
					tardiness = 0
					cur = 0
					for k in range(1, n[i] + 1):
						if k == j:
							cur += b
						if cur < s[i][k]:
							cur = s[i][k]
						cur += p[i][k]
						tardiness += max(0, cur - d[i][k])

					c_pick += cT * tardiness
					
					if c_pick < obj and c_pick > prev_best:
						obj = c_pick
						candidate = (i, j)
			
				cost_n[i] = obj
				
				if candidate != None:
					sol_value_dict[candidate] = obj
					sol.append(candidate)
					sol_round_n.append(candidate)
			
			sol_left = sol_round_n
			cost.append(cost_n)
			if len(sol_left) == 0: break
			'''
			# debug area
			print(sol)
			for i in cost:
				print(i)
			print(sol_value_dict)
			'''
		
		all_comb = []
		for i in range(len(sol) - 1):
			comb = list(combinations(sol, i + 1))
			for j in comb:
				j = list(j)
				all_comb.append(j)
				
		all_comb = list(filter(machine_not_duplicate, all_comb))
		
		best_obj = float('inf')
		best_sol = []
		for comb in all_comb:
			sol = comb
			fsb, collision = feasible(s, p, b, sol, h)
			if fsb:
				# cost_none
				sol_cost = sum(cost[0])
				for i in sol:
					sol_cost = sol_cost - cost[0][i[0]] + sol_value_dict[i]

				if sol_cost < best_obj:
					best_obj = sol_cost
					best_sol = sol
		
		solution = Solution(s, p, b, best_sol, best_obj, h)
		return solution
		
	elif mode == "strategic_idle":
		new_s = list(s)
		shifted_s = list(s)
		while not fsb:
			coll_finish_time_list = [new_s[i[0]][i[1] - 1] + b for i in collision]
			
			latest = max(coll_finish_time_list)
			second_latest = sorted(coll_finish_time_list)[1]
			
			latest_machine = [collision[i][0] for i,val in enumerate(coll_finish_time_list) if val==latest]
			
			move_to_sec = []
			if len(latest_machine) != len(collision):
				move_to_sec = latest_machine
			
			# calculate cost and decide which to shift
			best_cost = float('inf')
			best_machine_to_shift = None
			for i, j in collision:
				s_to_shift = list(s[i])
				cur = 0
				for k in range(len(s_to_shift)):
					if k == j:
						if i in move_to_sec:
							cur = second_latest + b
						else:
							cur = latest + b
					s_to_shift[k] = cur
					cur += p[i][k]
					
					if k == len(s_to_shift) - 1: break
					if cur < s[i][k + 1]:
						cur = s[i][k + 1]
					
				shifted_s[i] = list(s_to_shift)
				
				# defect cost
				c_pick = rB[i] * sum(p[i][:j]) + rA[i] * sum(p[i][j:])
				# tardiness
				tardiness = 0
				for k in range(1, n[i] + 1):
					tardiness += max(0, shifted_s[i][k] + p[i][k] - d[i][k])
				c_pick += cT * tardiness
				
				if c_pick < best_cost:
					best_cost = c_pick
					best_machine_to_shift = i
			
			print(best_cost, best_machine_to_shift)
			
			# move and renew new_s
			
			
			# check feasibility
			'''
			fsb, collision = feasible(s, p, b, sol, h)
			if fsb:
			'''
			
			break
		
# 給雪燕的，只輸出opt和running time	
def algo_test(instance_path, mode="first_combinations", nth_best=2):
	inst = read_instance(instance_path, True)
	start_time = time.time()
	sol = algo(inst, mode)
	running_time = time.time() - start_time
	
	return sol.obj, running_time
