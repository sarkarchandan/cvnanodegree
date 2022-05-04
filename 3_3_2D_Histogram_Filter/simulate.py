from typing import List, Tuple
import localizer 
import random
from copy import deepcopy
from matplotlib import pyplot as plt


class Simulation(object):

	grid: List[List[str]]
	beliefs: List[List[float]]
	height: int
	width: int
	blur: float
	p_hit: float
	p_miss: float
	incorrect_sense_probability: float
	colors: List[str]
	num_colors: int
	true_pose: Tuple[int, int]
	prev_pose: Tuple[int, int]
	X: List[int]  # Maintains x-coordinate of the location of the robot
	Y: List[int]  # Maintains y-coordinate of the location of the robot
	P: List[float]  # Denotes certainty of the robot about its location


	def __init__(self, grid: List[List[str]], blur: float, p_hit: float, start_pos: Tuple[int, int] = None) -> None:
		"""Initializes Simulation

		Args:
			grid: 2D grid representing the robot world
			blur: 
			p_hit:
			start_pos: Tuple
		"""
		self.grid = grid
		self.beliefs = localizer.initialize_beliefs(self.grid)
		self.height = len(grid)
		self.width  = len(grid[0])
		self.blur   = blur
		self.p_hit = p_hit
		self.p_miss = 1.0
		self.incorrect_sense_probability = self.p_miss / (p_hit + self.p_miss)
		self.colors = self.get_colors()
		self.num_colors = len(self.colors)
		# If starting position of the robot is given we initialize of the 
		# true location of the robot in the world accordingly, otherwise 
		# the starting location is the center of the world.
		if not start_pos:
			self.true_pose = (self.height // 2, self.width // 2)
		else:
			self.true_pose = start_pos
		self.prev_pose = self.true_pose
		self.prepare_visualizer()

	def prepare_visualizer(self) -> None:
		"""Initializes the properties, which would maintain the move coordinates and 
		associated uncertainties of the robot as it moves.
		"""
		self.X = []
		self.Y = []
		self.P = []

	def get_colors(self) -> List[str]:
		"""Creates a list of all colors from the  robot world

		Returns:
			All colors as the list of the strings
		"""
		all_colors: List[str] = []
		for row in self.grid:
			for cell in row:
				if cell not in all_colors:
					all_colors.append(cell)
		return all_colors

	def sense(self) -> None:
		"""Implements the belief state update logic for the robot. It 
		invokes the sense method, which simulates a sensor measurement 
		with some possible uncertainties / errors. Then it delegates 
		the computation of new belief state to the localizer passing 
		on the sensor measurement.
		"""
		color: str = self.get_observed_color()
		beliefs: List[List[float]] = deepcopy(self.beliefs)
		new_beliefs: List[List[float]] = localizer.sense(
			color, self.grid, beliefs, self.p_hit, self.p_miss
		)
		if not new_beliefs or len(new_beliefs) == 0:
			print("NOTE! The robot doesn't have a working sense function at this point.")
			self.beliefs = beliefs
		else:
			self.beliefs = new_beliefs

	def move(self, dy: int, dx: int) -> None:
		"""Moves the robot in its grid world w.r.t. the provided 
		steps for y and x directions. This actually updates the belief 
		of the robot about its location in the world.

		Args:
			dy: An integer step (-1, 0 or 1) to take in y direction
			dx: An integer step (-1, 0 or 1) to take in x direction
		"""
		# Derive new vertical index by adding the step to currently 
		# known true location, while ensuring that the new location 
		# stays withing the dimension of the world
		new_y = (self.true_pose[0] + dy) % self.height
		# Derive new horizontal index similarly
		new_x = (self.true_pose[1] + dx) % self.width
		# Make currently known location as the previously known location 
		# as the current location is about to change
		self.prev_pose = self.true_pose
		# Update the current position
		self.true_pose = (new_y, new_x)
		# Update the belief of the robot about its location in its world
		# and maintan the same in the current state
		beliefs = deepcopy(self.beliefs)
		new_beliefs = localizer.move(dy, dx, beliefs, self.blur)
		self.beliefs = new_beliefs


	def get_observed_color(self) -> str:
		"""Implements a logic to simulate some uncertainties
		in the sensor measurement of the robot. Grid cells are 
		marked with colors. This implementation tries to implement 
		a logic, with which the robot may or may not see the correct 
		color.

		Returns:
			An observed color as string value
		"""
		# Get the current coordinates of the robot 
		# and determine color associated with that 
		# coordinate position.
		y,x = self.true_pose
		true_color: str = self.grid[y][x]
		# Implements a bit of uncertainty and error in the 
		# observations of the robot. If the following condition 
		# is true then simulator makes an attempt to get color 
		# which may or may not be true color. If the condition 
		# is false it chooses the true color.
		if random.random() < self.incorrect_sense_probability:
			possible_colors: List[str] = []
			# Iterate over all possible colors and makes an attempt 
			# against choosing the true color by populating the 
			# possible colors with underlying condition and then make 
			# a random choice.
			for color in self.colors:
				if color != true_color and color not in possible_colors:
					possible_colors.append(color)
			color: str = random.choice(possible_colors)
		else:
			color = true_color
		return color

	def show_beliefs(self,past_turn: bool = False) -> None:
		"""Visualizes the belief of the robot about its location 
		in its world.

		Args:
			past_turn: If the historic turns taken by the robots 
			need to be shown.
		"""
		# Copy previously maintained state about the location of the robot
		# In this case this state was maintaining all the previous positions 
		# of the robot and its certainties about its locations.
		if past_turn:
			X: List[int] = deepcopy(self.X)
			Y: List[int] = deepcopy(self.Y)
			P: List[float] = deepcopy(self.P)
		# Clean up the previously maintained state before refreshing he same 
		# with the current belief
		del(self.X[:])
		del(self.Y[:])
		del(self.P[:])
		# Updates the state of the location of the robot with the current belief
		for y, row in enumerate(self.beliefs):
			for x, belief in enumerate(row):
				self.X.append(x)
				self.Y.append(self.height-y-1) # puts large y ABOVE small y
				self.P.append(5000.0 * belief)

		plt.figure()
		# If past_turn is True, scatter plot should include the previous position
		# the robot as well. If False only the true position of the robot would be 
		# shown.
		if past_turn:
			plt.scatter(X, Y, s=P, alpha=0.3,color="blue")
			plt.scatter([self.prev_pose[1]], [self.height-self.true_pose[0]-1], color='red', marker="*", s=200, alpha=0.3)
		plt.scatter(self.X,self.Y,s=self.P,color="blue")
		plt.scatter([self.true_pose[1]], [self.height-self.true_pose[0]-1], color='red', marker="*", s=200)
		plt.show()

	@staticmethod
	def random_move() -> Tuple[int, int]:
		"""Randomly determines a step to take. This means 
		randomly choosing a frontal or backward step or 
		staying stationary both in x, y directions.

		Returns:
			A tuple of randomly chosen steps
		"""
		dy = random.choice([-1,0,1])
		dx = random.choice([-1,0,1])
		return dy,dx

	def run(self, num_steps: int = 1) -> None:
		"""Executes one step of the robot movement simulation.
		Takes a number of steps. In each step the robot makes 
		a sensor measurement to compute posterior probability 
		distribution about its location (gain information), which 
		decreases uncertainty and then it takes a random move 
		(loss information), which increases uncertainty.

		Args:
			num_steps: Number of steps to take 
			for the robot.
		"""
		for i in range(num_steps):
			self.sense()
			dy, dx = self.random_move()
			self.move(dy,dx)
