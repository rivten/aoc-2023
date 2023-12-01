#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

void solve_puzzle_1(std::vector<std::string> const& lines)
{
    const int sum = std::accumulate(lines.begin(), lines.end(), 0,
        [](const int sum, std::string const& line)
        {
            const auto is_digit =
                [](const char c)
                {
                    return (c >= '0' && c <= '9');
                };

            const char digit_1 = *std::find_if(line.begin(), line.end(), is_digit);
            const char digit_2 = *std::find_if(line.rbegin(), line.rend(), is_digit);

            return (sum + (digit_1 - '0') * 10 + (digit_2 - '0'));
        }
    );

    std::cout << sum << std::endl;
}

void solve_puzzle_2(std::vector<std::string> const& lines)
{
    // @todo
}
