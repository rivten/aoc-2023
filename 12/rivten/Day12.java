import java.util.*;
import java.util.stream.*;
import java.io.*;

class Day12 {

    record S(List<Character> springs, List<Integer> groups, boolean inGroup) {}

    static HashMap<S, Long> memo = new HashMap<S, Long>();

    private static long arrangements(List<Character> springs, List<Integer> groups, boolean inGroup) {
        var s = new S(springs, groups, inGroup);
        //System.out.println("TESING " + s);
        var r = memo.get(s);
        if (r == null) {
            if (springs.size() == 0) {
                if (groups.size() == 0 || (groups.size() == 1 && groups.get(0) == 0)) {
                    memo.put(s, 1l);
                    return 1;
                } else {
                    memo.put(s, 0l);
                    return 0;
                }
            }
            if (groups.size() == 0) {
                for (char c: springs) {
                    if (c == '#') {
                        memo.put(s, 0l);
                        return 0;
                    }
                }
                memo.put(s, 1l);
                return 1;
            }

            char c = springs.get(0);
            if (c == '.') {
                var groupsCpy = new ArrayList<Integer>(groups);
                if (inGroup) {
                    if (groups.get(0) == 0) {
                        // we have finished a group
                        groupsCpy.remove(0);
                    } else {
                        memo.put(s, 0l);
                        return 0;
                    }
                }
                var springsCpy = new ArrayList<Character>(springs);
                springsCpy.remove(0);
                var a = arrangements(springsCpy, groupsCpy, false); 
                memo.put(s, a);
                return a;
            } else if (c == '#') {
                var springsCpy = new ArrayList<Character>(springs);
                springsCpy.remove(0);
                var groupsCpy = new ArrayList<Integer>(groups);
                groupsCpy.set(0, groupsCpy.get(0) - 1);
                if (groupsCpy.get(0) < 0) {
                    // impossible solution
                    memo.put(s, 0l);
                    return 0;
                } else {
                    var a = arrangements(springsCpy, groupsCpy, true);
                    memo.put(s, a);
                    return a;
                }
            } else if (c == '?') {
                var springsCpy = new ArrayList<Character>(springs);
                springsCpy.remove(0);
                var groupsCpy = new ArrayList<Integer>(groups);

                if (groupsCpy.get(0) == 0) {
                    assert inGroup;
                    // we need to put a dot
                    groupsCpy.remove(0);
                    var a = arrangements(springsCpy, groupsCpy, false); 
                    memo.put(s, a);
                    return a;
                } else {
                    if (inGroup) {
                        // we need to put a hash
                        groupsCpy.set(0, groupsCpy.get(0) - 1);
                        var a = arrangements(springsCpy, groupsCpy, true); 
                        memo.put(s, a);
                        return a;
                    } else {
                        // we can either put a dot or a hash
                        var groupsCpyDot = new ArrayList<Integer>(groups);
                        var groupsCpyHash = new ArrayList<Integer>(groups);
                        groupsCpyHash.set(0, groupsCpyHash.get(0) - 1);
                        var a = arrangements(springsCpy, groupsCpyDot, false) + arrangements(springsCpy, groupsCpyHash, true);
                        memo.put(s, a);
                        return a;
                    }
                }

            } else {
                assert false;
                return 0;
            }
        } else {
            return r;
        }
    }

    private static long countArrangements(String line) {
        var s = line.split(" ");
        var springs = s[0].chars().mapToObj(e -> (char)e).collect(Collectors.toList());
        var groups = Arrays.stream(s[1].split(",")).map(e -> Integer.parseInt(e)).collect(Collectors.toList());
        var bigSprings = new ArrayList<Character>();
        var bigGroups = new ArrayList<Integer>();
        for (int i = 0; i < 5; ++i) {
            bigSprings.addAll(springs);
            if (i != 4) {
                bigSprings.add('?');
            }
            bigGroups.addAll(groups);
        }

        var arrangements = arrangements(bigSprings, bigGroups, false);

        return arrangements;
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        long sol = br.lines().mapToLong(Day12::countArrangements).sum();
        System.out.println(sol);
    }
}
