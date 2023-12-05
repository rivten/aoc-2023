#include <iostream>
#include <numeric>
#include <string>
#include <vector>

void solve_puzzle_1(std::vector<std::string> const& lines)
{
    const int sum = std::accumulate(lines.begin(), lines.end(), 0,
        [](const int sum, std::string const& line)
        {
            return sum;
        }
    );

    std::cout << sum << std::endl;
}

void solve_puzzle_2(std::vector<std::string> const& lines)
{
    const int sum = std::accumulate(lines.begin(), lines.end(), 0,
        [](const int sum, std::string const& line)
        {
            return sum;
        }
    );

    std::cout << sum << std::endl;
}
