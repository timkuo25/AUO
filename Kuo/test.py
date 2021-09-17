from algo import algo, algo_test
from utils import visualize_result, read_solution, read_instance, generate_no_maintenance_result, calculate_result_cost
import itertools
import pickle


obj, runtime = algo_test("2021_4_18__60_schedule.txt", "nth_combinations", nth_best=3, time_limit=0.0000000000001)

print(obj)








#r = algo(inst, "waiting")
#visualize_result([], 0, r.result, r.obj, r.d)

#pickle_in = open("result.pickle", "rb")
#r = pickle.load(pickle_in)

#visualize_result([], 0, r.result, r.obj, r.d)