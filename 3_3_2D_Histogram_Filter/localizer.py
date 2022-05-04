import pdb
from typing import List
from helpers import normalize, blur


def initialize_beliefs(grid: List[List[float]]) -> List[List[float]]:
    """Initializes the belief of the robot with uniform probability 
    distribution. Belief has the same shape of 2D robot world.

    Args:
        grid: 2D grid representing the Robot world
    
    Returns: 
        Uniform probability distribution of the 
        same shape of 2D robot world
    """
    # TODO: Refactor with NumPy
    # Derive the height width and area from the list of lists
    height: int = len(grid)
    width: int = len(grid[0])
    area: int = height * width
    # Derive the uniform probability by dividing the total 
    # probability 1.0 by area.
    belief_per_cell: float = 1.0 / area
    beliefs: List[List[float]] = []
    # Create the uniform probability distribution having the 
    # same shape as with robot world.
    for _ in range(height):
        row: List[float] = []
        for _ in range(width):
            row.append(belief_per_cell)
        beliefs.append(row)
    return beliefs

def sense(color: str, grid: List[List[float]], beliefs: List[List[float]], p_hit: float, p_miss: float) -> List[List[float]]:
    """Implements the sensor measurement step. It takes into account the world, current belief of the robot 
    as well as its sensor measurement (color) and updates prior probability distribution (beliefs) to the 
    posterior probability distribution (new_beliefs).

    Args:
        color: Observation by the robot i.e. the sensor measurement
        grid: The robot world as list of lists
        beliefs: The prior probability distribution about the location of the robot
        p_hit: Factor to consider if the measurement is correct
        p_miss: Factor to consider if the measurement is incorrect

    Returns:
        New beliefs after taking the sensor measurement into account i.e. the posterior
        probability distribution as list of lists
    """
    new_beliefs: List[List[float]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    for i in range(height):
        row: List[float] = []
        for j in range(width):
            hit: int = (grid[i][j] == color)
            prior: float = beliefs[i][j]
            posterior: float = (prior * (hit * p_hit + (1 - hit) * p_miss))
            row.append(posterior)
        new_beliefs.append(row)
    return normalize(new_beliefs)

def move(dy: int, dx: int, beliefs: List[List[float]], blurring: float) -> List[List[float]]:
    """Implements the move step. This method shifts the cell values as the robot 
    takes a step to a given x and y directions.

    Args:
        dy: Step to take in the vertical direction
        dx: Step to take in the horizontal direction
        beliefs: Current beliefs of the robot about its location
        blurring: Floating point factor for spreading out the probabilities

    Returns:
        New belief added with uncertainties as list of lists
    """
    # Derive the height and width of the world / belief from the 
    # outer and inner lengths of the list of list object.
    height: int = len(beliefs)
    width : int= len(beliefs[0])
    # Initialize new belief with 0.0s and the same shape of the old 
    # belief.
    new_G: List[List[float]] = [[0.0 for _ in range(width)] for _ in range(height)]

    for i, row in enumerate(beliefs):
        for j, cell in enumerate(row):
            new_i: int = (i + dy ) % height
            new_j: int = (j + dx ) % width
            # pdb.set_trace()
            new_G[int(new_i)][int(new_j)] = cell
    return blur(new_G, blurring)
