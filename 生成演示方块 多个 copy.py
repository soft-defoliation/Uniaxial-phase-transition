import json
import os
import matplotlib.pyplot as plt
import numpy as np

# Create the size of the cube
axes = [5, 5, 5]

# Create data indicating whether each voxel is filled
data = np.ones(axes, dtype=bool)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Define color arrays to control the color and transparency of the voxels
facecolors = '#FFD65DC0'
facecolors1 = '#7A88CCC0'
edgecolors = '#7D84A6'

# Define arrow directions
arrow_directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

red_count = 0
green_count = 0

red = '#FB6F6F'
green = '#009300'
blue = '#5E72FF'

# File name to store arrow directions
arrow_directions_file = 'arrow_directions_duo.json'

# Check if the file exists
if os.path.exists(arrow_directions_file):
    # Read arrow directions from the file
    with open(arrow_directions_file, 'r') as file:
        arrow_directions = json.load(file)
else:
    # Generate new arrow directions and save them to the file
    arrow_directions = []
    for i in range(5):
        for j in range(1):
            for k in range(5):
                if data[i, j, k]:
                    direction = np.random.uniform(-1, 1, size=3)
                    direction[2] = np.random.uniform(0, 1)
                    direction /= np.linalg.norm(direction)  # Normalize to unit vector
                    arrow_directions.append((i, j, k, direction.tolist()))
    with open(arrow_directions_file, 'w') as file:
        json.dump(arrow_directions, file)

# Record positions of arrows to be removed
arrows_to_remove = []

# Generate randomly oriented arrows at the center of each voxel
for (i, j, k, direction) in arrow_directions:
    if data[i, j, k]:
        x = i + 0.5
        y = j + 0.5
        z = k + 0.5

        # Take the absolute value
        direction_abs = np.abs(direction)

        # Normalize to unit vector
        unit_vector = direction / np.linalg.norm(direction)

        # Components of the unit vector along each axis
        x_component = np.abs(unit_vector[0])
        y_component = np.abs(unit_vector[1])
        z_component = np.abs(unit_vector[2])

        u, v, w = direction
        arrow_length = 1

        pressure_x = np.abs(direction[0])
        pressure_y = np.abs(direction[1])
        pressure_z = np.abs(direction[2])

        px1 = 0.3
        py1 = 0.3
        pz1 = 0.3

        # Determine arrow color
        if pressure_x > px1 or pressure_y > py1 or pressure_z > pz1:
            arrow_color = blue
            arrows_to_remove.append((x, y, z, u, v, w))
        else:
            arrow_color = red

        # Draw the arrow
        ax.quiver(x - u * arrow_length / 2, y - v * arrow_length / 2, z - w * arrow_length / 2,
                  u, v, w, length=arrow_length, linewidth=2, color=arrow_color, alpha=1)

        axes1 = [i + 1, j + 1, k + 1]
        data1 = np.zeros(axes, dtype=bool)
        data1[i, j, k] = True  # Create a voxel at the specified position

        # Color the voxel if the component along the x-axis exceeds 30% of the arrow length
        if pressure_x > px1 or pressure_y > py1 or pressure_z > pz1:
            ax.voxels(data1, facecolors=green, edgecolors=edgecolors, alpha=0.4, zorder=1)
            green_count += 1
        else:
            ax.voxels(data1, facecolors=red, edgecolors=edgecolors, alpha=0.4, zorder=1)
            red_count += 1

# Remove arrows corresponding to blue voxels
for (x, y, z, u, v, w) in arrows_to_remove:
    ax.quiver(x - u * arrow_length / 2, y - v * arrow_length / 2, z - w * arrow_length / 2,
              u, v, w, length=arrow_length, linewidth=2, color='none')

# Set axis labels
ax.set_xlabel('x', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})
ax.set_ylabel('y', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})
ax.set_zlabel('z', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})

ax.xaxis.labelpad = -15  # Adjust values as needed
ax.yaxis.labelpad = -15  # Adjust values as needed
ax.zaxis.labelpad = -15  # Adjust values as needed

print(f"Number of green voxels: {green_count}")
print(f"Number of red voxels: {red_count}")

# Display the plot
plt.show()

# Save the image
fig.savefig('pressure.png', dpi=300)
plt.cla()  # Clear the axes to draw the result for the next pressure value
