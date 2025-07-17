from collections import deque, defaultdict

# Node structure
class Node:
    def __init__(self, value):
        self.data = value
        self.left = None
        self.right = None

# Build the binary tree
def build_tree(edges):
    nodes = {}
    children = set()
    
    for u, v, c in edges:
        if u not in nodes:
            nodes[u] = Node(u)
        if v not in nodes:
            nodes[v] = Node(v)
        
        if c == 'L':
            nodes[u].left = nodes[v]
        else:
            nodes[u].right = nodes[v]
        children.add(v)
    
    # Root is the node that's never a child
    for node_val in nodes:
        if node_val not in children:
            return nodes[node_val]
    return None

# Zigzag traversal
def zigzag_traversal(root):
    if not root:
        return
    
    result = []
    queue = deque()
    queue.append(root)
    left_to_right = True

    while queue:
        level_size = len(queue)
        level_nodes = []

        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.data)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if not left_to_right:
            level_nodes.reverse()
        result.extend(level_nodes)

        left_to_right = not left_to_right

    print(" ".join(map(str, result)))

# Main
n = int(input())
edges = []
for _ in range(n - 1):
    u, v, c = input().split()
    edges.append((int(u), int(v), c))

root = build_tree(edges)
zigzag_traversal(root)
