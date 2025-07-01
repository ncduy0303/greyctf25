#include <iostream>
#include <cstdint>
using namespace std;

// Number of bytes in a block and number of rounds per block
constexpr int N      = 5;
constexpr int ROUNDS = 1000;

// Ask GCC/Clang to do ofast, unroll, inline
#pragma GCC optimize("Ofast,unroll-loops")
// (remove the above pragma if your compiler doesn’t support it)

inline uint8_t rotl8(uint8_t x, int n) {
    // single instr on x86
    return (x << n) | (x >> (8 - n));
}

// Encrypt exactly one 5-byte block in registers
inline void encrypt_block(const uint8_t* __restrict pt,
                          uint8_t*       __restrict ct,
                          const uint8_t* __restrict key)
{
    uint8_t s0 = pt[0];
    uint8_t s1 = pt[1];
    uint8_t s2 = pt[2];
    uint8_t s3 = pt[3];
    uint8_t s4 = pt[4];

    for (int t = 0; t < ROUNDS; ++t) {
        // key addition round 1
        s0 += key[0]; s1 += key[1]; s2 += key[2];
        s3 += key[3]; s4 += key[4];

        // mix
        s0 += s1;
        s3 = rotl8(s3 ^ s0, 1);
        s2 += s4;
        s0 = rotl8(s0 ^ s2, 7);
        s1 += s2;
        s4 = rotl8(s4 ^ s1, 2);

        // key addition round 2
        s0 += key[0]; s1 += key[1]; s2 += key[2];
        s3 += key[3]; s4 += key[4];
    }

    ct[0] = s0;
    ct[1] = s1;
    ct[2] = s2;
    ct[3] = s3;
    ct[4] = s4;
}

// Encrypt two consecutive 5-byte blocks
inline void encrypt2(const uint8_t* pt,
                     uint8_t*       ct,
                     const uint8_t* key)
{
    encrypt_block(pt,     ct,     key);
    encrypt_block(pt + N, ct + N, key);
}

// Quick checks on only the necessary bytes
inline bool check_first(const uint8_t* ct, const uint8_t* corr) {
    return ct[1]==corr[1] && ct[2]==corr[2] && ct[4]==corr[4]
        && ct[6]==corr[6] && ct[7]==corr[7] && ct[9]==corr[9];
}
inline bool check_second(const uint8_t* ct, const uint8_t* corr) {
    return ct[0]==corr[0] && ct[3]==corr[3]
        && ct[5]==corr[5] && ct[8]==corr[8];
}

int main() {
    const uint8_t pt[10]    = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    const uint8_t corr[10]  = {178, 242, 67, 76, 246, 226, 121, 52, 210, 81};
    uint8_t best1_k1=0, best1_k2=0, best1_k4=0;
    uint8_t ct[10];

    // Phase 1: brute-force key[1], key[2], key[4]
    for (int k1 = 0; k1 < 256; ++k1) {
        cout << "Trying k1=" << k1 << endl;
      for (int k2 = 0; k2 < 256; ++k2) {
        for (int k4 = 0; k4 < 256; ++k4) {
          uint8_t key[5] = {0, uint8_t(k1), uint8_t(k2), 0, uint8_t(k4)};
          encrypt2(pt, ct, key);
          if (check_first(ct, corr)) {
            best1_k1 = k1;
            best1_k2 = k2;
            best1_k4 = k4;
            goto PHASE2;  // break out of all three loops immediately
          }
        }
      }
    }

PHASE2:
    // Phase 2: brute-force key[0], key[3]
    for (int k0 = 0; k0 < 256; ++k0) {
      for (int k3 = 0; k3 < 256; ++k3) {
        uint8_t key[5] = {
          uint8_t(k0), best1_k1, best1_k2, uint8_t(k3), best1_k4
        };
        encrypt2(pt, ct, key);
        if (check_second(ct, corr)) {
          cout << "Key found: "
               << k0 << ' '
               << int(best1_k1) << ' '
               << int(best1_k2) << ' '
               << k3 << ' '
               << int(best1_k4)
               << "\n";
          return 0;
        }
      }
    }

    return 0;
}
