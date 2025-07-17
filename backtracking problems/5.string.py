def permute(s, l=0):
    if l == len(s):
        print("".join(s))
    else:
        for i in range(l, len(s)):
            s[l], s[i] = s[i], s[l]
            permute(s, l+1)
            s[l], s[i] = s[i], s[l]  # backtrack

# Example
permute(list("abc"))
