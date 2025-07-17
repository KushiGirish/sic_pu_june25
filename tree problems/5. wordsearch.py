class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Stores the word at the end node

def build_trie(words):
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = word  # Mark end of word
    return root

def find_words(board, words):
    root = build_trie(words)
    result = set()
    m, n = len(board), len(board[0])

    def dfs(i, j, node):
        char = board[i][j]
        if char not in node.children:
            return
        
        next_node = node.children[char]
        if next_node.word:
            result.add(next_node.word)
            next_node.word = None  # Avoid duplicate
        
        board[i][j] = '#'  # Mark as visited

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            x, y = i + dx, j + dy
            if 0 <= x < m and 0 <= y < n and board[x][y] != '#':
                dfs(x, y, next_node)

        board[i][j] = char  # Restore character

    for i in range(m):
        for j in range(n):
            dfs(i, j, root)

    return result

# Input Reading
m, n = map(int, input().split())
board = []
for _ in range(m):
    board.append(input().split())

k = int(input())
words = [input().strip() for _ in range(k)]

# Solve and print
found_words = find_words(board, words)
for word in found_words:
    print(word)
