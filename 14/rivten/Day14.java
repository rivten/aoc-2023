import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day14 {

    record P(int x, int y) {}

    static int load(int maxY, Set<P> rocks) {
        return rocks.stream().mapToInt(rock -> maxY - rock.y).sum();
    }

    static Set<P> tiltNorth(Set<P> cubes, int maxX, int maxY, Set<P> rocks) {
        var rocksSorted = rocks.stream().sorted(new Comparator<P>() {
            @Override
            public int compare(P a, P b) {
                return a.y - b.y;
            }
        }).toList();
        var newRocks = new HashSet<P>();
        for (var rock: rocksSorted) {
            int hit = -1;
            for (int y = rock.y; y >= 0; --y) {
                var testP = new P(rock.x, y);
                if (cubes.contains(testP) || newRocks.contains(testP)) {
                    hit = y;
                    break;
                }
            }
            newRocks.add(new P(rock.x, hit + 1));
        }
        return newRocks;
    }

    static void display(Set<P> cubes, int maxX, int maxY, Set<P> rocks) {
        for (int y = 0; y < maxY; ++y) {
            for (int x = 0; x < maxX; ++x) {
                var p = new P(x, y);
                if (cubes.contains(p)) {
                    System.out.print('#');
                } else if (rocks.contains(p)) {
                    System.out.print('O');
                } else {
                    System.out.print('.');
                }
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var rocks = new HashSet<P>();
        var cubes = new HashSet<P>();
        var lines = br.lines().toList();
        int maxY = lines.size();
        int maxX = lines.get(maxY - 1).length();

        for (int y = 0; y < lines.size(); ++y) {
            var line = lines.get(y);
            for (int x = 0; x < line.length(); ++x) {
                char c = line.charAt(x);
                if (c == '.') {
                } else if (c == '#') {
                    cubes.add(new P(x, y));
                } else if (c == 'O') {
                    rocks.add(new P(x, y));
                } else {
                    assert false;
                }
            }
        }

        var newRocks = tiltNorth(cubes, maxX, maxY, rocks);

        //display(cubes, maxX, maxY, rocks);
        //System.out.println();
        //display(cubes, maxX, maxY, newRocks);

        System.out.println(load(maxY, newRocks));
    }
}
