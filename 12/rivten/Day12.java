import java.util.*;
import java.util.stream.*;
import java.io.*;

class Day12 {
    private static boolean match(List<Character> springs, List<Integer> groups) {
        int currentGroupIndex = 0;
        int currentGroupSize = 0;
        for (char c: springs) {
            switch (c) {
                case '.': {
                    if (currentGroupSize > 0) {
                        if (currentGroupIndex >= groups.size()) {
                            return false;
                        }
                        if (groups.get(currentGroupIndex) != currentGroupSize) {
                            return false;
                        }
                        currentGroupSize = 0;
                        currentGroupIndex++;
                    }
                } break;
                case '#': {
                    currentGroupSize++;
                } break;
                default: 
                    assert false;
            }
        }
        if (currentGroupSize > 0) {
            if (currentGroupIndex >= groups.size()) {
                return false;
            }
            if (groups.get(currentGroupIndex) != currentGroupSize) {
                return false;
            }
            currentGroupSize = 0;
            currentGroupIndex++;
        }
        if (currentGroupIndex != groups.size()) {
            return false;
        }
        return true;
    }

    private static long arrangements(List<Character> springs, List<Integer> groups, int index) {
        if (index == springs.size()) {
            if (match(springs, groups)) {
                return 1;
            } else {
                return 0;
            }
        } else {
            if (springs.get(index) == '?') {
                var copySpringsHash = new ArrayList<Character>(springs);
                copySpringsHash.set(index, '#');
                var arrangementsHash = arrangements(copySpringsHash, groups, index + 1);

                var copySpringsDot = new ArrayList<Character>(springs);
                copySpringsDot.set(index, '.');
                var arrangementsDot = arrangements(copySpringsDot, groups, index + 1);

                return arrangementsHash + arrangementsDot;
            } else {
                return arrangements(springs, groups, index + 1);
            }
        }
    }

    private static long countArrangements(String line) {
        var s = line.split(" ");
        var springs = s[0].chars().mapToObj(e -> (char)e).collect(Collectors.toList());
        var groups = Arrays.stream(s[1].split(",")).map(e -> Integer.parseInt(e)).collect(Collectors.toList());
        var arrangements = arrangements(springs, groups, 0);
        return arrangements;
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        long sol = br.lines().mapToLong(Day12::countArrangements).sum();
        System.out.println(sol);
    }
}
