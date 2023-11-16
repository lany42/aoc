#include <days.hpp>
#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>

int surface_area(int l, int w, int h)
{
    return (2*l*w) + (2*w*h) + (2*h*l);
}

int smallest_side(int l, int w, int h)
{
    int lw = l*w;
    int wh = w*h;
    int hl = h*l;

    int r = lw < wh ? lw : wh;
    return r < hl ? r : hl;
}

int smallest_perimeter(int l, int w, int h)
{
    int lw = 2 * (l + w);
    int wh = 2 * (w + h);
    int hl = 2 * (h + l);

    int r = lw < wh ? lw : wh;
    return r < hl ? r : hl;
}

void day2()
{
    std::ifstream f("inputs/day2.txt");
    if (!f.is_open())
    {
        std::cerr << "Failed to open\n";
        return;
    }

    int part1 = 0;
    int part2 = 0;

    for (std::string line; std::getline(f, line);)
    {
        int l, w, h;
        int ret = std::sscanf(line.data(), "%dx%dx%d\n", &l, &w, &h);
        if (ret == 3)
        {
            part1 += surface_area(l, w, h) + smallest_side(l, w, h);
            part2 += smallest_perimeter(l, w, h) + (l * w * h);
        }
    }

    std::cerr << "02: " << part1 << ' ' << part2 << '\n';
}