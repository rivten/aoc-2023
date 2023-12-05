#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

using namespace std::literals::string_view_literals;

class Draw
{
public:
    explicit Draw(std::string input)
    {
        std::istringstream stream {std::move(input)};

        stream >> num_;
        stream >> color_;
    }

    std::string_view color() const
    {
        return color_;
    }

    int num() const
    {
        return num_;
    };

private:
    std::string color_;
    int num_;
};

class Reveal
{
public:
    explicit Reveal(std::string input)
    {
        std::istringstream stream {std::move(input)};

        for (std::string draw; std::getline(stream, draw, ',');)
        {
            draws_.emplace_back(std::move(draw));
        }
    }

    bool is_possible() const
    {
        static const std::map<std::string_view, int> max_cubes_by_color =
        {
            {"red"sv, 12},
            {"green"sv, 13},
            {"blue"sv, 14},
        };

        for (Draw const& draw : draws_)
        {
            if (draw.num() > max_cubes_by_color.find(draw.color())->second)
            {
                return false;
            }
        }

        return true;
    }

private:
    std::vector<Draw> draws_;
};

class Game
{
public:
    explicit Game(std::string input)
    {
        std::istringstream stream {std::move(input)};

        stream.ignore("Game "sv.size());
        stream >> id_;
        stream.ignore(1);

        for (std::string reveal; std::getline(stream, reveal, ';');)
        {
            reveals_.emplace_back(std::move(reveal));
        }
    }

    int id() const
    {
        return id_;
    }

    bool is_possible() const
    {
        for (Reveal const& reveal : reveals_)
        {
            if (!reveal.is_possible())
            {
                return false;
            }
        }

        return true;
    }

private:
    int id_;
    std::vector<Reveal> reveals_;
};

void solve_puzzle_1(std::vector<std::string> const& lines)
{
    const int sum = std::accumulate(lines.begin(), lines.end(), 0,
        [](const int sum, std::string const& line)
        {
            const Game game {line};

            return sum + (game.is_possible() ? game.id() : 0);
        }
    );

    std::cout << sum << std::endl;
}

void solve_puzzle_2(std::vector<std::string> const& lines)
{
    const int sum {0};

    std::cout << sum << std::endl;
}
