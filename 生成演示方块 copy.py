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

arrow_lengths = []

red_count = 0
green_count = 0

red = '#FB6F6F'
green = '#009300'
blue = '#5E72FF'
# 在每个方块中心生成随机取向的箭头 
for i in range(5):
    for j in range(1):
        for k in range(5):
          if data[i, j, k]:
                x = i + 0.5
                y = j + 0.5
                z = k + 0.5
                #print("i,j,k：", i,j,k)
                # 生成随机方向向量
                direction_x = np.random.uniform(-1, 1)
                direction_y = np.random.uniform(-1, 1)
                direction_z = np.random.uniform(-1, 1)

                # 归一化为单位向量
                x_unit_vector = direction_x / np.linalg.norm(direction_x)
                y_unit_vector = direction_y / np.linalg.norm(direction_y)
                z_unit_vector = direction_z / np.linalg.norm(direction_z)

                # 单位向量在每个轴上的分量
                x_component =  np.abs(x_unit_vector)  # x 轴分量
                y_component =  np.abs(y_unit_vector)  # y 轴分量
                z_component =  np.abs(z_unit_vector)  # z 轴分量

                u, v, w = direction_x,direction_y, direction_z

                arrow_length = 1

                arrow_color = 'red'

                arrow_length_x = x_component * arrow_length
                arrow_length_y = y_component * arrow_length
                arrow_length_z = z_component * arrow_length

                px1 = arrow_length * 2.0
                py1 = arrow_length * 4.0
                pz1 = arrow_length * 7.0

                px2 = arrow_length * 20.0
                py2 = arrow_length * 23.0

                pressure = 4
                pressure_x = float(arrow_length_x) * pressure
                pressure_y = float(arrow_length_y) * pressure
                pressure_z = float(arrow_length_z) * pressure

                #print("箭头在 x 轴上的分量：", pressure_x)
                #print("箭头在 y 轴上的分量：", pressure_y)
                #print("箭头在 z 轴上的分量：", pressure_z)
                #arrow_lengths.append((arrow_length_x, arrow_length_y, arrow_length_z))  # 记录箭头长度
 
                # 计算箭头在 x、y 和 z 轴上的分量长度
                ax.quiver(x- u * arrow_length / 2, y - v * arrow_length / 2, z - w * arrow_length / 2,
                        u, v, w, length=arrow_length, linewidth=2, color=arrow_color, alpha=1, zorder=2)
                
                """
                # 获取箭头长度
                start = np.array([x - u * arrow_length / 2, y - v * arrow_length / 2, z - w * arrow_length / 2])
                end = np.array([x + u * arrow_length / 2, y + v * arrow_length / 2, z + w * arrow_length / 2])
                length = np.linalg.norm(end - start)
                arrow_lengths.append(length)
                """
               
                axes1 = [i+1, j+1, k+1]
                data1 = np.zeros(axes, dtype=bool)
                data1[i, j, k] = True  # 在指定位置创建方块
                # 当x轴分量超过30%箭头长度时所对应的方块变色
                if pressure_x > px1 or pressure_y > py1 or pressure_z > pz1:

                    ax.voxels(data1, facecolors=green, edgecolors=edgecolors, alpha=0.4, zorder=1)
                    green_count += 1
                else:
                    ax.voxels(data1, facecolors=red,  edgecolors=edgecolors, alpha=0.4, zorder=1)
                    red_count += 1
                """
                if pressure_x > px2 or pressure_y > py2:
                    axes1 = [i+1, j+1, k+1]
                    data1 = np.zeros(axes, dtype=bool)
                    data1[i, j, k] = True  # 在指定位置创建方块
                    ax.voxels(data1, facecolors='blue', edgecolors=edgecolors, alpha=0.3, zorder=2,)
                """




print(f"绿色方块数量：{green_count}")
print(f"红色方块数量：{red_count}")

ax.set_aspect('equal')
ax.axis('off')

print("箭头在 x 轴上的压力：", px1)


# 统计箭头长度
#print("每个箭头长度：", arrow_lengths)


# 显示图形
plt.show()

fig.savefig(f'{pressure}.png', dpi=300)
 