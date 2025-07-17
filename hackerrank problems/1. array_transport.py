n = int(input())
arr = list(map(int, input().split()))
m = int(input())
brr = list(map(int, input().split()))

count_arr = Counter(arr)
count_brr = Counter(brr)

missing = []
for num in count_brr:
    if count_brr[num] > count_arr.get(num, 0):
        missing.append(num)

missing.sort()
print(" ".join(map(str, missing)))