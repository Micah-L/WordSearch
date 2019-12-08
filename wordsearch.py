#!/usr/bin/env python
from collections import defaultdict
import sys

class WordSearch:
	def __init__(self, grid, wrap_mode):
		self.grid=grid
		self.wrapping = True if wrap_mode.upper() == "WRAP" else False
		self.rows = len(grid)
		self.cols = len(grid[0])
		
		# First build hash table of all 2-char prefixes
		# Dictionary contains prefix:[list of (position,direction)]
		self.pref_map = defaultdict(list) # so default values are []
		if self.wrapping: # Then all directions are always valid
			directions={(1,0),(0,1),(1,1),(-1,1)} # We only use 4 because we will just reverse the words and search for those too
			for x in range(self.rows): 
				for y in range(self.cols):
					self.pref_map[grid[x][y]] = ((x,y),(0,0)) # In case of 1 letter words
					for dx,dy in directions:
						self.pref_map[grid[x][y] + grid[(x+dx) % self.rows][(y+dy) % self.cols]].append(((x,y), (dx, dy)))
						
						
		else: # Divide the loop into parts where each direction is valid instead of having to check each time
			directions={(1,0),(0,1),(1,1)}
			x = 0
			for y in range(self.cols-1):
				self.pref_map[grid[x][y]] = ((x,y),(0,0)) # In case of 1 letter words
				for dx, dy in directions:
					self.pref_map[grid[x][y] + grid[x+dx][y+dy]].append(((x,y), (dx, dy)))
			directions={(1,0),(0,1),(1,1),(-1,1)}
			for x in range(1,self.rows-1):
				for y in range(self.cols - 1):
					self.pref_map[grid[x][y]] = ((x,y),(0,0)) # In case of 1 letter words
					for dx, dy in directions:
						self.pref_map[grid[x][y] + grid[x+dx][y+dy]].append(((x,y), (dx, dy)))
			directions={(0,1),(-1,1)}		
			x = self.rows - 1
			for y in range(self.cols-1):
				self.pref_map[grid[x][y]] = ((x,y),(0,0)) # In case of 1 letter words
				for dx, dy in directions:
					self.pref_map[grid[x][y] + grid[x+dx][y+dy]].append(((x,y), (dx, dy)))
			directions = {(1,0)}
			y = self.cols - 1
			for x in range(self.rows-1):
				self.pref_map[grid[x][y]] = ((x,y),(0,0)) # In case of 1 letter words
				for dx, dy in directions:
					self.pref_map[grid[x][y] + grid[x+dx][y+dy]].append(((x,y), (dx, dy)))
			self.pref_map[grid[self.rows-1][self.cols-1]] = ((self.rows-1,self.cols-1),(0,0)) # In case of 1 letter words
		
	# returns a pair (start, end) if found. Otherwise None	
	def find_word(self,word):
		if len(word) == 1:
			try:
				return (self.pref_map[word][0],self.pref_map[word][0])
			except (KeyError, IndexError):
				return None
		def find_word_one_way(word):	
			pref = word[0:2]		
			for position, direction in self.pref_map[pref]:
				end = (position[0] + (len(word) - 1)*direction[0], position[1] + (len(word) - 1)*direction[1])
				if word == pref:
					return (position, (end[0] % self.rows, end[1] % self.cols) )
				if self.wrapping or (end[0] in range(self.rows) and end[1] in range(self.cols)):
					for n in range(2, len(word)):
						x = (position[0] + n*direction[0]) % self.rows
						y = (position[1] + n*direction[1]) % self.cols
						if self.grid[x][y] != word[n]: 
							break
						return (position, (end[0] % self.rows, end[1] % self.cols) )
			return None
		result = find_word_one_way(word)
		if result == None:
			result = find_word_one_way(word[::-1])
			if result == None:
				return result
			else:
				return (result[1], result[0])
		else:
			return result
				

# Assumes the input file looks like this:
# numrows numcols
# abcd
# efgh
# . . .  
# zzzz
# WRAP_MODE (i.e. "WRAP" or "NO_WRAP")
# P (an integer)
# word_1
# word_2
# . . .
# word_P
if __name__ == "__main__":
	if len(sys.argv) > 1:
		with open(sys.argv[1],"r") as fp:
			rows, cols = [int(x) for x in next(fp).strip().split()]
			grid = []
			for _ in range(rows):
				grid.append([x for x in next(fp).strip()])
			wrap_mode = next(fp).strip()
			numwords = int(next(fp).strip())
			wordlist = []
			for _ in range(numwords):
				wordlist.append(next(fp).strip())
		ws = WordSearch(grid,wrap_mode)
		for word in wordlist:
			result = ws.find_word(word)
			if result == None:
				print("NOT FOUND")
			else:
				print("{} {}".format(result[0],result[1]))
	else:
		print("No input file specified.\nUsage: python {} input_file".format(sys.argv[0]))
		raise SystemExit

