import numpy as np 

p = [0.2,0.2,0.2,0.2,0.2]
world = ['green','red','red','green','green']
measurements = ['red','green']
motions = [1,1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p,Z):
	q = []
	for i in range(len(p)):
		hit = (Z == world[i])
		q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
	# Normalize
	return np.array(q)/sum(q)

def sense2D(p,Z,world,sense_acc):
	q = np.ones_like(p)
	rows, cols  = q.shape
	
	for i in range(rows):
		for j in range(cols):
			hit = (Z == world[i,j])
			if (hit):
				q[i,j] = p[i,j] * (pHit * sense_acc + pMiss * (1- sense_acc))
			else:
				q[i,j] = p[i,j] * (pHit * (1- sense_acc) + pMiss * sense_acc)
	# Normalize
	return q/np.sum(q)

def move(p,U):
	l = len(p)
	q = [ pExact * p[(i-U)%l] 
		+ pOvershoot * p[(i-U-1)%l]
		+ pUndershoot * p[(i-U+1)%l] 
		for i in range(l)]
	return q

def move2D(p,U,p_move):
	q = np.ones_like(p)
	rows = q.shape[0]
	cols = q.shape[1]
	for i in range(rows):
		for j in range(cols):
			q[i,j] = p_move * p[(i-U[0])%rows][(j-U[1])%cols] + (1-p_move) * p[i,j]
	return q/np.sum(q)


# 1D
for k in range(len(motions)):
	# sense first then move 
	p = sense(p,measurements[k])
	p = move(p,motions[k])

# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localize(world,measurements,motions,sensor_right,p_move):
	if (len(measurements) != len(motions)):
		raise ValueError("len of measures should be same as motions")

	# initializes p to a uniform distribution over a grid of the same dimensions as colors
	pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
	p = np.array([[pinit for row in range(len(colors[0]))] for col in range(len(colors))])

    # >>> Insert your code here <<<
	for i in range(len(motions)):
		p = sense2D(p,measurements[i],world,sensor_right)
		p = move2D(p,motions[i],p_move)

	return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = np.array([['R','G','G','R','R'],
          			['R','R','G','R','R'],
          			['R','R','G','G','R'],
          			['R','R','R','R','R']])

#
# The essence is that the state matchs all 
# measures during the motions keeps the highest
# in the end, it is not compute the most likely path.
#

measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p) # displays your answer




