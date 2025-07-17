n, x = map(int, input().split())
A = list(map(int, input().split()))
operations = [input().strip() for _ in range(n)]

stack = []
pointer = 0
current_sum = 0

for op in operations:
    if op == "Harry":
        stack.append(A[pointer])
        current_sum += A[pointer]
        pointer += 1
    elif op == "Remove" and stack:
        current_sum -= stack.pop()
    
    if current_sum == x:
        print(len(stack))
        break
else:
    print(-1)
