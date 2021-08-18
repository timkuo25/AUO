from algo import algo, algo_test
from utils import visualize_result, read_solution, read_instance, generate_no_maintenance_result, calculate_result_cost
import itertools

inst = read_instance("m_6_h_3_n_max_15_1.txt", True)

#result = generate_no_maintenance_result(inst)
#obj = calculate_result_cost(result, inst.d, inst.rA, inst.rB, 3.8, inst.cT)

#print(obj)

r = algo(inst, "nth_combinations", 2)
visualize_result(r.result, r.obj, r.d)

#print (list(itertools.product([1,2], [0,6], [8, 9], [3, 6])))

'''
sol = algo(inst, "nth_combinations", 100)
visualize(sol)
'''

'''
sol = algo(inst, "strategic_idle")
visualize(sol)
'''


'''
sol = read_solution('solution_test.txt')
visualize(sol)
'''

'''
from algo import algo_test

obj, time = algo_test('m_6_h_3_n_max_15_1.txt', 'first_combinations')
print(obj, time)

obj, time = algo_test('m_6_h_3_n_max_15_1.txt', 'nth_combinations', 3)
print(obj, time)
'''