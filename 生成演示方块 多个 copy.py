import json
import os
import matplotlib.pyplot as plt
import numpy as np

# 创建立方体的尺寸
axes = [5, 5, 5]

# 创建数据，表示每个体素是否被填充
data = np.ones(axes, dtype=bool)

# 创建3D图形对象
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# 创建颜色数组，用于控制体素的颜色和透明度
facecolors = '#FFD65DC0'
facecolors1 = '#7A88CCC0'
edgecolors = '#7D84A6'

# 绘制体素图形
# ax.voxels(data, facecolors=facecolors, edgecolors=edgecolors, alpha=0.8, zorder= 1)
# 创建箭头方向
arrow_directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

red_count = 0
green_count = 0

red = '#FB6F6F'
green = '#009300'
blue = '#5E72FF'

# 存储箭头方向的文件名
arrow_directions_file = 'arrow_directions.json'

# 检查文件是否存在
if os.path.exists(arrow_directions_file):
    # 从文件中读取箭头方向
    with open(arrow_directions_file, 'r') as file:
        arrow_directions = json.load(file)
else:
    # 生成新的箭头方向并保存到文件中
    arrow_directions = []
    for i in range(5):
        for j in range(1):
            for k in range(5):
                if data[i, j, k]:
                    direction = np.random.uniform(-1, 1, size=3)
                    direction[2] = np.random.uniform(0, 1)
                    direction /= np.linalg.norm(direction)  # 归一化为单位向量
                    arrow_directions.append((i, j, k, direction.tolist()))
    with open(arrow_directions_file, 'w') as file:
        json.dump(arrow_directions, file)
# 记录需要删除箭头的位置
arrows_to_remove = [] 

# 在每个方块中心生成随机取向的箭头
for (i, j, k, direction) in arrow_directions:
        if data[i, j, k]:
            x = i + 0.5
            y = j + 0.5
            z = k + 0.5

            # 取绝对值
            direction_abs = np.abs(direction)

            # 归一化为单位向量
            unit_vector = direction / np.linalg.norm(direction)

            # 单位向量在每个轴上的分量
            x_component = np.abs(unit_vector[0])
            y_component = np.abs(unit_vector[1])
            z_component = np.abs(unit_vector[2])

            u, v, w = direction
            arrow_length = 1

            arrow_length_x = x_component * arrow_length
            arrow_length_y = y_component * arrow_length
            arrow_length_z = z_component * arrow_length
           
            pressure = 80
           
            px1 = arrow_length * 3.3
            py1 = arrow_length * 3.5
            pz1 = arrow_length * 10.2

            px2 = arrow_length * 14.5
            py2 = arrow_length * 14.5

            pressure_x = float(arrow_length_x) * pressure
            pressure_y = float(arrow_length_y) * pressure
            pressure_z = float(arrow_length_z) * pressure
            
            if pressure_x > px2 or pressure_y > py2:

                arrow_color = 'none'
                arrows_to_remove.append((x, y, z))
            else:
                arrow_color = 'red'

            # 绘制箭头
            ax.quiver(x - u * arrow_length / 2, y - v * arrow_length / 2, z - w * arrow_length / 2,
                      u, v, w, length=arrow_length, linewidth=2, color=arrow_color, alpha=1)

            axes1 = [i + 1, j + 1, k + 1]
            data1 = np.zeros(axes, dtype=bool)
            data1[i, j, k] = True  # 在指定位置创建方块
                # 当x轴分量超过30%箭头长度时所对应的方块变色
            """
            if pressure_x > px1 or pressure_y > py1 or pressure_z > pz1:

                ax.voxels(data1, facecolors=green, edgecolors=edgecolors, alpha=0.4, zorder=1)
                green_count += 1
            else:
                ax.voxels(data1, facecolors= red, edgecolors=edgecolors, alpha=0.4, zorder=1)
                red_count += 1
            """    
            if pressure_x > px2 or pressure_y > py2:
                ax.voxels(data1, facecolors=blue, edgecolors=edgecolors, alpha=0.4, zorder=1)
                green_count += 1
                arrows_to_remove.append((x, y, z))
            else:
                ax.voxels(data1, facecolors= green, edgecolors=edgecolors, alpha=0.4, zorder=1)
                red_count += 1
                  
                



# 保存当前压力值的图像
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# 设置坐标轴标签
ax.set_xlabel('x', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})
ax.set_ylabel('y', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})
ax.set_zlabel('z', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})

ax.xaxis.labelpad = -15  # 根据需要调整数值
ax.yaxis.labelpad = -15  # 根据需要调整数值
ax.zaxis.labelpad = -15 # 根据需要调整数值



print(f"绿色方块数量：{green_count}")
print(f"红色方块数量：{red_count}")


#隐藏坐标轴刻度和刻度标签
ax.set_aspect('equal')
ax.axis('off')

 # 调整 elevation 和 azimuth
ax.view_init(elev=15, azim=90) 
# 显示图形
plt.show()
 
#保存图像
fig.savefig(f'{pressure:.2f}.png', dpi=300)
plt.cla()  # 清除轴内容以便绘制下一个压力值的结果