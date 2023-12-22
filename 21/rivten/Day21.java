import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day21 {
    record P(int x, int y) {}

    private static Set<P> step(Set<P> rocks, Set<P> ps) {
        var res = new HashSet<P>();
        for (var p: ps) {
            var up = new P(p.x, p.y - 1);
            var down = new P(p.x, p.y + 1);
            var left = new P(p.x - 1, p.y);
            var right = new P(p.x + 1, p.y);

            if (!rocks.contains(up)) {
                res.add(up);
            }
            if (!rocks.contains(down)) { 
                res.add(down);
            }
            if (!rocks.contains(left)) { 
                res.add(left);
            }
            if (!rocks.contains(right)) { 
                res.add(right);
            }
        }
        return res;
    }

    private static void trace(Set<P> rocks, P start, Set<P> ps, int maxX, int maxY) {
        for (int y = 0; y < maxY; ++y) {
            for (int x = 0; x < maxX; ++x) {
                var p = new P(x, y);
                
                if (rocks.contains(p)) {
                    System.out.print('#');
                } else if (ps.contains(p)) {
                    System.out.print('O');
                } else if (start.x == x && start.y == y) {
                    System.out.print('S');
                } else {
                    System.out.print('.');
                }
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var lines = br.lines().toList();
        int maxY = lines.size();
        int maxX = lines.get(0).length();
        var rocks = new HashSet<P>();
        P start = null;
        
        for (int y = 0; y < maxY; ++y) {
            var line = lines.get(y);
            for (int x = 0; x < maxX; ++x) {
                char c = line.charAt(x);
                if (c == '.') {
                } else if (c == '#') {
                    rocks.add(new P(x, y));
                } else if (c == 'S') {
                    start = new P(x, y);
                } else {
                    assert false;
                }
            }
        }

        Set<P> ps = new HashSet<P>();
        ps.add(start);
        for (int i = 0; i < 64; ++i) {
            ps = step(rocks, ps);
            //System.out.println("========================");
            //trace(rocks, start, ps, maxX, maxY);
        }
        System.out.println(ps.size());
    }
}
