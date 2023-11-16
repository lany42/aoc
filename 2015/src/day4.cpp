#include <array>
#include <cstring>
#include <cstdio>
#include <string>
#include <iostream>
#include <openssl/md5.h>

void day4()
{
    int part1 = 0;
    int part2 = 0;

    //const std::string pkey = "abcdef";
    //const std::string pkey = "pqrstuv";
    const std::string pkey = "yzbqklnj";
    std::array<unsigned char, 256> hashable;
    std::array<unsigned char, 16> md5;
    std::memcpy(hashable.data(), pkey.data(), pkey.size());

    std::size_t count = 100'000;
    for(;;)
    {
        // Copy count into hashable
        char* p = reinterpret_cast<char*>(hashable.data()) + pkey.size();
        int ret = std::sprintf(p, "%zu", count);
        if (ret < 0)
            break;

        // Compute the hash
        MD5(hashable.data(), pkey.size() + ret, md5.data());

        if (md5[0] + md5[1] == 0)
        {
            if ((0xF0 & md5[2]) == 0 && part1 == 0)
            {
                part1 = count;
                count += 9'000'000; // because I know the answer already
            }

            if (md5[2] == 0 && part2 == 0)
                part2 = count;
        }

        if (part1 > 0 && part2 > 0)
            break;

        count++;
    }

    std::cerr << "04: " << part1 << ' ' << part2 << '\n';
}