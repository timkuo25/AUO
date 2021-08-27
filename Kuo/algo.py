from utils import read_instance, Solution, feasible_result, generate_result, generate_no_maintenance_result, visualize_result, calculate_result_cost
import time
from itertools import product
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
	#cD = 3.8
	#cT = 1
	#rB = [i * 100 for i in rB]
	#h = 1
	
	collision = []
	cost = []
	first_best_sol = []
	result_no_maintenance = generate_no_maintenance_result(inst)
	
	
	for i in range(1, m + 1):
		cost_dict = {}
		candidate = 0
		best_c = float('inf')
		c_none = 0

		# defect cost
		c_none += rB[i] * sum(p[i]) * cD
		
		# tardiness
		for j in range(1, n[i] + 1):
			c_none += cT * max(0, s[i][j] + p[i][j] - d[i][j])

		best_c = c_none
		cost_dict[0] = c_none
		
		for j in range(1, n[i] + 1):
			# defect cost
			c_pick = cD * (rB[i] * sum(p[i][:j]) + rA[i] * sum(p[i][j:]))
			
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
			cost_dict[j] = c_pick
			
			
			if c_pick < best_c:
				best_c = c_pick
				candidate = j
				
		cost.append(cost_dict)
		first_best_sol.append(candidate)
	
	first_best_result = generate_result(s, p, b, first_best_sol)
	first_best_cost = calculate_result_cost(first_best_result, d, rA, rB, cD, cT)
	#visualize_result([], 0, first_best_result, first_best_cost, d)
	
	fsb, collision = feasible_result(first_best_result, h)
	
	if fsb: return Solution(s, p, b, first_best_sol, first_best_cost, h, first_best_result, d)
	
	
	if mode == "first_combinations":
		list_add_zero = [[i, 0] for i in first_best_sol]
		candidates = list(set(product(*list_add_zero)))
		
		best_sol = []
		best_cost = float('inf')
		best_result = []
		
		for candidate in candidates:
			candidate_result = generate_result(s, p, b, list(candidate))
			fsb, candidate_collision = feasible_result(candidate_result, h)
			
			if fsb:
				candidate_cost = calculate_result_cost(candidate_result, d, rA, rB, cD, cT)
				if candidate_cost < best_cost:
					best_cost = candidate_cost
					best_sol = list(candidate)
					best_result = candidate_result
		
		
		return Solution(s, p, b, best_sol, best_cost, h, best_result, d)
		
	
	elif mode == "nth_combinations":
		list_sorted = [sorted(list(i.items()), key=lambda x: x[1]) for i in cost]
		list_nth = first_best_sol
		
		for i in range(1, nth_best):
			if i == 1:
				list_nth = [[list_nth[j]] + [list_sorted[j][i][0]] for j in range(len(list_nth))]
			else:
				list_nth = [list_nth[j] + [list_sorted[j][i][0]] for j in range(len(list_nth))]
			
			candidates = list(set(product(*list_nth)))
			
			best_sol = []
			best_cost = float('inf')
			best_result = []
			
			for candidate in candidates:
				candidate_result = generate_result(s, p, b, list(candidate))
				fsb, candidate_collision = feasible_result(candidate_result, h)
				
				if fsb:
					candidate_cost = calculate_result_cost(candidate_result, d, rA, rB, cD, cT)
					if candidate_cost < best_cost:
						best_cost = candidate_cost
						best_sol = list(candidate)
						best_result = candidate_result
					
			if  len(best_sol) != 0:
				return Solution(s, p, b, best_sol, best_cost, h, best_result, d)
		
		
		list_add_zero = [list_nth[j] + [0] for j in range(len(list_nth))]
		candidates = list(set(product(*list_add_zero)))
		
		best_sol = []
		best_cost = float('inf')
		best_result = []
		
		for candidate in candidates:
			candidate_result = generate_result(s, p, b, list(candidate))
			fsb, candidate_collision = feasible_result(candidate_result, h)
			
			if fsb:
				candidate_cost = calculate_result_cost(candidate_result, d, rA, rB, cD, cT)
				if candidate_cost < best_cost:
					best_cost = candidate_cost
					best_sol = list(candidate)
					best_result = candidate_result
		
		return Solution(s, p, b, best_sol, best_cost, h, best_result, d)
				
	
	elif mode == "waiting":
		while not fsb:
			coll_finish_time_list =[]
			result = first_best_result
			#visualize_result([], 0, first_best_result, first_best_cost, d)
			
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
			
			
			result[best_machine_to_shift - 1] = result_no_maintenance[best_machine_to_shift - 1]
			obj_no_wait = calculate_result_cost(result, d, rA, rB, cD, cT)
						
			# move and renew new_s
			result[best_machine_to_shift - 1] = copy.deepcopy(best_schedule_shifted)
			obj_wait = calculate_result_cost(result, d, rA, rB, cD, cT)
			
			if obj_no_wait < obj_wait:
				result[best_machine_to_shift - 1] = copy.deepcopy(result_no_maintenance[best_machine_to_shift - 1])
			
			# check feasibility
			fsb, collision = feasible_result(result, h)
		
		obj = calculate_result_cost(result, d, rA, rB, cD, cT)
		solution = Solution(s, p, b, [], obj, h, result=result, d=d)
		
		return solution	
		
		
# 給雪燕的，只輸出opt和running time	
def algo_test(instance_path, mode="first_combinations", nth_best=2):
	inst = read_instance(instance_path, True)
	start_time = time.time()
	sol = algo(inst, mode, nth_best)
	running_time = time.time() - start_time
	
	return sol.obj, running_time
