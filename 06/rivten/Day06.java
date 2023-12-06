import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

class Day06 {

    private record Race(long t, long d) {
        private long solveCount() {
            // let's call tb the time you press the button.
            // then we have the equation
            // (t - tb) * tb <= d
            // with 0 <= tb <= t
            // also written as
            // tb^2 - t * tb + d > 0 (E)
            // this is a second order equation with
            // a = 1
            // b = -t
            // c = d
            // we need to find how many integer solution does the equation (E) has
            // we can solve (E')
            // tb^2 - t * tb + d = 0 (E')
            // delta = b * b - 4 * a * c
            // delta = t^2 - 4 * d
            // if delta > 0 (which it is always in our input)
            // then we have two solutions
            // s0 = (- b - sqrt(delta)) / (2 * a)
            // s1 = (- b + sqrt(delta)) / (2 * a)
            // since we look for the range, we have:
            // s1 - s0 = sqrt(delta) / a

            var epsilon = 0.001; // epsilon is a hack because we need to be _strictly_ better than t
            var delta = t * t - 4 * d;
            var sqrtDelta = Math.sqrt(delta);
            var s0 = (t - sqrtDelta) / 2.0;
            var s1 = (t + sqrtDelta) / 2.0;
            var start = (long)Math.ceil(Math.max(Math.min(epsilon + s0, t), 0.0));
            var end = (long)Math.floor(Math.max(Math.min(-epsilon + s1, t), 0.0));
            return end + 1 - start;
        }
    }

    private static Race[] parse() {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        var lines = bi.lines().toList();
        var times = Arrays.stream(lines.get(0).split(":")[1].trim().split(" ")).filter(s -> s.length() != 0).map(Long::parseLong).toList();
        var distances = Arrays.stream(lines.get(1).split(":")[1].trim().split(" ")).filter(s -> s.length() != 0).map(Long::parseLong).toList();
        var races = new Race[times.size()];
        for (int i = 0; i < times.size(); ++i) {
            races[i] = new Race(times.get(i), distances.get(i));
        }
        
        return races;
    }

    private static Race parseRace() {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        var lines = bi.lines().toList();
        var t = Long.parseLong(lines.get(0).split(":")[1].replaceAll("\\s", ""));
        var d = Long.parseLong(lines.get(1).split(":")[1].replaceAll("\\s", ""));
        return new Race(t, d);
    }

    public static void main(String[] args) {
        //var races = parse();
        //var sol = Arrays.stream(races)
        //    .mapToInt(Race::solveCount)
        //    .reduce(1, (a, b) -> a * b);
        var race = parseRace();
        var sol = race.solveCount();
        System.out.println(sol);
    }
}
