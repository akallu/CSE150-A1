#!/usr/bin/python -tt
import re
import sys
import copy
import time

class board:
  #constructs a board object which loads in a csv file of puzzle
  def __init__(self, filename):
    matrix = []
    with open(filename) as f:
      for line in f:
        matrix.append(map(int, line.split(',')))
    self.matrix = matrix
    self.coords = self.get_matrix_coords(matrix)
    self.m = len(matrix[0])
    self.n = len(matrix)
    self.goal_matrix = self.get_goal_matrix()
    self.goal_coords = self.get_matrix_coords(self.goal_matrix)

  def get_goal_matrix(self):
    goal_matrix = []
    j = 0
    for i in xrange(self.n):
      goal_matrix.append(range(j, j+self.m))
      j += self.m
    return goal_matrix

  # moves the 0 in the matrix according to the value of d
  # where d is either:
  # 0 - move left
  # 1 - move right
  # 2 - move up
  # 3 - move down
  def move(self, d):
    zc = self.coords[0][:]

    #move up
    if d == 2:
      #detect invalid out of board move
      if zc[0]-1 < 0:
        return False
      else:
        num = self.matrix[zc[0]-1][zc[1]]
        self.matrix[zc[0]][zc[1]] = num
        self.matrix[zc[0]-1][zc[1]] = 0
    #move down
    if d == 3:
      #detect invalid out of board move
      if zc[0]+1 > self.n-1:
        return False
      else:
        num = self.matrix[zc[0]+1][zc[1]]
        self.matrix[zc[0]][zc[1]] = num
        self.matrix[zc[0]+1][zc[1]] = 0
    #move left
    if d == 0:
      #detect invalid out of board move
      if zc[1]-1 < 0:
        return False
      else:
        num = self.matrix[zc[0]][zc[1]-1]
        self.matrix[zc[0]][zc[1]] = num
        self.matrix[zc[0]][zc[1]-1] = 0
    #move right
    if d == 1:
      #detect invalid out of board move
      if zc[1]+1 > self.m-1:
        return False
      else:
        num = self.matrix[zc[0]][zc[1]+1]
        self.matrix[zc[0]][zc[1]] = num
        self.matrix[zc[0]][zc[1]+1] = 0
    self.coords = self.get_matrix_coords(self.matrix)
    return True


  def get_matrix_coords(self, matrix):
    coords = {}
    i = j = 0
    for a in matrix:
      j = 0
      for num in a:
        coords[num] = [i, j]
        j += 1
      i += 1
    return coords

  def print_matrix(self, flag=None):
    if flag == None:
      ma = self.matrix[:]
    else:
      ma = self.goal_matrix[:]
    for a in ma:
      for num in a:
        print str(num) + '\t',
      print ''
    #print 'MISMATCH SCORE: ', self.mismatches(), '\n'
    print ''

  def print_coords(self, flag=None):
    if flag == None:
      c = self.coords
      ma = self.matrix
    else:
      c = self.goal_coords
      ma = self.goal_matrix
    for a in ma:
      for num in a:
        print str(c[num]) + '\t',
      print ''
  
  def mismatches(self):
    score = 0
    for i in xrange(self.n):
      for j in xrange(self.m):
        if self.matrix[i][j] != self.goal_matrix[i][j]:
          score += 1
    return score

  def manhattan(self):
    score = 0
    for i in xrange(self.n*self.m):
      #coordinates of i in current state
      a = self.coords[i][:]
      #coordinates of i in goal state
      b = self.goal_coords[i][:]
      score += abs(a[0]-b[0])+abs(a[1]-b[1])
    return score
      

  #returns a list of list of form (board_state, mismatch_score, manhattan_score, movement)
  #representing all valid moves possible from the previous state
  def make_all_states(self):
    valid_states = []
    moves = ['W', 'E', 'N', 'S']
    for i in xrange(4):
      tmp = copy.deepcopy(self)
      if tmp.move(i):
        #if a valid move occured, and zero is not in same position, we append:
        #the move state, its mismatch score, manhattan score, and the direction it moved
        valid_states.append([tmp, tmp.mismatches(), tmp.manhattan(), moves[i]])
    return valid_states

#Greedy Best First Search
#
#Parameters:
# b = initial board state
# h = string representing which heuristic to use
#
def GBF(b, h):
  it = 0
  if b.mismatches() == 0:
    return ('', 0, 0)
  if h == 'Manhattan':
    curr = min(b.make_all_states(), key=manhattan_helper)
  if h == 'Mismatch':
    curr = min(b.make_all_states(), key=mismatch_helper)
  path = curr[3]
  #while the current boards mismatch score does not equal zero
  #remember a mismatch score = 0 means goal state has been reached
  #it represents cutoff size
  while curr[1] != 0 and it < 1000:
    it += 1
    if h == 'Manhattan':
      curr = min(curr[0].make_all_states(), key=manhattan_helper)
    if h == 'Mismatch':
      curr = min(curr[0].make_all_states(), key=mismatch_helper)
    path += curr[3]
  if it >= 1000:
    return -1
  return (len(path), len(path)+1, path)

# Breadth First Search
def BFS(b):
  #current nodes
  c_nodes = b.make_all_states()
  #children nodes
  ch_nodes = []
  nodes_explored = 1
  nodes_expanded = 1
  if b.mismatches() == 0:
    return ('', 0, 0)

  #these moves signify that a descendant went back to an ancestor state
  return_to_parent_state = ['NS', 'SN', 'WE', 'EW']
  while True:
    #search through current nodes and see if there exists a solution
    for i in xrange(len(c_nodes)):
      #we found a solution, return it
      if c_nodes[i][1] == 0:
        return (len(c_nodes[i][3]), nodes_expanded+1, c_nodes[i][3])

    #we did not find a solution above, so we expand each of the nodes
    for i in xrange(len(c_nodes)):
        #make the children states of the current state
        tmp = c_nodes[i][0].make_all_states()
        

        #append parent's path to its children's path
        for j in xrange(len(tmp)):
          tmp[j][3] = c_nodes[i][3] + tmp[j][3]
          if len(tmp[j][3]) > 1:
            if not tmp[j][3][-2:] in return_to_parent_state:
              ch_nodes.append(tmp[j])
        nodes_expanded += 1

    #children nodes become the current nodes
    c_nodes = ch_nodes

dfs_node_count = 0
#Depth-limited Depth First Search
def DFS(b, limit):
  global dfs_node_count
  dfs_node_count = 1
  return rec_DFS('', b, int(limit))

#recursive DFS that does the heavy lifting
#A return of -1 signifies CUTOFF
#A return of -2 signifies FAILURE
def rec_DFS(path, b, limit):
  #these moves signify that a descendant went back to an ancestor state
  return_to_parent_state = ['NS', 'SN', 'WE', 'EW']

  global dfs_node_count
  #check if current node is solution
  if b.mismatches() == 0:
    return (len(path), dfs_node_count, path)
  #check if limit has been reached, return cutoff value if yes
  elif limit == 0:
    return -1
  else:
    #set cutoff variable to False
    cutoff = False
    #generate all possible moves from current state
    curr_nodes = b.make_all_states()
    for node in curr_nodes:
      if len(path) > 0:
        if path[-1]+node[3] in return_to_parent_state:
          curr_nodes.remove(node)

    for i in xrange(len(curr_nodes)):
      #append parent's path to its children's path
      curr_nodes[i][3] = path + curr_nodes[i][3]
      #increment number of expanded nodes
      dfs_node_count += 1
      #recursion happens here
      result = rec_DFS(curr_nodes[i][3], curr_nodes[i][0], limit-1)
      #check if result was cutoff, set cutoff if yes
      if result == -1:
        cutoff = True
      #check if result was a failure, if not, return result
      elif result != -2:
        return result
    if cutoff == True:
      #return cutoff
      return -1
    else:
      #return failure
      return -2

#Iterative Deepening Search
def IDS(b, lim):
  depth = 1
  while depth <= lim:
    result = rec_DFS('', b, depth)
    depth += 1
    if result != -1:
      return result

def print_solutions(t):
  if t > 0:
    print 'Sol. Length:\t', t[0]
    print 'Nodes Expanded:\t', t[1]
    print 'Sol. Path:\t', t[2]
  else:
    print 'Solution was not found'

def mismatch_helper(t):
  return t[1]
def manhattan_helper(t):
  return t[2]

def main():
  if len(sys.argv) < 3:
    print 'Usage:'
    print '> python board.py (puzzle file) (algorithm) [heuristic|depth]\n'
    sys.exit(1)
  b = board(sys.argv[1])
  alg = sys.argv[2]
  print 'INITIAL STATE:'
  b.print_matrix()

  if alg == 'Greedy':
    if len(sys.argv) < 4:
      print 'Heuristic not specified: use either "Manhattan" or "Mismatch"'
      print 'Usage:'
      print '> python board.py (puzzle file) (algorithm) (heuristic)\n'
      sys.exit(1)
    start = time.time()
    print 'Greedy Best First Search found solution:' 
    print_solutions(GBF(b, sys.argv[3]))
    print 'In time: ', time.time()-start, '\n'
  elif alg == 'A_Star':
    start = time.time()
    print 'A* Search found solution:' 
    print_solutions(A_Star(b, 'Mismatch'))
    print 'In time: ', time.time()-start, '\n'
  elif alg == 'BFS':
    start = time.time()
    print 'Breadth First Search found solution:' 
    print_solutions(BFS(b))
    print 'In time: ', time.time()-start, '\n'  
  elif alg == 'DFS':
    if len(sys.argv) < 4:
      print 'Depth not specified'
      print 'Usage:'
      print '> python board.py (puzzle file) (algorithm) (depth)\n'
      sys.exit(1)
    start = time.time()
    print 'Depth-limited Depth First Search found solution:'
    print_solutions(DFS(b, sys.argv[3]))
    print 'In time: ', time.time()-start, '\n'
  elif alg == 'IDS':
    start = time.time()
    print 'Iterative Deepening Search found solution:'
    print_solutions(IDS(b, int(sys.argv[3])))
    print 'In time: ', time.time()-start, '\n'
  else:
    print 'Usage:'
    print '> python board.py (puzzle file) (algorithm) [heuristic|depth]\n' 

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

