m = int()
h = int()
b = int()
n = []
cD = 1
cT = 1

rA = [0]
rB = [0]

s = [[0]]
p = [[0]]
d = [[0]]

file_name = "test.txt"
with open(file_name, 'r') as f:
	# m, h, b, n
	line = f.readline().split()
	m, h, b = [int(i) for i in line]
	
	line = f.readline().split()
	n = [0] + [int(i) for i in line]
	
	# rA, rB
	for _ in range(m):
		line = f.readline().split()
		rA.append(float(line[1]))
		rB.append(float(line[2]))

	for i in range(1, 1 + m):
		s_i = [0]
		p_i = [0]
		d_i = [0]
		for _ in range(n[i]):
			line = f.readline().split()
			s_i.append(int(line[2]))
			p_i.append(int(line[3]))
			d_i.append(int(line[4]))
		s.append(s_i)
		p.append(p_i)
		d.append(d_i)

print("n = ", n)
print("rA = ", rA)
print("rB = ", rB)
print("s = ", s)
print("p = ", p)
print("d = ", d)