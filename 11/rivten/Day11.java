import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day11 {
    private final record P(int x, int y) {}

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var lines = br.lines().toList();
        var planets = new ArrayList<P>();
        var emptyRows = new HashSet<Integer>();
        var emptyCols = new HashSet<Integer>();
        for (int y = 0; y < lines.size(); ++y) {
            boolean emptyLine = true;
            var line = lines.get(y);
            for (int x = 0; x < line.length(); ++x) {
                char c = line.charAt(x);
                if (c == '#') {
                    planets.add(new P(x, y));
                    emptyLine = false;
                }
            }
            if (emptyLine) {
                emptyRows.add(y);
            }
        }

        for (int x = 0; x < lines.get(0).length(); ++x) {
            boolean emptyCol = true;
            for (int y = 0; y < lines.size(); ++y) {
                char c = lines.get(y).charAt(x);
                if (c == '#') {
                    emptyCol = false;
                }
            }
            if (emptyCol) {
                emptyCols.add(x);
            }
        }

        int sol = 0;
        for (int i = 0; i < planets.size(); ++i) {
            var a = planets.get(i);
            for (int j = i + 1; j < planets.size(); ++j) {
                var b = planets.get(j);
                var d = Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
                for (int x = Math.min(a.x, b.x) + 1; x < Math.max(a.x, b.x); ++x) {
                    if (emptyCols.contains(x)) {
                        d++;
                    }
                }
                for (int y = Math.min(a.y, b.y) + 1; y < Math.max(a.y, b.y); ++y) {
                    if (emptyRows.contains(y)) {
                        d++;
                    }
                }
                sol += d;
            }
        }
        System.out.println(sol);
    }
}
