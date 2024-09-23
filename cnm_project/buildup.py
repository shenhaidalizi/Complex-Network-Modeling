import random
import matplotlib.pyplot as plt
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def create_scale_free_network(n, m):
    edges = []  # 网络中的边列表
    nodes = list(range(m))  # 初始节点集

    # 初始完全图
    for i in range(m):
        for j in range(i + 1, m):
            edges.append((i, j))

    # 逐步添加节点
    for new_node in range(m, n):
        target_nodes = set()
        while len(target_nodes) < m:
            # 根据度数优先选择已有节点
            potential_target = random.choices(nodes, weights=[degree_count(n, edges, node) for node in nodes])[0]
            target_nodes.add(potential_target)

        # 将新节点连接到目标节点
        for target in target_nodes:
            edges.append((new_node, target))
        nodes.append(new_node)

    return edges


def degree_count(n, edges, node):
    count = 0
    for edge in edges:
        if node in edge:
            count += 1
    return count


# 创建一个100个节点的无标度网络
n = 100
m = 3
edges = create_scale_free_network(n, m)


def evolve_network(original_edges, new_nodes, m, rewire_probability=0.1):
    """演化网络，保留原网络并添加新节点."""
    edges = original_edges.copy()  # 保留原网络
    current_nodes = list(set([node for edge in edges for node in edge]))

    # 添加新节点
    for new_node in range(max(current_nodes) + 1, max(current_nodes) + new_nodes + 1):
        target_nodes = set()
        while len(target_nodes) < m:
            potential_target = random.choices(current_nodes, weights=[degree_count(len(edges), edges, node) for node in current_nodes])[0]
            target_nodes.add(potential_target)
        for target in target_nodes:
            edges.append((new_node, target))
        current_nodes.append(new_node)

    # 边重连
    for i, (u, v) in enumerate(edges):
        if random.random() < rewire_probability:
            new_target = random.choice(current_nodes)
            edges[i] = (u, new_target)

    return edges

# 演化网络
new_edges = evolve_network(edges, new_nodes=10, m=m, rewire_probability=0.1)



def degree_distribution(n, edges):
    degree_dict = {i: 0 for i in range(n)}
    for edge in edges:
        degree_dict[edge[0]] += 1
        degree_dict[edge[1]] += 1

    degree_freq = {}
    for degree in degree_dict.values():
        if degree not in degree_freq:
            degree_freq[degree] = 0
        degree_freq[degree] += 1

    return degree_freq


# 计算度分布
degree_dist = degree_distribution(n, edges)
degree_dist1 = degree_distribution(n + 10, new_edges)
print("Degree Distribution:", degree_dist)
print("New Degree Distribution:", degree_dist1)


def plot_degree_distribution(degree_dist):
    degrees = list(degree_dist.keys())
    frequencies = list(degree_dist.values())

    plt.figure(figsize=(8, 6))
    plt.bar(degrees, frequencies, color='skyblue', edgecolor='black')
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# 绘制度分布图
plot_degree_distribution(degree_dist)
plot_degree_distribution(degree_dist1)




def bfs_shortest_path(n, edges, start):
    distances = {i: float('inf') for i in range(n)}
    distances[start] = 0
    queue = deque([start])

    while queue:
        node = queue.popleft()
        for edge in edges:
            if node in edge:
                neighbor = edge[0] if edge[1] == node else edge[1]
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
    return distances


def average_shortest_path_length(n, edges):
    total_path_length = 0
    num_pairs = 0

    for node in range(n):
        distances = bfs_shortest_path(n, edges, node)
        for target, distance in distances.items():
            if distance != float('inf') and target != node:
                total_path_length += distance
                """print("Points pair with ", node, target, distance)"""
                num_pairs += 1
    print("Total distance", total_path_length)
    return total_path_length / num_pairs if num_pairs > 0 else float('inf')


# 计算平均最短路径长度
avg_shortest_path_length = average_shortest_path_length(n, edges)
print("Average Shortest Path Length:", avg_shortest_path_length)
new_avg_shortest_path_length = average_shortest_path_length(n + 10, new_edges)
print("New Average Shortest Path Length:", new_avg_shortest_path_length)

def clustering_coefficient(n, edges):
    """计算网络的平均聚类系数."""
    clustering_coeffs = []

    for node in range(n):
        # 找出当前节点的邻居
        neighbors = set()
        for edge in edges:
            if edge[0] == node:
                neighbors.add(edge[1])
            elif edge[1] == node:
                neighbors.add(edge[0])

        # 计算邻居之间的边数
        if len(neighbors) < 2:
            clustering_coeffs.append(0)
            continue

        links_between_neighbors = 0
        for neighbor1 in neighbors:
            for neighbor2 in neighbors:
                if neighbor1 != neighbor2 and (neighbor1, neighbor2) in edges or (neighbor2, neighbor1) in edges:
                    links_between_neighbors += 1

        # 计算聚类系数
        clustering_coeffs.append(links_between_neighbors / (len(neighbors) * (len(neighbors) - 1)))

    return sum(clustering_coeffs) / n


# 计算平均聚类系数
avg_clustering_coefficient = clustering_coefficient(n, edges)
print("Average Clustering Coefficient:", avg_clustering_coefficient)
new_avg_clustering_coefficient = clustering_coefficient(n + 10, new_edges)
print("Average Clustering Coefficient:", new_avg_clustering_coefficient)
def calculate_local_clustering_coefficients(n, edges):
    """计算每个节点的局部聚类系数。"""
    local_clustering_coeffs = []

    for node in range(n):
        # 找出当前节点的邻居
        neighbors = set()
        for edge in edges:
            if edge[0] == node:
                neighbors.add(edge[1])
            elif edge[1] == node:
                neighbors.add(edge[0])

        # 计算邻居之间的边数
        if len(neighbors) < 2:
            local_clustering_coeffs.append(0)
            continue

        links_between_neighbors = 0
        neighbors_list = list(neighbors)
        for i in range(len(neighbors_list)):
            for j in range(i + 1, len(neighbors_list)):
                if (neighbors_list[i], neighbors_list[j]) in edges or (neighbors_list[j], neighbors_list[i]) in edges:
                    links_between_neighbors += 1

        # 计算局部聚类系数
        local_clustering_coeffs.append(links_between_neighbors / (len(neighbors) * (len(neighbors) - 1) / 2))

    return local_clustering_coeffs

def plot_local_clustering_coefficients(local_clustering_coefficients):
    """绘制节点的局部聚类系数的散点图。"""
    nodes = list(range(len(local_clustering_coefficients)))
    clustering_values = local_clustering_coefficients

    plt.figure(figsize=(8, 6))
    plt.scatter(nodes, clustering_values, color='purple', alpha=0.7)
    plt.title("Local Clustering Coefficients of Nodes")
    plt.xlabel("Node")
    plt.ylabel("Local Clustering Coefficient")
    plt.ylim(0, 1)  # 聚类系数范围通常在0到1之间
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def plot_average_clustering_coefficient(avg_clustering_coefficient):
    """绘制平均聚类系数的条形图。"""
    plt.figure(figsize=(6, 4))
    plt.bar(['Network'], [avg_clustering_coefficient], color='skyblue', edgecolor='black')
    plt.title("Average Clustering Coefficient of the Network")
    plt.ylabel("Clustering Coefficient")
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# 计算局部聚类系数
local_clustering_coefficients = calculate_local_clustering_coefficients(n, edges)
new_local_clustering_coefficients = calculate_local_clustering_coefficients(n + 10, new_edges)

# 计算平均聚类系数
average_clustering_coefficient = sum(local_clustering_coefficients) / n
new_average_clustering_coefficient = sum(new_local_clustering_coefficients) / n

# 可视化局部聚类系数
plot_local_clustering_coefficients(local_clustering_coefficients)
plot_local_clustering_coefficients(new_local_clustering_coefficients)

# 可视化平均聚类系数
plot_average_clustering_coefficient(average_clustering_coefficient)
plot_average_clustering_coefficient(new_average_clustering_coefficient)


def plot_network(n, edges):
    """绘制网络的结构图."""
    plt.figure(figsize=(8, 6))

    # 生成节点的随机布局
    pos = {i: (random.random(), random.random()) for i in range(n)}

    # 绘制边
    for edge in edges:
        x_values = [pos[edge[0]][0], pos[edge[1]][0]]
        y_values = [pos[edge[0]][1], pos[edge[1]][1]]
        plt.plot(x_values, y_values, 'gray', alpha=0.5)

    # 绘制节点
    for node, (x, y) in pos.items():
        plt.plot(x, y, 'o', markersize=8, color='skyblue')

    plt.title("Network Structure Visualization")
    plt.axis('off')
    plt.show()

# 绘制网络结构图
plot_network(n, edges)
plot_network(n + 10, new_edges)

def calculate_core_number(n, edges):
    """计算每个节点的核心度（k-core number）."""
    # 初始化每个节点的度数
    degree = {i: 0 for i in range(n)}
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1

    # 初始化核心度
    core_number = {i: 0 for i in range(n)}

    # 使用队列进行核心度计算
    nodes = sorted(degree.keys(), key=lambda x: degree[x])  # 按度数排序的节点列表

    while nodes:
        node = nodes.pop(0)  # 移除度数最小的节点
        current_degree = degree[node]

        # 更新核心度
        core_number[node] = current_degree

        # 移除当前节点并更新其邻居的度数
        for u, v in edges:
            if u == node or v == node:
                neighbor = v if u == node else u
                if degree[neighbor] > current_degree:  # 仅减少度数大于当前节点的邻居
                    degree[neighbor] -= 1

        # 重新排序节点列表
        nodes = sorted(nodes, key=lambda x: degree[x])

    return core_number

# 计算核心度
core_number = calculate_core_number(n, edges)
print("Core Number of each node:", core_number)
new_core_number = calculate_core_number(n + 10, new_edges)
print("Core Number of each node:", new_core_number)

def plot_core_number(core_number):
    """绘制节点核心度的柱状图."""
    nodes = list(core_number.keys())
    cores = list(core_number.values())

    plt.figure(figsize=(8, 6))
    plt.bar(nodes, cores, color='lightcoral', edgecolor='black')
    plt.title("Core Number of Nodes")
    plt.xlabel("Node")
    plt.ylabel("Core Number")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# 绘制节点核心度图
plot_core_number(core_number)
plot_core_number(new_core_number)


def simulate_random_attack(n, edges):
    """模拟网络的随机攻击."""
    nodes = list(range(n))
    random.shuffle(nodes)  # 随机打乱节点顺序
    sizes = []

    for node in nodes:
        edges = [(u, v) for u, v in edges if u != node and v != node]  # 移除节点和相关的边
        if not edges:
            break
        largest_cc_size = get_largest_connected_component_size(n, edges)
        sizes.append(largest_cc_size)

    return sizes


def get_largest_connected_component_size(n, edges):
    """计算最大连通子图的大小."""
    visited = [False] * n

    def dfs(node):
        stack = [node]
        size = 0
        while stack:
            current = stack.pop()
            if not visited[current]:
                visited[current] = True
                size += 1
                for edge in edges:
                    if edge[0] == current and not visited[edge[1]]:
                        stack.append(edge[1])
                    elif edge[1] == current and not visited[edge[0]]:
                        stack.append(edge[0])
        return size

    largest_size = 0
    for node in range(n):
        if not visited[node]:
            component_size = dfs(node)
            if component_size > largest_size:
                largest_size = component_size
    return largest_size


# 执行随机攻击模拟
random_attack_sizes = simulate_random_attack(n, edges)
print("Random Attack Sizes:", random_attack_sizes)
new_random_attack_sizes = simulate_random_attack(n + 10, new_edges)
print("New Random Attack Sizes:", new_random_attack_sizes)


def simulate_targeted_attack(n, edges):
    """模拟网络的故意攻击."""
    nodes = list(range(n))
    degrees = {node: degree_count(n, edges, node) for node in nodes}
    nodes_sorted_by_degree = sorted(nodes, key=lambda x: degrees[x], reverse=True)  # 按度数从大到小排序
    sizes = []

    for node in nodes_sorted_by_degree:
        edges = [(u, v) for u, v in edges if u != node and v != node]  # 移除节点和相关的边
        if not edges:
            break
        largest_cc_size = get_largest_connected_component_size(n, edges)
        sizes.append(largest_cc_size)

    return sizes


# 执行故意攻击模拟
targeted_attack_sizes = simulate_targeted_attack(n, edges)
print("Targeted Attack Sizes:", targeted_attack_sizes)
new_targeted_attack_sizes = simulate_targeted_attack(n + 10, new_edges)
print("Targeted Attack Sizes:", new_targeted_attack_sizes)

def plot_attack_simulation(random_attack_sizes, targeted_attack_sizes):
    """绘制攻击模拟的结果图."""
    plt.figure(figsize=(8, 6))

    # 绘制随机攻击结果
    plt.plot(range(len(random_attack_sizes)), random_attack_sizes, label='Random Attack', color='blue', linestyle='-', marker='o')

    # 绘制故意攻击结果
    plt.plot(range(len(targeted_attack_sizes)), targeted_attack_sizes, label='Targeted Attack', color='red', linestyle='-', marker='x')

    plt.title("Network Robustness under Attacks")
    plt.xlabel("Number of Removed Nodes")
    plt.ylabel("Size of Largest Connected Component")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# 绘制攻击鲁棒性分析图
plot_attack_simulation(random_attack_sizes, targeted_attack_sizes)
plot_attack_simulation(new_random_attack_sizes, new_targeted_attack_sizes)




def small_world_test(edges, num_randomizations=100):
    """判断网络是否是小世界网络."""
    G = nx.Graph()
    G.add_edges_from(edges)

    # 检查网络是否连通
    if not nx.is_connected(G):
        return False, None, None, None, None  # 返回 False 表示不是小世界

    # 计算目标网络的聚类系数和平均路径长度
    target_clustering = nx.average_clustering(G)
    target_avg_path_length = nx.average_shortest_path_length(G)

    # 创建随机网络并进行对比
    random_clustering = []
    random_avg_path_length = []

    for _ in range(num_randomizations):
        random_graph = nx.gnm_random_graph(len(G.nodes()), len(G.edges()))

        # 检查随机网络是否连通
        if nx.is_connected(random_graph):
            random_clustering.append(nx.average_clustering(random_graph))
            random_avg_path_length.append(nx.average_shortest_path_length(random_graph))

    # 计算随机网络的平均聚类系数和平均路径长度
    if random_clustering and random_avg_path_length:
        avg_random_clustering = np.mean(random_clustering)
        avg_random_path_length = np.mean(random_avg_path_length)

        # 判断小世界特性
        is_small_world = (target_clustering > avg_random_clustering) and (
                    target_avg_path_length < avg_random_path_length)
        return is_small_world, target_clustering, target_avg_path_length, avg_random_clustering, avg_random_path_length
    else:
        return False, None, None, None, None  # 如果没有有效的随机网络返回 False


# 测试小世界特性
is_small_world, target_clustering, target_avg_path_length, avg_random_clustering, avg_random_path_length = small_world_test(
    new_edges)

if is_small_world is not None:
    print(f"Is Small World: {is_small_world}")
    print(f"Target Clustering: {target_clustering}, Random Clustering: {avg_random_clustering}")
    print(f"Target Average Path Length: {target_avg_path_length}, Random Average Path Length: {avg_random_path_length}")
else:
    print("网络不连通，无法判断小世界特性。")

n = 100  # 节点数
m = 150  # 随机选择边数（50到300之间）

# 生成随机图
random_graph = nx.gnm_random_graph(n, m)

# 提取边并转换为边数组
edges = list(random_graph.edges)

random_attack_sizes = simulate_random_attack(n, edges)
print("Random Attack Sizes:", random_attack_sizes)
targeted_attack_sizes = simulate_targeted_attack(n, edges)
print("Targeted Attack Sizes:", targeted_attack_sizes)
plot_attack_simulation(random_attack_sizes, targeted_attack_sizes)


