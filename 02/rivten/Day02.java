import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;
import java.util.Map;
import java.util.HashMap;

class Day02 {
    private record Game(int id, Map<String, Integer> seen) {
        private int power() {
            return seen().getOrDefault("red", 0)
                * seen().getOrDefault("green", 0)
                * seen().getOrDefault("blue", 0);
        }
    }

    private static boolean isGameOk(Game g) {
        return g.seen().getOrDefault("red", 0) <= 12
            && g.seen().getOrDefault("green", 0) <= 13
            && g.seen().getOrDefault("blue", 0) <= 14;
    }

    private static Game parse(String line) {
        var seen = new HashMap<String, Integer>();
        var colonSplit = line.split(":");
        var stringId = colonSplit[0].split(" ")[1];
        var id = Integer.parseInt(stringId);
        var rounds = colonSplit[1].split("; ");
        for (var round: rounds) {
            var balls = round.split(", ");
            for (var ball: balls) {
                var parsed = ball.trim().split(" ");
                var count = Integer.parseInt(parsed[0]);
                var color = parsed[1];
                seen.put(color, Math.max(count, seen.getOrDefault(color, 0)));
            }
        }
        return new Game(id, seen);
    }
    public static void main(String[] args) {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        //int sol = bi.lines()
        //    .map(Day02::parse)
        //    .filter(Day02::isGameOk)
        //    .mapToInt(Game::id)
        //    .sum();
        int sol = bi.lines()
            .map(Day02::parse)
            .mapToInt(Game::power)
            .sum();

        System.out.println(sol);
    }
}
