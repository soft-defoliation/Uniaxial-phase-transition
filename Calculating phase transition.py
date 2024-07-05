import matplotlib.pyplot as plt
import numpy as np
import time
from joblib import Parallel, delayed

# Create the dimensions of the cube
axes = [1000, 1, 1000]

# Create data indicating whether each voxel is filled
data = np.ones(axes, dtype=bool)

# Create 3D graphics objects
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Creates a color array to control the color of the voxel
edgecolors = '#7D84A6'

# Set the pressure range and step size
pressure_values = np.arange(13,70, 0.05)

# Create a text file to save the output
output_file = "output.txt"

# Write list head
with open('output.txt', 'a') as f:
    f.write("Pressure;\tgreen\tred\n")

# Traverse different pressure values
for pressure in pressure_values:
    # Records the start time of the loop
    start_time = time.time()

    # Define parallel functions
    def process_arrow(i, j, k):
        # Generate random direction vectors
        direction = np.random.uniform(-1, 1, size=3)
        direction[2] = np.random.uniform(0, 1)

        # Normalized to a unit vector
        unit_vector = direction / np.linalg.norm(direction)

        # The component of the unit vector on each axis
        x_component = np.abs(unit_vector[0])  # X-axis component
        y_component = np.abs(unit_vector[1])  # Y-axis component
        z_component = np.abs(unit_vector[2])  # Z-axis component

        u, v, w = direction
        arrow_length = 1

        arrow_color = 'red'

        arrow_length_x = x_component * arrow_length
        arrow_length_y = y_component * arrow_length
        arrow_length_z = z_component * arrow_length

        px1 = arrow_length * 3.3
        py1 = arrow_length * 3.5
        pz1 = arrow_length * 10.5

        px2 = arrow_length * 14.6
        py2 = arrow_length * 14.6

        pressure_x = float(arrow_length_x) * pressure
        pressure_y = float(arrow_length_y) * pressure
        pressure_z = float(arrow_length_z) * pressure

        axes1 = [i + 1, j + 1, k + 1]
        data1 = np.zeros(axes, dtype=bool)
        data1[i, j, k] = True  # Creates a box at the specified location

        # When the X-axis component exceeds 30% of the arrow length, the corresponding square changes color
        if  pressure_x > px2 or pressure_y > py2:
            return 1, 0  # 1代表绿色方块，0代表红色方块
        else:
            return 0, 1

    # Calculate arrow colors in parallel
    results = Parallel(n_jobs=-1)(
        delayed(process_arrow)(i, j, k) for i in range(1000) for j in range(1) for k in range(1000)
    )

    # Count the number of green squares and red squares
    green_count = sum(result[0] for result in results)
    red_count = sum(result[1] for result in results)

    # Records the end time of the loop
    end_time = time.time()

    # Calculating cycle time
    loop_time = end_time - start_time

    # Open file to write in append mode
    with open('output.txt', 'a') as f:
        f.write(f"{pressure:.2f}\t{green_count}\t{red_count}\n")

    print(f"time： {loop_time:.2f}")

ax.set_aspect('equal')
ax
