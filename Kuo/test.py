from algo import algo1
from utils import visualizer, feasibility_checker, read_solution

#opt, running_time = algo1("test.txt")

#visualizer(s, p, b, sol)

#print(feasibility_checker(s, p, b, sol, h))

s, p, b, h, opt, sol = read_solution('test.txt')
print(s, p, b, h, opt, sol)