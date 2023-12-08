import java.io.*;
import java.util.*;
import java.util.regex.*;

class Day08 {
    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var lines = br.lines().toList();
        var instructions = lines.get(0).chars().mapToObj(i -> Integer.valueOf(i)).toList();

        var map = new HashMap<String, String[]>();

        var pattern = Pattern.compile("^(\\w{3}) = \\((\\w{3}), (\\w{3})\\)$");
        for (int i = 2; i < lines.size(); ++i) {
            var m = pattern.matcher(lines.get(i));
            if (m.find()) {
                map.put(m.group(1), new String[] {m.group(2), m.group(3)});
            }
        }

        int count = 0;
        String currentLoc = "AAA";
        while (true) {
            int instruction = instructions.get(count % instructions.size());
            instruction = (instruction - 'L') / ('R' - 'L');
            currentLoc = map.get(currentLoc)[instruction];
            count++;
            if (currentLoc.equals("ZZZ")) break;
        }
        System.out.println(count);
    }
}
