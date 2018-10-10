
class Sudo:
	def __init__(self, width):
		self.result = [[ 0 for i in range(width)] for i in range(width)]
		self.possible = [ [ [ i for i in range(1, width + 1)] for i in range(width) ] for i in range(width)]
		self.width = width


	def set(self, x, y, value):
		self.result[x][y] = value
		self.possible[x][y] = []

	def _getRemainPossible(self, current):
		res = []
		for i in range(1, self.width + 1):
			if i not in current:
				res.append(i)
		return res

	def _getUnion(self, current, coming):
		res = []
		for item in current:
			if item in coming:
				res.append(item)
		return res

	def setTarget(self, row, col):
		self.target = [row, col]




	def run(self):
		# get row possibles 
		iteration = 0
		while True:
			# get all possible result of each row for empty positions
			for row in range(self.width):
				current = []
				for col in range(self.width):
					if self.result[row][col] != 0:
						current.append(self.result[row][col])
				allPossible = self._getRemainPossible(current)

				for col in range(self.width):
					if self.result[row][col] != 0:
						continue
					union = self._getUnion(self.possible[row][col], allPossible)
					self.possible[row][col] = union

			# get all possible result of each col for empty positions
			for col in range(self.width):
				current = []
				for row in range(self.width):
					if self.result[row][col] != 0:
						current.append(self.result[row][col])
				allPossible = self._getRemainPossible(current)
				for row in range(self.width):
					if self.result[row][col] != 0:
						continue
					union = self._getUnion(self.possible[row][col], allPossible)
					self.possible[row][col] = union

			# decide the value of positions that has only one possible choices
			for row in range(self.width):
				for col in range(self.width):
					if len(self.possible[row][col]) == 1:
						self.result[row][col] = self.possible[row][col][0]
						self.possible[row][col] = []
			

			# for each row, if one possible value could only be input to a specific position, than it is
			for row in range(self.width):
				finished = []
				for col in range(self.width):
					if self.result[row][col] != 0:
						finished.append(self.result[row][col])
				remain = self._getRemainPossible(finished)
				for key in remain:
					keyCount = 0
					for col in range(self.width):
						if self.result[row][col] != 0:
							continue
						if key in self.possible[row][col]:
							keyCount += 1
					if keyCount == 1:
						for col in range(self.width):
							if self.result[row][col] != 0:
								continue
							if key in self.possible[row][col]:
								self.result[row][col] = key
								self.possible[row][col] = []
			# for each col, same as above
			for col in range(self.width):
				finished = []
				for row in range(self.width):
					if self.result[row][col] != 0:
						finished.append(self.result[row][col])
				remain = self._getRemainPossible(finished)
				for key in remain:
					keyCount = 0
					for row in range(self.width):
						if self.result[row][col] != 0:
							continue
						if key in self.possible[row][col]:
							keyCount += 1
					if keyCount == 1:
						print 'key =====' , key
						for row in range(self.width):
							if self.result[row][col] != 0:
								continue
							if key in self.possible[row][col]:
								self.result[row][col] = key
								self.possible[row][col] = []

			iteration += 1
			# if goes beyond max iterations or the target is found, break
			if  iteration > 10 or self.result[self.target[0]][self.target[1]] != 0:
				self._updatedSudoBoard()
				break


	def _updatedSudoBoard(self):
		for row in range(self.width):
			for col in range(self.width):
				if self.result[row][col] != 0:
					for tempCol in range(self.width):
						if self.result[row][col] in self.possible[row][tempCol]:
							self.possible[row][tempCol].remove(self.result[row][col])
					for tempRow in range(self.width):
						if self.result[row][col] in self.possible[tempRow][col]:
							self.possible[tempRow][col].remove(self.result[row][col])
		for row in range(self.width):
			for col in range(self.width):
				if len(self.possible[row][col]) == 1:
					self.result[row][col] = self.possible[row][col][0]
					self.possible[row][col] = []

	

	def _isValidRow(self, container):
		if 0 in container:
			return False
		else:
			for i in range(1, self.width + 1):
				if i not in container:
					return False
		return True

	def isValid(self):
		isValid = True
		# check if each row is a valid row
		for row in range(self.width):
			container = []
			for col in range(self.width):
				container.append(self.result[row][col])
			if self._isValidRow(container):
				continue
			else:
				isValid = False
				break
		# check if each rol is a valid col
		for col in range(self.width):
			container = []
			for row in range(self.width):
				container.append(self.result[row][col])
			if self._isValidRow(container):
				continue
			else:
				isValid = False
				break
		return isValid

	def _isValidTempSudo(self, tempSudo):
		sudo = tempSudo['sudo']
		for row in range(self.width):
			current = []
			for col in range(self.width):
				current.append(sudo[row][col])
			if not self._isValidRow(current):
				return False
		for col in range(self.width):
			current = []
			for row in range(self.width):
				current.append(sudo[row][col])
			if not self._isValidRow(current):
				return False
		return True

	def _isCompletePossibleSudo(self, possibleSudo):
		for sudo in possibleSudo:
			if not self._isValidTempSudo(sudo):
				return False
		return True

	def _updateTempSudoByPosition(self, tempSudo, row, col):
		res = []
		possibleValues = tempSudo['possible'][row][col]
		for key in possibleValues:
			newTempSudo = tempSudo
			newTempSudo['sudo'][row][col] = key
			newTempSudo['possible'][row][col] = []
			for tempCol in range(self.width):
				if key in newTempSudo['possible'][row][tempCol]:
					newTempSudo['possible'][row][tempCol].remove(key)
					if len(newTempSudo['possible'][row][tempCol]) == 1:
						newTempSudo['sudo'][row][tempCol] = newTempSudo['possible'][row][tempCol][0]
						newTempSudo['possible'][row][tempCol] = []
			for tempRow in range(self.width):
				if key in newTempSudo['possible'][tempRow][col]:
					newTempSudo['possible'][tempRow][col].remove(key)
					if len(newTempSudo['possible'][tempRow][col]) == 1:
						newTempSudo['sudo'][tempRow][col] = newTempSudo['possible'][tempRow][col][0]
						newTempSudo['possible'][tempRow][col] = []
			#print newTempSudo
			res.append(newTempSudo)
		return res


	def completeSudo(self):
		if self.isValid():
			return
		possibleSudo = [{'sudo': self.result, 'possible': self.possible}]
		while not self._isCompletePossibleSudo(possibleSudo):
			tempSudo = possibleSudo[0]
			possibleSudo = possibleSudo[1:]
			for row in range(self.width):
				for col in range(self.width):
					if len(tempSudo['possible'][row][col]) == 0:
						continue
					updatedSudo = self._updateTempSudoByPosition(tempSudo, row, col)
					possibleSudo.extend(updatedSudo)
		return possibleSudo



	def getResult(self):
		print self.result[self.target[0], self.target[1]]

	def printResult(self):
		#print self.possible
		revRange = sorted([ i for i in range(self.width)], reverse = True)
		for row in revRange:
			res = ''
			for col in range(self.width):
				res += str(self.result[row][col]) + ' '
			print res



sudo = Sudo(4)

# sudo.setTarget(1,3)
# sudo.set(0,4, 4)
# sudo.set(1,2, 5)
# sudo.set(1,4, 3)
# sudo.set(2,0, 1)
# sudo.set(2,2, 2)
# sudo.set(2,4, 5)
# sudo.set(3,0, 5)
# sudo.set(3,3, 3)
# sudo.set(3,4, 2)
# sudo.set(4,0, 3)

# sudo.setTarget(0,1)
# sudo.set(0,0, 3)
# sudo.set(0,4, 4)
# sudo.set(1,0, 4)
# sudo.set(1,3, 3)
# sudo.set(1,4, 1)
# sudo.set(2,3, 2)
# sudo.set(3,1, 5)
# sudo.set(4,1, 4)
# sudo.set(4,2, 3)


# sudo.setTarget(3,1)
# sudo.set(0,0, 4)
# sudo.set(1,3, 1)
# sudo.set(2,1, 2)
# sudo.set(2,2, 1)
# sudo.set(2,3, 4)
# sudo.set(3,2, 2)

sudo.setTarget(2,1)
sudo.set(0,0, 3)
sudo.set(1,0, 2)
sudo.set(1,3, 4)
sudo.set(2,2, 3)
sudo.set(2,3, 2)
sudo.set(3,0, 1)

sudo.run()
sudo.completeSudo()

sudo.printResult()
