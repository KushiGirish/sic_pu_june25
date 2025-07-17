n, x, y = map(int, input().split())
arr = list(map(int, input().split()))

arr.sort()  # Sorting is key

# The best dividing point is at index x
# The smallest possible p that satisfies arr[x - 1] > p and arr[x] < p
# So the p must be between arr[x-1] and arr[x] (exclusive)

if arr[x - 1] < arr[x]:
    print(arr[x] - arr[x - 1] - 1)
else:
    print(0)
