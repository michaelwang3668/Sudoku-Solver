import common

#helpful, but not needed
class variables:
	counter=0

def used_in_row(sudoku,y,num):
	for i in range(9):
		if sudoku[y][i] == num:
			return True
	return False

def used_in_col(sudoku,x,num):
	for j in range(9):
		if sudoku[j][x] == num:
			return True
	return False

def used_in_box(sudoku, y, x, num):
	box_x = x//3
	box_y = y//3
	for j in range(box_y*3, box_y*3+3):
		for i in range(box_x*3, box_x*3+3):
			if sudoku[j][i] == num:
				return True
	return False


def check_safe(sudoku,y,x,num):
	row = not used_in_row(sudoku, y, num)
	col = not used_in_col(sudoku, x, num)
	#subtracting by modulo 3 gets us the location of top left box
	box = not used_in_box(sudoku,y,x,num)
	return row and col and box

def find_empty(sudoku,loc):
	# finding empty location
	for j in range(9):
		for i in range(9):
			if sudoku[j][i] == 0:
				loc[0] = j
				loc[1] = i
				return True
	return False

def sudoku_backtracking(sudoku):
	variables.counter = 0
	def loop(sudoku):
		variables.counter += 1
		loc = [-1,-1]
		#if no empty, board is finished
		if not find_empty(sudoku,loc):
			return True
		y,x = loc[0],loc[1]
		for num in range(1,10):
			if(check_safe(sudoku,y,x,num)):
				#make move if safe
				sudoku[y][x] = num
				#recursion
				if loop(sudoku):
				     return True
			     #take back move
			     #WE CAN CHOOSE TO NOT TAKE BACK MOVE (else) WHEN THERE IS
			     #RECURSION BECAUSE IT GETS OVERWRITTEN ANYWAY
				sudoku[y][x] = 0
		return False
	loop(sudoku)
	return variables.counter

def update_domain(domain,y,x,v):
	# v-1 because input 1 should be the first possible choice
	for count in range(9):
		domain[y][count][v-1] = -1
		domain[count][x][v-1] = -1

	box_x = x // 3
	box_y = y // 3
	for j in range(box_y * 3, box_y * 3 + 3):
		for i in range(box_x * 3, box_x * 3 + 3):
			domain[j][i][v-1] = -1

	return domain

def no_empty_domain(domain, sudoku):
	#an empty domain on a filled square does not matter
	for y in range(9):
		for x in range(9):
			if (1 not in domain[y][x]) and (sudoku[y][x] == 0):
				return False
	return True

def copy_domain(domain):
	result = [[[1 for k in range(9)] for j in range(9)] for i in range(9)]
	for j in range(9):
		for i in range(9):
			for k in range(9):
				 result[j][i][k] = domain[j][i][k]
	return result


def sudoku_forwardchecking(sudoku):
	variables.counter = 0
	# 1st index = y
	# 2nd index = x
	# 3rd index = value we input
	# (index 0 = input 1) !!!

	domain = [[[1 for k in range(9)] for j in range(9)] for i in range(9)]
	for j in range(9):
		for i in range(9):
			value = sudoku[j][i]
			if value != 0:
			     domain = update_domain(domain, j,i,value)

	def loop(sudoku, domain):
		variables.counter += 1

		loc = [-1, -1]
	     # if no empty, board is finished
		if not find_empty(sudoku, loc):
		     return True
		y, x = loc[0], loc[1]

		for num in range(1, 10):
			if (check_safe(sudoku, y, x, num)):

				old_domain = copy_domain(domain)
				sudoku[y][x] = num
				domain = update_domain(domain,y,x,num)

				if no_empty_domain(domain,sudoku):
					# recursion
					if loop(sudoku, domain):
						return True
				# IT IS IMPORTANT TO ALWAYS REVERT REGARDLESS OF RECURSION OR NOT, SINCE DOMAIN IS NOT
				# OVERWRITTEN LIKE BOARD IN BACKTRACKING. OTHERWISE, THE NEXT NUMBER WE INPUT WILL HAVE INCORRECT DOMAIN
				sudoku[y][x] = 0
				domain = old_domain
		return False

	loop(sudoku, domain)
	return variables.counter

