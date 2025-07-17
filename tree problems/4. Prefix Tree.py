class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.isEnd = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.isEnd

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

# Reading input and performing operations
trie = Trie()
n = int(input())
for _ in range(n):
    op, arg = input().split()
    if op == "insert":
        trie.insert(arg)
    elif op == "search":
        print("true" if trie.search(arg) else "false")
    elif op == "startsWith":
        print("true" if trie.startsWith(arg) else "false")
