import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day15 {
    static long hash(String s) {
        long h = 0;
        for (int i = 0; i < s.length(); ++i) {
            char c = s.charAt(i);
            h += (long)c;
            h *= 17;
            h %= 256;
        }
        return h;
    }
    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var lines = br.lines().toList();
        long sum = 0;
        for (var s: lines.get(0).split(",")) {
            sum += hash(s);
        }
        System.out.println(sum);
    }
}
