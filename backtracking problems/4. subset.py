def subset_sum(nums, target):
    def dfs(i, curr_sum):
        if curr_sum == target:
            return True
        if i == len(nums) or curr_sum > target:
            return False
        return dfs(i + 1, curr_sum + nums[i]) or dfs(i + 1, curr_sum)

    return dfs(0, 0)

# Example
print(subset_sum([3, 34, 4, 12, 5, 2], 9))  # Output: True
