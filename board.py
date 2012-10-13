#!/usr/bin/python -tt
import re
import sys
import copy

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
        self.coords[0] = [zc[0]-1, zc[1]]
        self.coords[num] = zc
    #move down
    if d == 3:
      #detect invalid out of board move
      if zc[0]+1 > self.n-1:
        return False
      else:
        num = self.matrix[zc[0]+1][zc[1]]
        self.matrix[zc[0]][zc[1]] = num
        self.matrix[zc[0]+1][zc[1]] = 0
        self.coords[0] = [zc[0]+1, zc[1]]
        self.coords[num] = zc
    #move left
    if d == 0:
      #detect invalid out of board move
      if zc[1]-1 < 0:
        return False
      else:
        num = self.matrix[zc[0]][zc[1]-1]
        self.matrix[zc[0]][zc[1]] = num
        self.matrix[zc[0]][zc[1]-1] = 0
        self.coords[0] = [zc[0], zc[1]-1]
        self.coords[num] = zc
    #move right
    if d == 1:
      #detect invalid out of board move
      if zc[1]+1 > self.m-1:
        return False
      else:
        num = self.matrix[zc[0]][zc[1]+1]
        self.matrix[zc[0]][zc[1]] = num
        self.matrix[zc[0]][zc[1]+1] = 0
        self.coords[0] = [zc[0], zc[1]+1]
        self.coords[num] = zc
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
    print 'MISMATCH SCORE: ', self.mismatches(), '\n'

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

  #returns a list of tuples of form (board_state, mismatch_score, movement)
  #representing all valid moves possible from the previous state
  def make_all_states(self):
    valid_states = []
    moves = ['W', 'E', 'N', 'S']
    for i in xrange(4):
      tmp = copy.deepcopy(self)
      if tmp.move(i):
        valid_states.append((tmp, tmp.mismatches(), moves[i]))
    return valid_states

#where b is the initial board
def greedy_best_first(b):
  curr = min(b.make_all_states(), key=helper)
  path = curr[2]
  while curr[1] != 0:
    curr = min(curr[0].make_all_states(), key=helper)
    path += curr[2]
  return path
    
  
def helper(t):
  return t[1]

def main():
  b = board(sys.argv[1])
  print 'INITIAL STATE:'
  c = copy.deepcopy(b)
  b.print_matrix()
  '''c.move(0)
  c.print_matrix()
  c = copy.deepcopy(b)
  c.move(1)
  c.print_matrix()
  c = copy.deepcopy(b)
  c.move(2)
  c.print_matrix()
  c = copy.deepcopy(b)
  c.move(3)
  c.print_matrix()'''

  print greedy_best_first(b)
  

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

