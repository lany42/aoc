#include <days.hpp>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>
#include <vector>

struct Point2
{
    int x;
    int y;

    Point2() = default;
    Point2(int x, int y)
        : x(x)
        , y(y)
    {}
};

bool operator==(const Point2& a, const Point2& b)
{
    return (a.x == b.x) && (a.y == b.y);
}

bool operator<(const Point2& a, const Point2&b)
{
    return a.x == b.x ? a.y < b.y : a.x < b.x;
}

int part1_solver(std::string& line)
{
    std::vector<Point2> houses;
    houses.reserve(line.size());

    // Starting house
    int x = 0;
    int y = 0;
    houses.emplace_back(x, y);

    for (const char c : line)
    {
        switch(c)
        {
            case 60:    x--;    break; // <
            case 62:    x++;    break; // >
            case 94:    y++;    break; // ^
            case 118:   y--;    break; // v
            default:
                std::cerr << "invalid_input\n";
                return 0;
        }

        Point2 p(x, y);
        auto upper = std::upper_bound(begin(houses), end(houses), p);
        houses.insert(upper, p);
    }

    int uniques = 0;
    auto current = houses.begin();
    for(;;)
    {
        auto upper = std::upper_bound(current, end(houses), *current);
        auto count = std::distance(current, upper);
        current += count;
        uniques++;
        if (upper == end(houses))
            break;
    }

    return uniques;
}

int part2_solver(std::string& line)
{
    std::vector<Point2> houses;
    houses.reserve(line.size());

    // Starting house
    int x = 0;
    int y = 0;
    houses.emplace_back(x, y);

    int x1 = 0;
    int y1 = 0;

    for (auto iter = begin(line); iter != end(line); iter += 2)
    {
        char c1 = *iter;
        char c2 = *(iter + 1);

        switch(c1)
        {
            case 60:    x--;    break; // <
            case 62:    x++;    break; // >
            case 94:    y++;    break; // ^
            case 118:   y--;    break; // v
            default:
                std::cerr << "invalid_input\n";
                return 0;
        }

        Point2 p(x, y);
        auto upper = std::upper_bound(begin(houses), end(houses), p);
        houses.insert(upper, p);

        switch(c2)
        {
            case 60:    x1--;    break; // <
            case 62:    x1++;    break; // >
            case 94:    y1++;    break; // ^
            case 118:   y1--;    break; // v
            default:
                std::cerr << "invalid_input\n";
                return 0;
        }

        Point2 p1(x1, y1);
        upper = std::upper_bound(begin(houses), end(houses), p1);
        houses.insert(upper, p1);
    }

    int uniques = 0;
    auto current = houses.begin();
    for(;;)
    {
        auto upper = std::upper_bound(current, end(houses), *current);
        auto count = std::distance(current, upper);
        current += count;
        uniques++;
        if (upper == end(houses))
            break;
    }

    return uniques;
}

std::string test_value_1 = "^>v<";

void day3()
{
    std::ifstream f("inputs/day3.txt");
    if (!f.is_open())
    {
        std::cerr << "Failed to open\n";
        return;
    }

    int part1 = 0;
    int part2 = 0;

    for (std::string line; std::getline(f, line);)
    {
        //part1 = part1_solver(test_value_1);
        part1 = part1_solver(line);
        part2 = part2_solver(line);
    }

    std::cerr << "03: " << part1 << ' ' << part2 << '\n';
}