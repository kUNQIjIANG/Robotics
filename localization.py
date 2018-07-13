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
def move(p,U):
	l = len(p)
	q = [ pExact * p[(i-U)%l] 
		+ pOvershoot * p[(i-U-1)%l]
		+ pUndershoot * p[(i-U+1)%l] 
		for i in range(l)]
	return q

for k in range(len(motions)):
	# sense first then move 
	p = sense(p,measurements[k])
	p = move(p,motions[k])

print(p)




