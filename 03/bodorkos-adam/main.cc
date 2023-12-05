#include <exception>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

void solve_puzzle_1(std::vector<std::string> const&);
void solve_puzzle_2(std::vector<std::string> const&);

std::vector<std::string> read_input()
{
    std::vector<std::string> lines;
    std::ifstream file {"input.txt"};

    for (std::string line; std::getline(file, line);)
    {
        lines.emplace_back(std::move(line));
    }

    return lines;
}

int main()
{
    try
    {
        const std::vector<std::string> lines = read_input();

        solve_puzzle_1(lines);
        solve_puzzle_2(lines);

        return 0;
    }
    catch (std::exception const& exception)
    {
        std::cerr << "exception thrown: " << exception.what() << std::endl;
    }
    catch (...)
    {
        std::cerr << "unknown exception thrown" << std::endl;
    }

    return 1;
}
