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

    static Set<P> tiltSouth(Set<P> cubes, int maxX, int maxY, Set<P> rocks) {
        var rocksSorted = rocks.stream().sorted(new Comparator<P>() {
            @Override
            public int compare(P a, P b) {
                return - a.y + b.y;
            }
        }).toList();
        var newRocks = new HashSet<P>();
        for (var rock: rocksSorted) {
            int hit = maxY;
            for (int y = rock.y; y < maxY; ++y) {
                var testP = new P(rock.x, y);
                if (cubes.contains(testP) || newRocks.contains(testP)) {
                    hit = y;
                    break;
                }
            }
            newRocks.add(new P(rock.x, hit - 1));
        }
        return newRocks;
    }

    static Set<P> tiltWest(Set<P> cubes, int maxX, int maxY, Set<P> rocks) {
        var rocksSorted = rocks.stream().sorted(new Comparator<P>() {
            @Override
            public int compare(P a, P b) {
                return a.x - b.x;
            }
        }).toList();
        var newRocks = new HashSet<P>();
        for (var rock: rocksSorted) {
            int hit = -1;
            for (int x = rock.x; x >= 0; --x) {
                var testP = new P(x, rock.y);
                if (cubes.contains(testP) || newRocks.contains(testP)) {
                    hit = x;
                    break;
                }
            }
            newRocks.add(new P(hit + 1, rock.y));
        }
        return newRocks;
    }

    static Set<P> tiltEast(Set<P> cubes, int maxX, int maxY, Set<P> rocks) {
        var rocksSorted = rocks.stream().sorted(new Comparator<P>() {
            @Override
            public int compare(P a, P b) {
                return - a.x + b.x;
            }
        }).toList();
        var newRocks = new HashSet<P>();
        for (var rock: rocksSorted) {
            int hit = maxX;
            for (int x = rock.x; x < maxX; ++x) {
                var testP = new P(x, rock.y);
                if (cubes.contains(testP) || newRocks.contains(testP)) {
                    hit = x;
                    break;
                }
            }
            newRocks.add(new P(hit - 1, rock.y));
        }
        return newRocks;
    }

    static Set<P> cycle(Set<P> cubes, int maxX, int maxY, Set<P> rocks) {
        var r = rocks;
        r = tiltNorth(cubes, maxX, maxY, r);
        r = tiltWest(cubes, maxX, maxY, r);
        r = tiltSouth(cubes, maxX, maxY, r);
        r = tiltEast(cubes, maxX, maxY, r);
        return r;
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

    static boolean setEqls(Set<P> as, Set<P> bs) {
        for (var a: as) {
            if (!bs.contains(a)) return false;
        }
        for (var b: bs) {
            if (!as.contains(b)) return false;
        }
        return true;
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

        List<Set<P>> rocksList = new ArrayList<Set<P>>();
        Set<P> r = rocks;
        var loads = new ArrayList<Integer>();
        for (int i = 0; i < 1000000000; ++i) {
            r = cycle(cubes, maxX, maxY, r);
            loads.add(load(maxY, r));
            for (int j = 0; j < i; ++j) {
                var testRocks = rocksList.get(j);
                if (setEqls(testRocks, r)) {
                    int cycleLen = i - j;
                    int rem = 1000000000 - i;
                    int cycleOffset = rem % cycleLen;
                    //System.out.println(i + " " + j + " " + cycleLen + " " + rem + " " + cycleOffset + " " + loads.get(j + cycleOffset - 1) + " " + loads);
                    System.out.println(loads.get(j + cycleOffset - 1)); // -1 was discovered empirically :P

                    System.exit(0);
                }
            }
            var newR = new HashSet<P>(r);
            rocksList.add(newR);

        }
        System.out.println(loads);

        display(cubes, maxX, maxY, r);

        System.out.println(load(maxY, r));
    }
}
