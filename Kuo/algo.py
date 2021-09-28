from utils import read_instance, Solution, feasible_result, generate_result, generate_no_maintenance_result, visualize_result, calculate_result_cost
import time
from itertools import product
import copy
#import pickle

def algo(inst, mode="first_combinations", nth_best=2, time_limit=float('inf'), u_bar=float('inf')):
	m = inst.m
	h_bar = inst.h_bar
	n = inst.n
	rA = inst.rA
	rB = inst.rB
	h = inst.h
	b = inst.b
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
	elim_list = []
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
					cur += b[i]
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
	
	feasible_result(first_best_result, h, h_bar)
	
	fsb, collision = feasible_result(first_best_result, h, h_bar)
	
	# list of machines that "no maintenance is the best"
	count = 1
	for i in cost:
		if sorted(list(i.items()), key=lambda x: x[1])[0][0] == 0: elim_list.append(count)
		count += 1
	
	if fsb: return Solution(s, p, b, first_best_sol, first_best_cost, h, h_bar, first_best_result, d)
	
	#print(cost)
	#print(elim_list)
	
	
	if mode == "first_combinations":
		list_add_zero = [[i, 0] for i in first_best_sol]
		candidates = list(set(product(*list_add_zero)))
		
		best_sol = []
		best_cost = float('inf')
		best_result = []
		
		for candidate in candidates:
			candidate_result = generate_result(s, p, b, list(candidate))
			fsb, candidate_collision = feasible_result(candidate_result, h, h_bar)
			
			if fsb:
				candidate_cost = calculate_result_cost(candidate_result, d, rA, rB, cD, cT)
				if candidate_cost < best_cost:

					best_cost = candidate_cost
					best_sol = list(candidate)
					best_result = candidate_result
		'''	
		pickle_out = open("result.pickle", "wb")
		pickle.dump(Solution(s, p, b, best_sol, best_cost, h, h_bar, best_result, d), pickle_out)
		pickle_out.close()
		'''
		return Solution(s, p, b, best_sol, best_cost, h, h_bar, best_result, d)
		
	
	elif mode == "nth_combinations":
		sol_so_far = None
		obj_so_far = None
		result_so_far = None
		
		list_sorted = [sorted(list(i.items()), key=lambda x: x[1]) for i in cost]
		list_nth = first_best_sol
		
		list_nth = [[list_nth[j]] for j in range(len(list_nth))]
		
		start_time = time.time()
		
		for i in range(1, nth_best):
			for j in range(len(list_nth)):
				# eliminate machines that "no maintenance is the best"
				if j + 1 in elim_list: continue
				list_nth[j].append(list_sorted[j][i][0])
			
			candidates = list(set(product(*list_nth)))
			
			best_sol = []
			best_cost = float('inf')
			best_result = []
			
			for candidate in candidates:
				#print(time.time() - start_time)
				if time.time() - start_time > time_limit:
					if sol_so_far == None:
						result_inf = generate_no_maintenance_result(inst)
						obj_inf = calculate_result_cost(result_inf, inst.d, inst.rA, inst.rB, inst.cD, inst.cT)
						return Solution(s, p, b, [0]*(m + 1), obj_inf, h, h_bar, result_inf, d)
						
					return Solution(s, p, b, sol_so_far, obj_so_far, h, h_bar, result_so_far, d)

				candidate_result = generate_result(s, p, b, list(candidate))
				fsb, candidate_collision = feasible_result(candidate_result, h, h_bar)
				
				if fsb:
					candidate_cost = calculate_result_cost(candidate_result, d, rA, rB, cD, cT)
					if candidate_cost < best_cost:
						best_cost = candidate_cost
						best_sol = list(candidate)
						best_result = candidate_result
						
						obj_so_far = candidate_cost
						sol_so_far = list(candidate)
						result_so_far = candidate_result
					
			if  len(best_sol) != 0:
				return Solution(s, p, b, best_sol, best_cost, h, h_bar, best_result, d)
		
		list_add_zero = [list_nth[j] + [0] for j in range(len(list_nth))]
		candidates = list(set(product(*list_add_zero)))
		
		best_sol = []
		best_cost = float('inf')
		best_result = []
		
		for candidate in candidates:
			if time.time() - start_time > time_limit:
				return Solution(s, p, b, sol_so_far, obj_so_far, h, h_bar, result_so_far, d)
			candidate_result = generate_result(s, p, b, list(candidate))
			fsb, candidate_collision = feasible_result(candidate_result, h, h_bar)
			
			if fsb:
				candidate_cost = calculate_result_cost(candidate_result, d, rA, rB, cD, cT)
				if candidate_cost < best_cost:
					best_cost = candidate_cost
					best_sol = list(candidate)
					best_result = candidate_result
					
					obj_so_far = candidate_cost
					sol_so_far = list(candidate)
					result_so_far = candidate_result
		
		return Solution(s, p, b, best_sol, best_cost, h, h_bar, best_result, d)	
	
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
						schedule_shifted.append((cur, cur + b[i], True))
						cur += b[i]
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
			
			
			m_not_shifted = list(filter(lambda x: x[2], result[best_machine_to_shift - 1]))
			m_shifted = list(filter(lambda x: x[2], best_schedule_shifted))
			
			if m_shifted[0][1] - m_not_shifted[0][1] > u_bar:
				result[best_machine_to_shift - 1] = copy.deepcopy(result_no_maintenance[best_machine_to_shift - 1])
			
			else:
				result[best_machine_to_shift - 1] = result_no_maintenance[best_machine_to_shift - 1]
				obj_no_wait = calculate_result_cost(result, d, rA, rB, cD, cT)
				
				
				# move and renew new_s
				result[best_machine_to_shift - 1] = copy.deepcopy(best_schedule_shifted)
				obj_wait = calculate_result_cost(result, d, rA, rB, cD, cT)
				
				if obj_no_wait < obj_wait:
					result[best_machine_to_shift - 1] = copy.deepcopy(result_no_maintenance[best_machine_to_shift - 1])
			
			# check feasibility
			fsb, collision = feasible_result(result, h, h_bar)
		
		obj = calculate_result_cost(result, d, rA, rB, cD, cT)
		solution = Solution(s, p, b, [], obj, h, h_bar, result=result, d=d)
		
		return solution	

		
# 給雪燕的，只輸出opt和running time	
def algo_test(instance_path, mode="first_combinations", nth_best=2, time_limit=float('inf')):
	inst = read_instance(instance_path, True)
	start_time = time.time()
	sol = algo(inst, mode, nth_best, time_limit)
	running_time = time.time() - start_time
	
	return sol.obj, running_time
