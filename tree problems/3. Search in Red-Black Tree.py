class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# Build tree using dictionary
def build_tree(n, node_info):
    nodes = {}

    # First, create all nodes
    for val, left, right in node_info:
        if val not in nodes:
            nodes[val] = Node(val)
        if left != -1 and left not in nodes:
            nodes[left] = Node(left)
        if right != -1 and right not in nodes:
            nodes[right] = Node(right)

    # Then, assign children
    for val, left, right in node_info:
        node = nodes[val]
        node.left = nodes[left] if left != -1 else None
        node.right = nodes[right] if right != -1 else None

    # Return the root (first inserted node)
    return nodes[node_info[0][0]]

# Search in BST
def search(root, key):
    if not root:
        return "Not Found"
    if root.val == key:
        return "Found"
    elif key < root.val:
        return search(root.left, key)
    else:
        return search(root.right, key)

# Input Reading
n = int(input())
node_info = []
for _ in range(n):
    val, left, right = map(int, input().split())
    node_info.append((val, left, right))

k = int(input())

# Build tree and search
root = build_tree(n, node_info)
print(search(root, k))
