import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day10 {
    private record P(int x, int y) {}

    private static void addEdge(Map<P, Set<P>> graph, P a, P b) {
        var adjA = graph.getOrDefault(a, new HashSet<P>());
        adjA.add(b);
        graph.put(a, adjA);
    }

    private record Step(P p, int d) {}

    private static boolean isVert(List<String> lines, P p) {
        char c = lines.get(p.y).charAt(p.x);
        // we could, or maybe not, add S, depending on whether it represent a L or J or | in the given example.
        // this needs to be added or removed on a case-by-case basis based on the example.
        return c == '|' || c == 'L' ||  c == 'J' || c == 'S';
    }

    private static boolean isPointInGraph(List<String> lines, P p, Set<P> loop) {
        int crossed = 0;
        for (int x = p.x; x >= 0; --x) {
            var newP = new P(x, p.y);
            if (loop.contains(newP) && isVert(lines, newP)) {
                crossed++;
            }
        }
        return crossed % 2 == 1;
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var graph = new HashMap<P, Set<P>>();
        P start = null;
        var lines = br.lines().toList();
        for (int y = 0; y < lines.size(); ++y) {
            var line = lines.get(y);
            for (int x = 0; x < line.length(); ++x) {
                char c = line.charAt(x);
                switch (c) {
                    case '.': {
                    } break;
                    case 'S': {
                        start = new P(x, y);
                        // the edges will be added by the other points

                        //// in theory, we should only add edges if there is no points
                        var left = line.charAt(x - 1);
                        if (left == '-' || left == 'L' || left == 'F') {
                            addEdge(graph, start, new P(x - 1, y));
                        }
                        var right = line.charAt(x + 1);
                        if (right == '-' || right == 'J' || right == '7') {
                            addEdge(graph, start, new P(x + 1, y));
                        }
                        var top = lines.get(y - 1).charAt(x);
                        if (top == '|' || top == 'F' || top == '7') {
                            addEdge(graph, start, new P(x, y - 1));
                        }
                        var down = lines.get(y + 1).charAt(x);
                        if (down == '|' || down == 'L' || top == 'J') {
                            addEdge(graph, start, new P(x, y + 1));
                        }
                    } break;
                    case '-': {
                        var here = new P(x, y);
                        var left = new P(x - 1, y);
                        var right = new P(x + 1, y);
                        addEdge(graph, here, left);
                        addEdge(graph, here, right);
                    } break;
                    case '7': {
                        var here = new P(x, y);
                        var left = new P(x - 1, y);
                        var down = new P(x, y + 1);
                        addEdge(graph, here, left);
                        addEdge(graph, here, down);
                    } break;
                    case '|': {
                        var here = new P(x, y);
                        var top = new P(x, y - 1);
                        var down = new P(x, y + 1);
                        addEdge(graph, here, top);
                        addEdge(graph, here, down);
                    } break;
                    case 'L': {
                        var here = new P(x, y);
                        var top = new P(x, y - 1);
                        var right = new P(x + 1, y);
                        addEdge(graph, here, top);
                        addEdge(graph, here, right);
                    } break;
                    case 'J': {
                        var here = new P(x, y);
                        var top = new P(x, y - 1);
                        var left = new P(x - 1, y);
                        addEdge(graph, here, top);
                        addEdge(graph, here, left);
                    } break;
                    case 'F': {
                        var here = new P(x, y);
                        var down = new P(x, y + 1);
                        var right = new P(x + 1, y);
                        addEdge(graph, here, down);
                        addEdge(graph, here, right);
                    } break;
                    default: {
                         System.out.println(c); 
                         assert false;
                    } break;
                };
            }
        }

        //var previous = start;
        //var current = graph.get(start).toArray(new P[graph.get(start).size()])[0]; // we just hope it's 0, otherwise test another number. yes, it's ugly
        //int steps = 1;
        //while (current.x != start.x || current.y != start.y) {
        //    P next = null;
        //    for (var p: graph.get(current)) {
        //        if (!(p.x == previous.x && p.y == previous.y)) {
        //            next = p;
        //            break;
        //        }
        //    }
        //    assert next != null;
        //    previous = current;
        //    current = next;
        //    steps++;
        //}
        //System.out.println(steps / 2);


        // performing BFS
        var queue = new LinkedList<Step>();
        var seen = new HashSet<P>();
        int maxDist = 0;
        queue.add(new Step(start, 0));
        while (queue.peek() != null) {
            var step = queue.remove();
            //System.out.println(step);

            if (seen.contains(step.p)) continue;

            seen.add(step.p);
            if (step.d > maxDist) {
                maxDist = step.d;
            }
            for (var adjP: graph.get(step.p)) {
                if (!seen.contains(adjP)) {
                    queue.add(new Step(adjP, step.d + 1));
                }
            }
        }

        //for (int y = 0; y < lines.size(); ++y) {
        //    var line = lines.get(y);
        //    for (int x = 0; x < line.length(); ++x) {
        //        if (seen.contains(new P(x, y))) {
        //            System.out.print("x");
        //        } else {
        //            if (isPointInGraph(lines, new P(x, y), seen)) {
        //                System.out.print("I");
        //            } else {
        //                System.out.print("O");
        //            }
        //        }
        //    }
        //    System.out.println();
        //}

        int count = 0;
        for (int y = 0; y < lines.size(); ++y) {
            var line = lines.get(y);
            for (int x = 0; x < line.length(); ++x) {
                var p = new P(x, y);
                if (!seen.contains(p)) {
                    if (isPointInGraph(lines, p, seen)) {
                        count++;
                    }
                }
            }
        }
        System.out.println(count);
    }
}
