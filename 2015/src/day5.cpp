#include <array>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

bool is_vowel(char c)
{
    switch(c)
    {
        // aeiou
        case 97:
        case 101:
        case 105:
        case 111:
        case 117:
            return true;

        default:
            return false;
    }
}

struct Pair
{
    char c1;
    char c2;
    int i1;
    int i2;

    Pair() = default;
    Pair(char a, char b)
        : c1(a)
        , c2(b)
    {}

    size_t n_vowels()
    {
        size_t n = 0;
        if (is_vowel(c1)) n++;
        if (is_vowel(c2)) n++;
        return n;
    }

    bool is_pair()
    {
        return c1 == c2;
    }
};

bool operator==(const Pair& a, const Pair& b)
{
    return (a.c1 == b.c1) && (a.c2 == b.c2);
}

bool operator<(const Pair& a, const Pair& b)
{
    return a.c1 == b.c1 ? a.c2 < b.c2 : a.c1 < b.c1;
}

bool overlaps(const Pair& even, const Pair& odd)
{
    return 
            (even.i1 == odd.i2)     // Even pair is right of odd pair
        ||  (even.i2 == odd.i1);    // Even pair is left of odd pair
}

bool has_repeated_pair(const std::vector<Pair>& sorted)
{
    auto current = begin(sorted);
    for(;;)
    {
        auto upper = std::upper_bound(current, end(sorted), *current);
        auto count = std::distance(current, upper);
        if (count > 1)
        {
            std::cerr << (*current).c1 << ' ' << (*current).c2;
            return true;
        }

        if (upper == end(sorted))
            return false;

        current += count;
    }
}

bool has_repeated_pair_2(const std::vector<Pair>& even, const std::vector<Pair>& odd)
{
    for (const auto pair : odd)
    {
        auto lower = std::lower_bound(begin(even), end(even), pair);
        if (lower == end(even))
            continue;

        if (!(pair < *lower) && !overlaps(*lower, pair))
        {
            std::cerr << pair.c1 << ' ' << pair.c2;
            return true;
        }
    }

    return false;
}

std::array<Pair, 4> banned_pairs{
    Pair('a', 'b'),
    Pair('c', 'd'),
    Pair('p', 'q'),
    Pair('x', 'y')
};

bool is_banned(const Pair& p)
{
    for (const Pair& bp : banned_pairs)
    {
        if (p == bp)
            return true;
    }
    return false;
}

bool is_nice(std::string line)
{
    // Part 1
    size_t n_vowels = 0;
    bool has_1_pair = false;
    for (auto iter = begin(line) + 1; iter != end(line) - 1; iter += 2)
    {
        Pair even(*(iter - 1), *iter);
        Pair odd(*iter, *(iter + 1));

        if (is_banned(even) || is_banned(odd))
            return false;

        n_vowels += even.n_vowels();

        if (even.is_pair() || odd.is_pair())
            has_1_pair = true;
    }
    // check last even pair
    Pair last (*(end(line) - 2), *(end(line) - 1));
    if (is_banned(last))
        return false;

    if (last.is_pair())
        has_1_pair = true;

    n_vowels += last.n_vowels();

    if (n_vowels < 3)
        return false;

    if (!has_1_pair)
        return false;

    return true;
}

bool is_nice_2(std::string line)
{
    // Part 2
    std::vector<Pair> evens;
    std::vector<Pair> odds;
    evens.reserve(8);
    odds.reserve(7);

    std::vector<Pair> evens_2;
    std::vector<Pair> odds_2;

    for (auto iter = begin(line) + 1; iter != end(line) - 1; iter += 2)
    {
        evens.emplace_back(*(iter - 1), *iter);
        odds.emplace_back(*iter, *(iter + 1));

        evens.back().i1 = std::distance(begin(line), iter - 1);
        evens.back().i2 = std::distance(begin(line), iter);
        
        odds.back().i1 = std::distance(begin(line), iter);
        odds.back().i1 = std::distance(begin(line), iter + 1);
    }
    evens.emplace_back(*(end(line) - 2), *(end(line) - 1));
    std::sort(begin(evens), end(evens));
    std::sort(begin(odds), end(odds));

    if (    !has_repeated_pair(evens)
        &&  !has_repeated_pair(odds)
        &&  !has_repeated_pair_2(evens, odds)
    )
        return false;

    for (auto iter = begin(line) + 2; iter != end(line) - 2; iter += 2)
        evens_2.emplace_back(*(iter - 2), *iter);

    for (auto iter = begin(line) + 3; iter != end(line) - 1; iter += 2)
        odds_2.emplace_back(*(iter - 2), *iter);

    std::cerr << '\n';
    for (auto p : evens_2)
    {
        if (p.is_pair())
        {
            std::cerr << p.c1 << ' ' << p.c2 << '\n';
            return true;
        }
    }

    std::cerr << '\n';
    for (auto p : odds_2)
    {
        if (p.is_pair())
        {
            std::cerr << p.c1 << ' ' << p.c2 << '\n';
            return true;
        }
    }

    return false;
}

void day5()
{
    std::ifstream f("inputs/day5.txt");
    if (!f.is_open())
    {
        std::cerr << "Failed to open\n";
        return;
    }

    int part1 = 0;
    int part2 = 0;

    std::vector<std::string> tests{
        "ugknbfddgicrmopn",
        "jchzalrnumimnmhp",
        "haegwjzuvuyypxyu",
        "dvszwmarrgswjxmb"
    };

    std::cerr << is_nice_2("qjhvhtzxzqqjkmpb") << '\n';
    std::cerr << is_nice_2("uurcxstgmygtbstg") << '\n';
    std::cerr << is_nice_2("ieodomkazucvgmuy") << '\n';

    for (std::string line; std::getline(f, line);)
    //for (auto line : tests)
    {
        if (is_nice(line))
            part1++;

        if (is_nice_2(line))
            part2++;
    }

    std::cerr << "05: " << part1 << ' ' << part2 << '\n';
}