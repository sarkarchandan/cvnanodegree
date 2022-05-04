from typing import List, Tuple


def normalize(grid: List[List[float]]) -> List[List[float]]:
    """Given a grid of nonnormalized probabilities, computes the
    correspond normalized version of that grid. 
    
    Args:
        grid: 2D grid of nonnormalized probability distribution
    
    Returns:
        2D grid of normalized probability distribution
    """
    #TODO: Refactor to use NumPy
    # Get the sum total of all probabilities in the 
    # grid.
    total: float = 0.0
    for row in grid:
        for cell in row:
            total += cell
    # Enumerate over each single element of the grid 
    # using nested loops and normalize the value by 
    # dividing the same with the sum.
    for i,row in enumerate(grid):
        for j,cell in enumerate(row):
            grid[i][j] = float(cell) / total
    return grid


def blur(grid: List[List[float]], blurring: float) -> List[List[float]]:
    """Spreads probability out on a grid using a 3x3 blurring window.
    The blurring parameter controls how much of a belief spills out
    into adjacent cells. If blurring is 0 this function will have 
    no effect. In essence, it defines a smoothening kernel with 
    the help of blurring factor and makes a convolution with 
    the input grid.

    Args:
        grid: 2D grid of probabilities
        blurring: Float value as a factor of spreading out the 
        probabilities
    
    Returns:
        2D grid of spread out probabilities
    """
    #TODO: Refactor to use NumPy
    # Since the grid is a list of lists number of inner lists 
    # is the height and number of elements in any of the inner 
    # lists is width.
    height: int = len(grid)
    width: int  = len(grid[0])
    # Assuming that the center has the maximum probability 
    # before spreading out, subtract the blurring from 1.0 
    # to get the new center probability after blurring.
    center_prob: float = 1.0-blurring
    # After spread out corner cells are supposed to have the 
    # minimum probability.
    corner_prob: float = blurring / 12.0
    # After spread out adjacent cells are supposed to have the 
    # probabilities somewhere in between the center and corner 
    # ones.
    adjacent_prob: float = blurring / 6.0
    # This is very similar to defining a normalization kernel 
    # or in other words a smoothening filter.
    window: List[List[float]] = [
        [corner_prob,  adjacent_prob,  corner_prob],
        [adjacent_prob, center_prob,  adjacent_prob],
        [corner_prob,  adjacent_prob,  corner_prob]
    ]
    # Initialize a new 2D grid of 0.0 values with the predetermined 
    # height and width of the input grid.
    new: List[List[float]] = [[0.0 for i in range(width)] for j in range(height)]
    # Following nested loop constrcut in essence implements a 2D 
    # convolution of the input grid with the window defined above.
    # Iterate over the input grid
    for i in range(height):
        for j in range(width):
            # Get each single grid value
            grid_val: float = grid[i][j]
            # Iterate in range [-1, 0, 1] for outer index
            for dx in range(-1,2):
                # Iterate in range [-1, 0, 1] for inner index
                for dy in range(-1,2):
                    # Get a value from the defined window. 
                    # The [dx+1][dy+1] indexing results in 
                    # (0,0),(0,1),(0,2)
                    # (1,0),(1,1),(1,2)
                    # (2,0),(2,1),(2,2) indexing
                    mult: float = window[dx+1][dy+1]
                    new_i: int = (i + dy) % height
                    new_j: int = (j + dx) % width
                    new[new_i][new_j] += mult * grid_val
    return normalize(new)

def is_robot_localized(beliefs: List[List[float]], true_pos: Tuple[int, int]) -> Tuple[bool, Tuple[int, int]]:
    """Returns None if the robot has no "strong opinion" about
    its belief. The robot has a strong opinion when the 
    size of it's best belief is greater than twice the size of 
    its second best belief.

    If it DOES have a strong opinion then this function returns 
    True if that opinion is correct and False if it is not.

    Args:
        beliefs: Current belief of the robot about its location
        true_pos: True position of the robot in its world as tuple 
        of indices
    
    Returns:
        A tuple indication, whether the robot is localized and its 
        best known location
    """
    best_belief: float = 0.0
    best_pos: Tuple[int, int] = None
    second_best: float = 0.0
    for y, row in enumerate(beliefs):
        for x, belief in enumerate(row):
            # If belief probability is higher than the best_belief
            # then best_belief goes to second best and belief 
            # probability takes the mantle of best belief. As a 
            # result corresponding indices becomes the best 
            # position for the robot.
            if belief > best_belief:
                second_best = best_belief
                best_belief = belief
                best_pos = (y,x)
            # If belief probability is greater than second_best
            # instead then it becomes the second_best.
            elif belief > second_best:
                second_best = belief
    # If the best belief is significantly greater than second best 
    # belief like a factor of 2.0 then we conclude, that the robot 
    # has high degree of certainty about its location.
    if second_best <= 0.00001 or best_belief / second_best > 2.0:
        # robot thinks it knows where it is
        localized =  best_pos == true_pos
        return localized, best_pos
    else:
        # No strong single best belief
        return None, best_pos

def close_enough(g1: List[List[float]], g2: List[List[float]]) -> bool:
    """Evaluates if two passed in grids of values are close enough
    Args:
        g1: First grid of float values
        g2: Second grid of float values
    
    Returns:
        Boolean indicator, if the values are close enough
    """
    if len(g1) != len(g2):
        return False
    if len(g1) == 0 or len(g1[0]) != len(g2[0]):
        return False
    for r1, r2 in zip(g1,g2):
        for v1, v2 in zip(r1, r2):
            if abs(v1 - v2) > 0.001:
                print(v1, v2)
                return False
    return True
