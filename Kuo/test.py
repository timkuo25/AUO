from algo import algo, algo_test
from utils import visualize_result, read_solution, read_instance, generate_no_maintenance_result, calculate_result_cost
import itertools

inst = read_instance("12_6_40_2_C.txt", True)

result = generate_no_maintenance_result(inst)
obj = calculate_result_cost(result, inst.d, inst.rA, inst.rB, inst.cD, inst.cT)

#r = algo(inst, "first_combinations")
#r = algo(inst, "nth_combinations", 3)
#r = algo(inst, "nth_combinations", 5)
r = algo(inst, "waiting")

visualize_result(result, obj, r.result, r.obj, r.d)