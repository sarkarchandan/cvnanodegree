from typing import Tuple, List
from typing_extensions import TypeAlias
from cv2 import transform
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


Constant_Velocity_State_t: TypeAlias = List[Tuple[int, int]]


class Car(object):
    """Defines a car's movement and keeps track of its state.
    The class includes init, move, and display functions.
    This class assumes a constant velocity motion model and the state
    of the car includes the car's position, and it's velocity.

    Attributes:
        state: A list of the car's current position [y, x] and velocity [vy, vx]
        world: The world that the car is moving within (a 2D list.
        _color: Default color of the car
        _path: Path that the car has taken in the world from its initialization
    """

    state: Constant_Velocity_State_t
    world: np.ndarray # world is a 2D array of values that range from 0-1
    _color: str
    _path: List[Tuple[int, int]] # Denotes 

    def __init__(self, position: Tuple[int, int], 
                velocity: Tuple[int, int], 
                world: np.ndarray, color: str = 'r') -> None:
        """Initializes the Car

        Args:
            position: Integer tuple (y, x) to denote the position of the car 
            in 2D world.
            velocity: Integer tuple (vy, vx) to denote the velocity of the car
            in a 2D world
            world: NumPy array of integers to represent a 2D world.
        """
        # Position is a list [y, x] and so is velocity [vy, vx]
        self.state = [position, velocity]
        self.world = world 
        self._color = color
        self._path = []
        # Append the initial position to the path
        self._path.append(position)
        

    # Move function
    def move(self, dt=1) -> None:
        """Moves the car in the direction of the velocity and 
        updates the state.
        
        It assumes a circular world and a default dt = 1 (though dt can be any 
        non-negative integer).

        Args:
            dt: Integer steps to move in a world. World is circular in 
            vertical and horizontal directions.
        """
        height: int = len(self.world)
        width: int = len(self.world[0])
        # Exract the position and velocity
        position: List[int] = self.state[0]
        velocity: List[int] = self.state[1]
        # Predict the new position [y, x] based on velocity [vx, vy] and time, dt
        predicted_position: Tuple[int, int] = (
            (position[0] + velocity[0]*dt) % height, # default dt = 1
            (position[1] + velocity[1]*dt) % width
        )
        # Update the state
        self.state = [predicted_position, velocity]
        # Every time the robot moves, add the new position to the path
        self._path.append(predicted_position)
        
    
    # Turn left function
    def turn_left(self) -> None:
        """Turn left using left rotation transformation.
        In the process we temporarily change the (vy, vx) form 
        to (vx, vy) for ease of intuitive understanding.
        """
        # Change the velocity
        velocity: Tuple[int, int] = self.state[1]  # (vy, vx)
        velocity_arr: np.ndarray = np.array([velocity[0], velocity[1]])
        # Left rotation tranformation for (vy, vx)
        left_rotate_transformer: np.ndarray = np.array([[0, -1], [1, 0]])
        left_rotated: np.ndarray = left_rotate_transformer  @ velocity_arr
        predicted_velocity: Tuple[int, int] = (left_rotated[0], left_rotated[1])
        # Update the state velocity
        self.state[1] = predicted_velocity

    
    # Turn right function
    def turn_right(self) -> None:
        """Turn right using right rotation transformation.
        In the process we temporarily change the (vy, vx) form 
        to (vx, vy) for ease of intuitive understanding.
        """
        # Change the velocity
        velocity: Tuple[int, int] = self.state[1]  # (vy, vx)
        velocity_arr: np.ndarray = np.array([velocity[0], velocity[1]])
        # Right rotation tranformation for (vy, vx)
        right_rotate_transformer: np.ndarray = np.array([[0, 1], [-1, 0]])
        right_rotated: np.ndarray = right_rotate_transformer  @ velocity_arr
        predicted_velocity: Tuple[int, int] = (right_rotated[0], right_rotated[1])
        # Update the state velocity
        self.state[1] = predicted_velocity
    
    
    # Helper function for displaying the world + robot position
    def display_world(self) -> None:
        """Displays the world along with position of the car in it"""
        
        position: Tuple[int, int] = self.state[0]
        # Plot grid of values + initial ticks
        plt.matshow(self.world, cmap='gray')
        # Set minor axes in between the labels
        # plt.gca returns the current Axes of the current figure, which 
        # was created earlier by the plt.imshow invocation
        ax: Axes = plt.gca() 
        rows: int = len(self.world)
        cols: int = len(self.world[0])

        ax.set_xticks([x-0.5 for x in range(1,cols)],minor=True )
        ax.set_yticks([y-0.5 for y in range(1,rows)],minor=True)

        # Plot grid on minor axes in gray (width = 2)
        plt.grid(which='minor',ls='-',lw=2, color='gray')

        # Create a 'x' character that represents the car
        # ha = horizontal alignment, va = verical
        ax.text(position[1], position[0], 'x', ha='center', va='center', color=self._color, fontsize=30)
            
        # Draw path if it exists
        if(len(self._path) > 1):
            # loop through all path indices and draw a dot (unless it's at the car's location)
            for pos in self._path:
                if(pos != position):
                    ax.text(pos[1], pos[0], '.', ha='center', va='baseline', color=self._color, fontsize=30)

        # Display final result
        plt.show()

