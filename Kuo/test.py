from algo import algo, algo_test
from utils import visualize_result, read_solution, read_instance, generate_no_maintenance_result, calculate_result_cost
import itertools

inst = read_instance("m_8_maxh_4_n_max_20_h_0_b_0_1.txt", True)

#print(inst.b)
#result = generate_no_maintenance_result(inst)
#obj = calculate_result_cost(result, inst.d, inst.rA, inst.rB, inst.cD, inst.cT)

#algo(inst, "nth_combinations", 3)

#r = algo(inst, "first_combinations")
#r = algo(inst, "nth_combinations", 3)
#r = algo(inst, "nth_combinations", 5)
r = algo(inst, "waiting")

visualize_result([], 0, r.result, r.obj, r.d)
