import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

class Day08 {

    private static class State {
        int instructionIndex; // always in [0, instructions.size()[
        String loc;
        final Program p;

        State(String loc, Program p) {
            this.instructionIndex = 0;
            this.loc = loc;
            this.p = p;
        }

        State(State other) {
            this.instructionIndex = other.instructionIndex;
            this.loc = other.loc;
            this.p = other.p;
        }

        void next() {
            loc = p.next(instructionIndex, loc);
            instructionIndex++;
            instructionIndex = instructionIndex % p.instructions.size();
        }

        boolean equals(State other) {
            return instructionIndex == other.instructionIndex &&
                loc.equals(other.loc);
        }
    }

    private final record Program(List<Integer> instructions, Map<String, String[]> map) {
        String next(long count, String loc) {
            int instruction = instructions.get((int)(count % instructions.size()));
            return map.get(loc)[instruction];
        }
    }

    private final record FloydResult(long mu, long lambda) {
        boolean isZ(long index) {
            return (((index - mu) % lambda) + mu) == lambda - 1;
        }
    }

    static long gcd(long a, long b) {
        if (a == 0 || b == 0) return a + b;
        if (a > b) return gcd(b, a);
        return gcd(b % a, a);
    }

    static long lcm(List<Long> l) {
        return l.stream().reduce(1l, (a, b) -> a * b / gcd(a, b));
    }

    private static FloydResult floyd(Program p, String loc) {
        // based on this https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare
        var tortoise = new State(loc, p);
        tortoise.next();
        var hare = new State(loc, p);
        hare.next();
        hare.next();
        while (!tortoise.equals(hare)) {
            tortoise.next();
            hare.next();
            hare.next();
        }

        long mu = 0;
        tortoise = new State(loc, p);
        while (!tortoise.equals(hare)) {
            tortoise.next();
            hare.next();
            mu++;
        }

        long lambda = 1;
        hare = new State(tortoise);
        hare.next();
        while (!tortoise.equals(hare)) {
            hare.next();
            lambda++;
        }
        return new FloydResult(mu, lambda);
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var lines = br.lines().toList();
        var instructions = lines.get(0).chars().mapToObj(i -> (Integer.valueOf(i) - 'L') / ('R' - 'L')).toList();

        var map = new HashMap<String, String[]>();

        var pattern = Pattern.compile("^(\\w{3}) = \\((\\w{3}), (\\w{3})\\)$");
        for (int i = 2; i < lines.size(); ++i) {
            var m = pattern.matcher(lines.get(i));
            if (m.find()) {
                map.put(m.group(1), new String[] {m.group(2), m.group(3)});
            }
        }

        final var program = new Program(instructions, map);

        long count = 0;
        List<String> currentLocs = map.keySet().stream().filter(s -> s.endsWith("A")).collect(Collectors.toList());
        var floydResults = currentLocs.stream().map(loc -> floyd(program, loc)).toList();

        // Just checking an assumption about the input
        // i.e that the index at which the Z happens is λ-1
        for (int i = 0; i < currentLocs.size(); ++i) {
            var state = new State(currentLocs.get(i), program);
            var floydResult = floydResults.get(i);
            for (int j = 0; j < floydResult.lambda + floydResult.mu; j++) {
                state.next();
                if (j >= floydResult.mu) {
                    if (state.loc.endsWith("Z")) {
                        // We assert that the point at which we reach a Z is the end of a cycle.
                        // This is not forced in any way, this is just a characterics of all the inputs
                        // we rely on.
                        assert j == floydResult.lambda - 1;
                    }
                }
            }
        }
        long lcm = lcm(floydResults.stream().map(FloydResult::lambda).toList());
        // just getting the lcm works because all Zs are in positons λ-1.
        // otherwise we would have needed to mess with the μ values as well
        System.out.println(lcm);
    }
}
