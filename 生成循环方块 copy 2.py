import matplotlib.pyplot as plt
import numpy as np
import time
from joblib import Parallel, delayed

# 创建立方体的尺寸
axes = [1000, 1, 1000]

# 创建数据，表示每个体素是否被填充
data = np.ones(axes, dtype=bool)

# 创建3D图形对象
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# 创建颜色数组，用于控制体素的颜色
edgecolors = '#7D84A6'

# 设置pressure的范围和步长
pressure_values = np.arange(13,70, 0.05)

# 创建一个文本文件来保存输出
output_file = "output.txt"

# 写入表头
with open('output.txt', 'a') as f:
    f.write("压力\t绿块\t红块\n")

# 遍历不同的pressure值
for pressure in pressure_values:
    # 记录循环开始时间
    start_time = time.time()

    # 定义并行函数
    def process_arrow(i, j, k):
        # 生成随机方向向量
        direction = np.random.uniform(-1, 1, size=3)
        direction[2] = np.random.uniform(0, 1)

        # 归一化为单位向量
        unit_vector = direction / np.linalg.norm(direction)

        # 单位向量在每个轴上的分量
        x_component = np.abs(unit_vector[0])  # x 轴分量
        y_component = np.abs(unit_vector[1])  # y 轴分量
        z_component = np.abs(unit_vector[2])  # z 轴分量

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
        data1[i, j, k] = True  # 在指定位置创建方块

        # 当x轴分量超过30%箭头长度时所对应的方块变色
        if  pressure_x > px2 or pressure_y > py2:
            return 1, 0  # 1代表绿色方块，0代表红色方块
        else:
            return 0, 1

    # 并行计算箭头颜色
    results = Parallel(n_jobs=-1)(
        delayed(process_arrow)(i, j, k) for i in range(1000) for j in range(1) for k in range(1000)
    )

    # 统计绿色方块和红色方块的数量
    green_count = sum(result[0] for result in results)
    red_count = sum(result[1] for result in results)

    # 记录循环结束时间
    end_time = time.time()

    # 计算循环时间
    loop_time = end_time - start_time

    # 打开文件以追加模式写入
    with open('output.txt', 'a') as f:
        f.write(f"{pressure:.2f}\t{green_count}\t{red_count}\n")

    print(f"时间： {loop_time:.2f}")

ax.set_aspect('equal')
ax
