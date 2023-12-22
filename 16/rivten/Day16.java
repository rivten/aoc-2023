import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day16 {
    enum Dir {
        LEFT,
        RIGHT,
        UP,
        DOWN,
    }

    record P(int x, int y) {
        private boolean inBounds(int maxX, int maxY) {
            return x >= 0 && y >= 0 && x < maxX && y < maxY;
        }
    }

    record Beam(P p, Dir dir) {}

    private static void trace(Set<Beam> been, int maxX, int maxY) {
        for (int y = 0; y < maxY; ++y) {
            for (int x = 0; x < maxX; ++x) {
                var p = new P(x, y);
                if (been.stream().map(beam -> beam.p).filter(bp -> bp.x == p.x && bp.y == p.y).count() == 0) {
                    System.out.print('.');
                } else {
                    System.out.print('#');
                }
            }
            System.out.println();
        }
    }

    private static List<Beam> simBeams(Map<P, Character> map, int maxX, int maxY, List<Beam> beams) {
        var next = new ArrayList<Beam>();
        for (int i = 0; i < beams.size(); ++i) {
            var beam = beams.get(i);
            char c = map.getOrDefault(beam.p, '.');
            switch (beam.dir) {
                case Dir.LEFT: {
                    switch (c) {
                        case '.': case '-': {
                            var p = new P(beam.p.x - 1, beam.p.y);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, beam.dir));
                            }
                        } break;
                        case '\\': {
                            var p = new P(beam.p.x, beam.p.y - 1);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.UP));
                            }
                        } break;
                        case '|': {
                            var p0 = new P(beam.p.x, beam.p.y - 1);
                            var p1 = new P(beam.p.x, beam.p.y + 1);
                            if (p0.inBounds(maxX, maxY)) {
                                var beam0 = new Beam(p0, Dir.UP);
                                next.add(beam0);
                            }
                            if (p1.inBounds(maxX, maxY)) {
                                var beam1 = new Beam(p1, Dir.DOWN);
                                next.add(beam1);
                            }
                        } break;
                        case '/': {
                            var p = new P(beam.p.x, beam.p.y + 1);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.DOWN));
                            }
                        } break;
                        default: {
                            assert false;
                        } break;
                    }
                } break;
                case Dir.RIGHT: {
                    switch (c) {
                        case '.': case '-': {
                            var p = new P(beam.p.x + 1, beam.p.y);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, beam.dir));
                            }
                        } break;
                        case '\\': {
                            var p = new P(beam.p.x, beam.p.y + 1);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.DOWN));
                            }
                        } break;
                        case '|': {
                            var p0 = new P(beam.p.x, beam.p.y - 1);
                            var p1 = new P(beam.p.x, beam.p.y + 1);
                            if (p0.inBounds(maxX, maxY)) {
                                var beam0 = new Beam(p0, Dir.UP);
                                next.add(beam0);
                            }
                            if (p1.inBounds(maxX, maxY)) {
                                var beam1 = new Beam(p1, Dir.DOWN);
                                next.add(beam1);
                            }
                        } break;
                        case '/': {
                            var p = new P(beam.p.x, beam.p.y - 1);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.UP));
                            }
                        } break;
                        default: {
                            assert false;
                        } break;
                    }
                } break;
                case Dir.UP: {
                    switch (c) {
                        case '.': case '|': {
                            var p = new P(beam.p.x, beam.p.y - 1);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, beam.dir));
                            }
                        } break;
                        case '\\': {
                            var p = new P(beam.p.x - 1, beam.p.y);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.LEFT));
                            }
                        } break;
                        case '/': {
                            var p = new P(beam.p.x + 1, beam.p.y);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.RIGHT));
                            }
                        } break;
                        case '-': {
                            var p0 = new P(beam.p.x - 1, beam.p.y);
                            var p1 = new P(beam.p.x + 1, beam.p.y);
                            if (p0.inBounds(maxX, maxY)) {
                                var beam0 = new Beam(p0, Dir.LEFT);
                                next.add(beam0);
                            }
                            if (p1.inBounds(maxX, maxY)) {
                                var beam1 = new Beam(p1, Dir.RIGHT);
                                next.add(beam1);
                            }
                        } break;
                        default: {
                            assert false;
                        } break;
                    }
                } break;
                case Dir.DOWN: {
                    switch (c) {
                        case '.': case '|': {
                            var p = new P(beam.p.x, beam.p.y + 1);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, beam.dir));
                            }
                        } break;
                        case '\\': {
                            var p = new P(beam.p.x + 1, beam.p.y);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.RIGHT));
                            }
                        } break;
                        case '/': {
                            var p = new P(beam.p.x - 1, beam.p.y);
                            if (p.inBounds(maxX, maxY)) {
                                next.add(new Beam(p, Dir.LEFT));
                            }
                        } break;
                        case '-': {
                            var p0 = new P(beam.p.x - 1, beam.p.y);
                            var p1 = new P(beam.p.x + 1, beam.p.y);
                            if (p0.inBounds(maxX, maxY)) {
                                var beam0 = new Beam(p0, Dir.LEFT);
                                next.add(beam0);
                            }
                            if (p1.inBounds(maxX, maxY)) {
                                var beam1 = new Beam(p1, Dir.RIGHT);
                                next.add(beam1);
                            }
                        } break;
                        default: {
                            assert false;
                        } break;
                    }
                } break;
                default: {
                    assert false;
                } break;
            }
        }
        return next;
    }

    private static int energize(Map<P, Character> map, int maxX, int maxY, Beam startBeam) {
        var been = new HashSet<Beam>();
        List<Beam> beams = new ArrayList<Beam>();
        beams.add(startBeam);
        been.add(startBeam);
        while (beams.size() != 0) {
            beams = simBeams(map, maxX, maxY, beams);
            for (int i = 0; i < beams.size(); ++i) {
                var beam = beams.get(i);
                if (been.contains(beam)) {
                    beams.remove(i);
                    i--;
                } else {
                    been.add(beam);
                }
            }
        }

        var ps = new HashSet<P>();
        for (var b: been) {
            ps.add(b.p);
        }
        return ps.size();
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var lines = br.lines().toList();
        var map = new HashMap<P, Character>();
        int maxY = lines.size();
        int maxX = lines.get(0).length();
        for (int y = 0; y < maxY; ++y) {
            var line = lines.get(y);
            for (int x = 0; x < maxX; ++x) {
                char c = line.charAt(x);
                if (c != '.') {
                    map.put(new P(x, y), c);
                }
            }
        }

        int maxEnergize = 0;
        for (int x = 0; x < maxX; ++x) {
            int e = 0;
            var startBeamTop = new Beam(new P(x, 0), Dir.DOWN);
            e = energize(map, maxX, maxY, startBeamTop);
            maxEnergize = Math.max(maxEnergize, e);
            var startBeamBottom = new Beam(new P(x, maxY - 1), Dir.UP);
            e = energize(map, maxX, maxY, startBeamBottom);
            maxEnergize = Math.max(maxEnergize, e);
        }
        for (int y = 0; y < maxY; ++y) {
            int e = 0;
            var startBeamLeft = new Beam(new P(0, y), Dir.RIGHT);
            e = energize(map, maxX, maxY, startBeamLeft);
            maxEnergize = Math.max(maxEnergize, e);
            var startBeamRight = new Beam(new P(maxX - 1, y), Dir.LEFT);
            e = energize(map, maxX, maxY, startBeamRight);
            maxEnergize = Math.max(maxEnergize, e);
        }
        System.out.println(maxEnergize);
    }
}
