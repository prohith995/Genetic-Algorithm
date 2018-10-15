## Date : 19/11/2016
##By : Rohith.P
## Genetic Algorithm used to solve a scheduling problem

import random
import math

## Data

prep_time = [[0,70,55,60,50],[95,0,84,96,80],[34,40,0,39,30],[105,90,97,0,81],[30,38,28,40,0]]
event_time = [120,150,150,180,180]
n = 5

## Generating the initial population

def rand(n):
	u = random.uniform(0,1)
	for i in range(n):
		if u <= (i+1)*1.0/n : return i

def selectrand(n,m):
	a = [i for i in range(n)]
	b = []
	for i in range(m):
		r = rand(len(a))
		b.append(a[r])
		a.remove(a[r])
	return b

def selectrandfrom(arr,m):
	b = []
	for i in range(m):
		r = rand(len(arr))
		b.append(arr[r])
		arr.remove(arr[r])
	return b

def generate_member(n):
	status = [0]*n
	m = []
	while status != [1]*n :
		m1 = rand(n)
		if status[m1] == 0 :
			m.append(m1)
			status[m1] = 1
	return m

def preptime(m):
	t = 0
	for i in range(len(m)-1):
		t = t + prep_time[m[i+1]][m[i]]
	return t

def generate_child(pair,n):
	status = [0]*n
	child = []
	c1 = rand(n-1) # Choosing which link to go to the child
	c2 = rand(2) # Choosing from which parent it should go
	child.append(pair[c2][0][c1])
	child.append(pair[c2][0][c1+1])
	status[pair[c2][0][c1]] = 1
	status[pair[c2][0][c1+1]] = 1		

	count = 0
	while status != [1]*n :
		neigh = []
		j = child[-1]
		i1 = pair[0][0].index(j)
		if i1 > 0 and i1 < n-1 :
			neigh.extend([pair[0][0][i1+1],pair[0][0][i1-1]])
		else :
			if i1 == 0 :
				neigh.append(pair[0][0][i1+1])
			if i1 == n-1 :
				neigh.append(pair[0][0][i1-1])

		i2 = pair[1][0].index(j)
		if i2 > 0 and i2 < n-1 :
			neigh.extend([pair[1][0][i2+1],pair[1][0][i2-1]])
		else :
			if i2 == 0 :
				neigh.append(pair[1][0][i2+1])
			if i2 == n-1 :
				neigh.append(pair[1][0][i2-1])
				
		next = selectrandfrom(neigh,1)
		if status[next[0]] == 0:
			child.append(next[0])
			status[next[0]] = 1

		count = count + 1
		if count > 100 : return None		

	return child




population = 10  ## Initial Population
members = [] #[path,cost,generation]
generation = 0

## Generating the initial population of 5 members
for i in range(population):
	members.append([generate_member(n),0,generation])
	members[-1][1] = preptime(members[-1][0])

## Sorting
for i in range(len(members)) :
	for j in range(1,len(members)-i):
		if members[j][1] <	 members[j-1][1] :
			temp = members[j]
			members[j] = members[j-1]
			members[j-1] = temp

optimal_solution = members[0]

## Running various generations
for generation in range(100) :

	## Coupling
	parents = []
	parents.extend([members[i] for i in selectrand(6,4)])
	parents.extend([members[i+6] for i in selectrand(4,2)])

	pairs = [ [parents[i],parents[i+1]] for i in range(0,len(parents),2) ]


	## Generate new generation
	members = []

	for p in  pairs :
		members.extend([p[0],p[1]])
		ch = 0
		while ch < 2:
			child = generate_child(p,n)

			if rand(20) == 0 and child != None: #### Mutations
				s = rand(n-1)
				temp = child[s]
				child[s] = child[s+1]
				child[s+1] = temp

			if child != None and preptime(child) <= 1.4*optimal_solution[1] :
				members.append([child,preptime(child),generation])
				ch = ch + 1


	## Retiring older generation
	for i in members :
		if generation - i[2] > 3 :
			members.remove(i)
	
	## Creating new members if population is less
	while len(members) < 10 :
		members.append([generate_member(n),0,generation])
		members[-1][1] = preptime(members[-1][0])

	## Sorting
	for i in range(len(members)) :
		for j in range(1,len(members)-i):
			if members[j][1] <	 members[j-1][1] :
				temp = members[j]
				members[j] = members[j-1]
				members[j-1] = temp

	## Retaining best from the generation
	members = members[0:10]
	if (optimal_solution[1]>members[0][1]):
		optimal_solution = members[0]

	for i in members :
		print i
	print " Optimal solution after generation " + str(generation) + " = " + str(optimal_solution[1])