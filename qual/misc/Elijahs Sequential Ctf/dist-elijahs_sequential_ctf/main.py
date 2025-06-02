n = int(input())
inputs = list(map(int, input().split()))

m = 3  # number of types

# Adjacency matrix
adj = [[0] * m for _ in range(m)]
adj[0][1] = 2
adj[1][2] = 5
adj[0][2] = 3
adj[1][0] = 4
adj[2][0] = 1
adj[2][1] = 6

dp = [-1] * m

for i in range(n):
    x = inputs[i]
    for y in range(m):
        if dp[y] == -1:
            continue
        dp[x] = max(dp[x], dp[y] + adj[y][x])
    dp[x] = max(dp[x], 0)
    

print(max(dp))