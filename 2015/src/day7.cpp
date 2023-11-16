#include <fstream>
#include <iostream>
#include <map>
#include <cstdint>
#include <type_traits>
#include <cstdlib>
#include <sstream>

std::map<std::string, std::uint16_t> wires;

// 'N -> aa'
void value_assignment(std::istream& f)
{
    std::string dest;
    std::uint16_t value;

    // 'N -> ';
    f >> value;
    f.ignore(4);

    // 'aa'
    f >> dest;

    wires[dest] = value;
}

// 'aa -> bb'
void wire_assignment(std::istream& f)
{
    std::string src;
    std::string dest;

    // 'aa -> '
    f >> src;
    f.ignore(4);

    // 'bb'
    f >> dest;

    wires[dest] = wires[src];
}

// 'NOT aa -> bb'
void not_gate(std::istream& f)
{
    std::string src;
    std::string dest;

    // 'NOT aa'
    f.ignore(4);
    f >> src;
    
    // ' -> bb'
    f.ignore(4);
    f >> dest;

    // bb == ~aa
    wires[dest] = ~wires[src];
}

// 'aa AND bb -> cc'
void and_gate(std::istream& f)
{
    std::string one;
    std::string two;
    std::string dest;

    // 'aa AND '
    f >> one;
    f.ignore(5);

    // 'bb -> '
    f >> two;
    f.ignore(4);

    // 'cc'
    f >> dest;

    wires[dest] = wires[one] & wires[two];
}

// '1 AND aa -> bb'
void one_and(std::istream& f)
{
    std::string src;
    std::string dest;

    // '1 AND '
    f.ignore(6);

    // 'aa -> '
    f >> src;
    f.ignore(4);

    // 'bb'
    f >> dest;

    wires[dest] = 1 & wires[src];
}

// 'aa OR bb -> cc'
void or_gate(std::istream& f)
{
    std::string one;
    std::string two;
    std::string dest;

    // 'aa OR '
    f >> one;
    f.ignore(4);

    // 'bb -> '
    f >> two;
    f.ignore(4);

    // 'cc'
    f >> dest;

    wires[dest] = wires[one] | wires[two];
}

// 'aa LSHIFT N -> bb'
void lshift_gate(std::istream& f)
{
    std::string src;
    std::string dest;
    std::uint16_t by;

    // 'aa LSHIFT '
    f >> src;
    f.ignore(8);

    // 'N -> '
    f >> by;
    f.ignore(4);

    // 'bb'
    f >> dest;

    wires[dest] = wires[src] << by;
}

// 'aa RSHIFT N -> bb'
void rshift_gate(std::istream& f)
{
    std::string src;
    std::string dest;
    std::uint16_t by;

    // 'aa RSHIFT '
    f >> src;
    f.ignore(8);

    // 'N -> '
    f >> by;
    f.ignore(4);

    // 'bb'
    f >> dest;

    wires[dest] = wires[src] >> by;
}

int peek_n(std::istream& f, int n)
{
    std::size_t start= f.tellg();
    f.seekg(n, std::ios::cur);

    int result = f.peek();
    f.seekg(start);
    return result;
}

// Seek until first space, reset positon, return the next char
int check_gate(std::istream& f)
{
    std::size_t start = f.tellg();
    while (f.peek() != ' ')
        f.seekg(1, std::ios::cur);

    f.seekg(1, std::ios::cur);

    int result = f.peek();
    f.seekg(start);
    return result;
}

void select_gate(std::istream& f)
{
    switch(check_gate(f))
    {
        case 'A':
            and_gate(f);
            break;

        case 'O':
            or_gate(f);
            break;

        case 'L':
            lshift_gate(f);
            break;

        case 'R':
            rshift_gate(f);
            break;

        case '-':
            wire_assignment(f);
            break;

        default:
        {
            std::cerr << "Error selecting gate\n";
            std::exit(1);
        }
    }
}

const char* test1 =
"123 -> x\n"
"456 -> y\n"
"x AND y -> d\n"
"x OR y -> e\n"
"x LSHIFT 2 -> f\n"
"y RSHIFT 2 -> g\n"
"NOT x -> h\n"
"NOT y -> i";

void day7()
{
    std::ifstream f("inputs/day7.txt");
    //std::istringstream f(test1);
    decltype(f)::traits_type e;
    if (!f.is_open())
    {
        std::cerr << "Failed to open\n";
        return;
    }

    int part1 = 0;
    int part2 = 0;


    while (f.good())
    {
        int p = f.peek();
        //std::cerr << char(p) << ":" << f.tellg() << '\n';
        switch(p)
        {
            // Traits::eof
            case e.eof(): break;

            // 0123456789
            case '0' ... '9':
            {
                if (peek_n(f, 2) == 'A')
                    one_and(f);

                else
                    value_assignment(f);

                break;
            }

            // 'N'
            case 'N':
            {
                not_gate(f);
                break;
            }

            // lowercase letters
            case 'a' ... 'z':
                select_gate(f);
                break;

            // All others
            default:
                std::cerr << "Error in first char: " << char(p) << '\n';
                f.ignore();
        }
        // '\n'
        f.ignore();

        for (const auto& pair : wires)
            std::cerr << pair.first << " = " << pair.second << '\n';

        std::cin.ignore();
    }

    for (const auto& pair : wires)
        std::cerr << pair.first << " = " << pair.second << '\n';

    std::cerr << "07: " << part1 << ' ' << part2 << '\n';
}