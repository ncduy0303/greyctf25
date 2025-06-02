#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int n; cin >> n;
    const int m = 3; // number of types
    vector<vector<int>> adj(m, vector<int>(m, 0));
    adj[0][1] = 2;
    adj[1][2] = 5;
    adj[0][2] = 3;
    adj[1][0] = 4;
    adj[2][0] = 1;
    adj[2][1] = 6;
    vector<int> dp(m, -1);
    for (int i = 0; i < n; i++) {
        int x; cin >> x;
        for (int y = 0; y < m; y++) {
            if (dp[y] == -1) continue;
            dp[x] = max(dp[x], dp[y] + adj[y][x]);
        }
        dp[x] = max(dp[x], 0);
    }
    int res = max(dp[0], max(dp[1], dp[2]));
    cout << res << endl;
    return 0;
}