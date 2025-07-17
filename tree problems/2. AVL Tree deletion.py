class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def getHeight(root):
    return root.height if root else 0

def getBalance(root):
    return getHeight(root.left) - getHeight(root.right) if root else 0

def rightRotate(y):
    x = y.left
    T2 = x.right

    # Perform rotation
    x.right = y
    y.left = T2

    # Update heights
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))
    x.height = 1 + max(getHeight(x.left), getHeight(x.right))

    return x

def leftRotate(x):
    y = x.right
    T2 = y.left

    # Perform rotation
    y.left = x
    x.right = T2

    # Update heights
    x.height = 1 + max(getHeight(x.left), getHeight(x.right))
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))

    return y

def insert(root, key):
    if not root:
        return Node(key)
    elif key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    # Update height
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    # Rebalance
    balance = getBalance(root)

    # 4 Cases
    if balance > 1 and key < root.left.key:
        return rightRotate(root)
    if balance < -1 and key > root.right.key:
        return leftRotate(root)
    if balance > 1 and key > root.left.key:
        root.left = leftRotate(root.left)
        return rightRotate(root)
    if balance < -1 and key < root.right.key:
        root.right = rightRotate(root.right)
        return leftRotate(root)

    return root

def minValueNode(root):
    while root.left:
        root = root.left
    return root

def delete(root, key):
    if not root:
        return root
    elif key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        # Node with 1 or 0 children
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        temp = minValueNode(root.right)
        root.key = temp.key
        root.right = delete(root.right, temp.key)

    # Update height
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    # Rebalance
    balance = getBalance(root)

    # 4 Cases
    if balance > 1 and getBalance(root.left) >= 0:
        return rightRotate(root)
    if balance > 1 and getBalance(root.left) < 0:
        root.left = leftRotate(root.left)
        return rightRotate(root)
    if balance < -1 and getBalance(root.right) <= 0:
        return leftRotate(root)
    if balance < -1 and getBalance(root.right) > 0:
        root.right = rightRotate(root.right)
        return leftRotate(root)

    return root

def inorder(root):
    return inorder(root.left) + [root.key] + inorder(root.right) if root else []

# Main I/O Handler
N = int(input())
values = list(map(int, input().split()))
K = int(input())

# Build AVL Tree
root = None
for val in values:
    root = insert(root, val)

# Delete and print in-order
root = delete(root, K)
print(*inorder(root))
