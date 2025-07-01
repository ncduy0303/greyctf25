#include <iostream>
#include <vector>
#include <cstdint>
#include <cstring>   // for std::memcpy
#include <cstdlib>   // for EXIT_FAILURE, EXIT_SUCCESS

namespace {
    constexpr int N      = 5;
    constexpr int ROUNDS = 1000;
    uint8_t key[N];

    // 8-bit left rotation
    inline uint8_t rotl8(uint8_t x, int n) {
        return static_cast<uint8_t>((x << n) | (x >> (8 - n)));
    }

    // one “block” of the cipher
    inline void block(uint8_t* state) {
        // key-add round
        for (int i = 0; i < N; ++i)
            state[i] = static_cast<uint8_t>(state[i] + key[i]);

        // mix layer
        state[0] = static_cast<uint8_t>(state[0] + state[1]);
        state[3] = rotl8(state[3] ^ state[0], 1);

        state[2] = static_cast<uint8_t>(state[2] + state[4]);
        state[0] = rotl8(state[0] ^ state[2], 7);

        state[1] = static_cast<uint8_t>(state[1] + state[2]);
        state[4] = rotl8(state[4] ^ state[1], 2);

        // key-add round
        for (int i = 0; i < N; ++i)
            state[i] = static_cast<uint8_t>(state[i] + key[i]);
    }

    // encrypt len bytes (must be multiple of N)
    void encrypt(const std::vector<uint8_t>& pt,
                 std::vector<uint8_t>&       ct) 
    {
        std::memcpy(ct.data(), pt.data(), pt.size());
        for (size_t off = 0; off < pt.size(); off += N) {
            uint8_t* blk = ct.data() + off;
            for (int r = 0; r < ROUNDS; ++r) {
                block(blk);
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <length> <key-as-uint64>\n";
        return EXIT_FAILURE;
    }

    // parse arguments
    const size_t LEN = std::stoul(argv[1]);
    const uint64_t K = std::stoull(argv[2]);

    // split 40-bit key into five bytes
    key[0] = static_cast<uint8_t>((K >> 32) & 0xFF);
    key[1] = static_cast<uint8_t>((K >> 24) & 0xFF);
    key[2] = static_cast<uint8_t>((K >> 16) & 0xFF);
    key[3] = static_cast<uint8_t>((K >>  8) & 0xFF);
    key[4] = static_cast<uint8_t>((K      ) & 0xFF);

    // allocate buffers
    std::vector<uint8_t> pt(LEN), ct(LEN);

    // read plaintext from stdin
    if (!std::cin.read(reinterpret_cast<char*>(pt.data()), LEN)) {
        std::cerr << "Error: failed to read " << LEN << " bytes from stdin\n";
        return EXIT_FAILURE;
    }

    // encrypt
    encrypt(pt, ct);

    // write ciphertext to stdout
    if (!std::cout.write(reinterpret_cast<const char*>(ct.data()), LEN)) {
        std::cerr << "Error: failed to write " << LEN << " bytes to stdout\n";
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
