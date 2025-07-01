#include <iostream>
#include <cstring>
#include <cstdint>

using namespace std;

#define N 5

uint8_t key[N];
uint8_t pt[10] = {1, 2, 3, 4, 5};
uint8_t correct_ct[10] = {178, 242, 67, 76, 246};
uint8_t ct[10];

// 8-bit left rotation
inline uint8_t rotl8(uint8_t x, int n) {
    return (x << n) | (x >> (8 - n));
}

// Core block transformation
inline void block(uint8_t* s) {
    for (int i = 0; i < N; ++i) s[i] += key[i];

    s[0] += s[1];
    s[3] = rotl8(s[3] ^ s[0], 1);

    s[2] += s[4];
    s[0] = rotl8(s[0] ^ s[2], 7);

    s[1] += s[2];
    s[4] = rotl8(s[4] ^ s[1], 2);

    for (int i = 0; i < N; ++i) s[i] += key[i];
}

// Encryption of data in 5-byte blocks
void encrypt(const uint8_t* pt, uint8_t* out, size_t len) {
    memcpy(out, pt, len);
    for (size_t i = 0; i < len; i += N) {
        for (int t = 0; t < 1000; ++t)
            block(out + i);
    }
}

// Phase 1: Search partial key [1,2,4]
void find_first() {
    for (int k1 = 0; k1 < 255; ++k1) {
        cout << "Trying k1 = " << k1 << endl;
        key[1] = k1;
        for (int k2 = 0; k2 < 255; ++k2) {
            key[2] = k2;
            for (int k4 = 0; k4 < 255; ++k4) {
                key[4] = k4;
                encrypt(pt, ct, 5);
                if (ct[1] == correct_ct[1] && ct[2] == correct_ct[2] &&
                    ct[4] == correct_ct[4])
                    return;
            }
        }
    }
}

// Phase 2: Complete key with [0,3]
void find_second() {
    for (int k0 = 0; k0 < 255; ++k0) {
        key[0] = k0;
        for (int k3 = 0; k3 < 255; ++k3) {
            key[3] = k3;
            encrypt(pt, ct, 5);
            if (ct[0] == correct_ct[0] && ct[3] == correct_ct[3]) {
                cout << "Key found: ";
                for (int i = 0; i < N; ++i)
                    cout << (int)key[i] << " ";
                cout << endl;
                return;
            }
        }
    }
}

int main() {
    find_first();
    find_second();
}
