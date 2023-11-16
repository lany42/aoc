#include <days.hpp>
#include <iostream>
#include <fstream>

void day1()
{
    std::ifstream f("inputs/day1.txt");
    if (!f.is_open())
    {
        std::cerr << "Failed to open\n";
        return;
    }

    int part1 = 0;
    int part2 = 0;
    int pos = 1;
    bool part2_found = false;
    while (1)
    {
        char c = static_cast<char>(f.get());
        if (f.eof())
            break;

        switch (c)
        {
            case 40:
                part1++;
                break;
            case 41:
                part1--;
                break;

            default:
            {
                std::cerr << "bad input\n";
                return;
            }
        }

        if (part1 == -1 && !part2_found)
        {
            part2 = pos;
            part2_found = true;
        }

        pos++;
    }
    std::cerr << "01: " << part1 << ' ' << part2 << '\n';
}