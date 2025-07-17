T = int(input())

for _ in range(T):
    N, current = input().split()
    N = int(N)
    current = int(current)
    
    stack = [current]  # stack to track who passed to whom
    
    for _ in range(N):
        parts = input().split()
        if parts[0] == 'P':
            new_id = int(parts[1])
            stack.append(new_id)
        elif parts[0] == 'B':
            stack.pop()  # go back to the previous player
            
    print(stack[-1])  # player with the ball at the end
