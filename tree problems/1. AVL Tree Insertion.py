class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

# Get height of a node
def get_height(node):
    return node.height if node else 0

# Get balance factor
def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

# Right rotate
def right_rotate(y):
    x = y.left
    T2 = x.right

    # Rotation
    x.right = y
    y.left = T2

    # Update heights
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))

    return x

# Left rotate
def left_rotate(x):
    y = x.right
    T2 = y.left

    # Rotation
    y.left = x
    x.right = T2

    # Update heights
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))

    return y

# Insert function
def insert(node, key):
    # Normal BST insertion
    if not node:
        return Node(key)
    elif key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)

    # Update height
    node.height = 1 + max(get_height(node.left), get_height(node.right))

    # Get balance factor
    balance = get_balance(node)

    # Balance the node if needed

    # Left Left
    if balance > 1 and key < node.left.key:
        return right_rotate(node)

    # Right Right
    if balance < -1 and key > node.right.key:
        return left_rotate(node)

    # Left Right
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)

    # Right Left
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

# Preorder traversal
def preorder(node):
    if not node:
        return
    print(node.key, end=" ")
    preorder(node.left)
    preorder(node.right)

# Main
n = int(input())
values = list(map(int, input().split()))

root = None
for val in values:
    root = insert(root, val)

preorder(root)
