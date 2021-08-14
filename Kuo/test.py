from algo import algo, algo_test
from utils import visualize, read_solution, read_instance

'''
inst = read_instance("m_6_h_3_n_max_15_1.txt", True)
sol = algo(inst, "first_combinations")

#visualize(sol)
# print(sol, opt)


sol = read_solution('solution_test.txt')

visualize(sol)
'''

obj, time = algo_test('m_6_h_3_n_max_15_1.txt', 'first_combinations')
print(obj, time)

obj, time = algo_test('m_6_h_3_n_max_15_1.txt', 'nth_combinations', 3)
print(obj, time)