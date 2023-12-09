import java.io.*;
import java.util.*;

class Day09 {
    static int getExtrapolatedValue(List<Integer> history) {
        if (history.stream().allMatch(v -> v == 0)) {
            return 0;
        }
        var derivative = new ArrayList<Integer>();
        var last = history.get(0);
        for (int i = 1; i < history.size(); ++i) {
            var n = history.get(i);
            derivative.add(n - last);
            last = n;
        }
        return last + getExtrapolatedValue(derivative);
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var sol = br.lines()
            .map(line -> Arrays.stream(line.split(" ")).map(Integer::parseInt).toList())
            .mapToInt(Day09::getExtrapolatedValue)
            .sum();
        System.out.println(sol);
    }
}
