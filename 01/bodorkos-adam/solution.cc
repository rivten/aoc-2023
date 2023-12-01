#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <string>
#include <string_view>
#include <vector>

bool is_valid_digit(const char c)
{
    return (c >= '1' && c <= '9');
};

void solve_puzzle_1(std::vector<std::string> const& lines)
{
    const int sum = std::accumulate(lines.begin(), lines.end(), 0,
        [](const int sum, std::string const& line)
        {
            const char digit_1 = *std::find_if(line.begin(), line.end(), is_valid_digit);
            const char digit_2 = *std::find_if(line.rbegin(), line.rend(), is_valid_digit);

            return (sum + (digit_1 - '0') * 10 + (digit_2 - '0'));
        }
    );

    std::cout << sum << std::endl;
}

void solve_puzzle_2(std::vector<std::string> const& lines)
{
    using namespace std::literals::string_view_literals;

     const int sum = std::accumulate(lines.begin(), lines.end(), 0,
        [](const int sum, std::string const& line)
        {
            int digit_1 {0};
            int digit_2 {0};

            const auto set_digit =
                [&digit_1, &digit_2](int value)
                {
                    ((digit_1 == 0) ? digit_1 : digit_2) = value;
                };

            for (std::string_view view {line}; !view.empty(); view.remove_prefix(1))
            {
                if (is_valid_digit(view[0]))
                {
                    set_digit(view[0] - '0');
                }
                else
                {
                    static const std::array<std::string_view, 9> digit_names =
                    {
                        "one"sv, "two"sv, "three"sv, "four"sv, "five"sv, "six"sv, "seven"sv, "eight"sv, "nine"sv
                    };

                    for (int i = 0; i < digit_names.size(); ++i)
                    {
                        if (view.starts_with(digit_names[i]))
                        {
                            set_digit(i + 1);
                            break;
                        }
                    }
                }
            }

            return (digit_2 == 0)
                ? (sum + digit_1 * 10 + digit_1)
                : (sum + digit_1 * 10 + digit_2);
        }
    );

    std::cout << sum << std::endl;
}
