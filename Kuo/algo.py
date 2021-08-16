from utils import read_instance, feasible, Solution, machine_not_duplicate, feasible_result
import time
from itertools import combinations
import copy

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
	result = []
	result_no_maintenance = []
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
	
	
	sol_cpy = list(sol)
	
	for i in range(1, m + 1):
		result_i = []
		cur = 0
		for j in range(1, n[i] + 1):
			if cur < s[i][j]: cur = s[i][j]
			result_i.append((cur, cur + p[i][j], False))
			cur = cur + p[i][j]
		result.append(result_i)
	
	result_no_maintenance = copy.deepcopy(result)
	
	
	for i, j in sol:
		result[i - 1].insert(j - 1, (s[i][j - 1] + p[i][j - 1], s[i][j - 1] + p[i][j - 1] + b, True))
		cur = s[i][j - 1] + p[i][j - 1] + b
		
		for k in range(j, len(result[i - 1])):
			if cur < result[i - 1][k][0]:
				cur = result[i - 1][k][0]
			result[i - 1][k] = (cur, cur + result[i - 1][k][1] - result[i - 1][k][0], False)
			cur = cur + result[i - 1][k][1] - result[i - 1][k][0]
	
	#fsb, collision = feasible_result(result, h)
	obj_none = sum(cost[0])
	fsb, collision = feasible(s, p, b, sol, h)

	
	if fsb:
		obj = sum(cost[1])
		solution = Solution(s, p, b, sol, obj, obj_none, h, result_no_maintenance, d=d)
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
		
		solution = Solution(s, p, b, best_sol, best_obj, obj_none, h, result_no_maintenance, d=d)
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
		
		solution = Solution(s, p, b, best_sol, best_obj, obj_none, h, result_no_maintenance, d=d)
		return solution
		
	elif mode == "strategic_idle":
	
		while not fsb:
			coll_finish_time_list =[]
			
			for i in collision:
				coll_finish_time_list.append(result[i[0] - 1][i[1] - 1][1])
			
			latest = max(coll_finish_time_list)
			second_latest = sorted(coll_finish_time_list)[1]
				
			latest_machine = [collision[i][0] for i,val in enumerate(coll_finish_time_list) if val==latest]
			

			move_to_sec = []
			if len(latest_machine) != len(collision):
				move_to_sec = latest_machine
			
			
			# calculate cost and decide which to shift
			

			lowest_cost_increased = float('inf')
			best_machine_to_shift = None
			best_schedule_shifted = None
			
			for i, j in collision:
				cost_not_shifted = 0
				cost_shifted = 0
				schedule_not_shifted = list(filter(lambda x: not x[2], result[i - 1]))
				schedule_shifted = []
				
				cost_not_shifted = sum([max(0, schedule_not_shifted[k][1] - d[i][k + 1]) for k in range(len(schedule_not_shifted))])
				
				cur = 0
				for k in range(n[i] + 1):
					if k + 1 == j:
						if i in move_to_sec:
							cur = second_latest
						else:
							cur = latest
						schedule_shifted.append((cur, cur + b, True))
						cur += b
					else:
						schedule_shifted.append((cur, cur + result[i - 1][k][1] - result[i - 1][k][0] , False))
						cur += result[i - 1][k][1] - result[i - 1][k][0]
					
					if k == n[i]: break
					if cur < result[i - 1][k + 1][0]:
						cur = result[i - 1][k + 1][0] 
				
				filtered_schedule_shifted = list(filter(lambda x: not x[2], schedule_shifted))
				cost_shifted = sum([max(0, filtered_schedule_shifted[k][1] - d[i][k + 1]) for k in range(len(schedule_not_shifted))])
				
				cost_increased = cost_shifted - cost_not_shifted
				if cost_increased < lowest_cost_increased:
					lowest_cost_increased = cost_increased
					best_machine_to_shift = i
					best_schedule_shifted = copy.deepcopy(schedule_shifted)
			
			
			# move and renew new_s
			result[best_machine_to_shift - 1] = copy.deepcopy(best_schedule_shifted)
			
			
			# check feasibility
			fsb, collision = feasible_result(result, h)
		
		sol = []
		obj = 0
		for i in range(m):
			# defect cost
			maintain = False
			for j in range(len(result[i])):
				if result[i][j][2]:
					sol.append((i + 1, j + 1))
					obj += (rB[i + 1] * sum(p[i + 1][:j + 1]) + rA[i + 1] * sum(p[i + 1][j + 1:])) * cD
					maintain = True
					break
			if not maintain:
				obj += rB[i + 1] * sum(p[i + 1]) * cD
				
			# tardiness cost
			filtered_schedule = list(filter(lambda x: not x[2], result[i]))
			
			obj += cT * sum([max(0, filtered_schedule[k][1] - d[i + 1][k + 1]) for k in range(n[i + 1])])
		
		solution = Solution(s, p, b, sol, obj, obj_none, h, result_no_maintenance, result=result, d=d)
		return solution
	
		
# 給雪燕的，只輸出opt和running time	
def algo_test(instance_path, mode="first_combinations", nth_best=2):
	inst = read_instance(instance_path, True)
	start_time = time.time()
	sol = algo(inst, mode)
	running_time = time.time() - start_time
	
	return sol.obj, running_time
