import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day15 {
    static int hash(String s) {
        int h = 0;
        for (int i = 0; i < s.length(); ++i) {
            char c = s.charAt(i);
            h += (int)c;
            h *= 17;
            h %= 256;
        }
        return h;
    }

    record Lens(String label, int focal) {}

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));
        var lines = br.lines().toList();
        var boxes = new ArrayList<LinkedList<Lens>>();
        for (int i = 0; i < 256; ++i) {
            boxes.add(new LinkedList<Lens>());
        }

        for (var s: lines.get(0).split(",")) {
            //System.out.println(s);
            if (s.charAt(s.length() - 1) == '-') {
                var label = s.substring(0, s.length() - 1);
                int h = hash(label);
                var box = boxes.get(h);
                for (int i = 0; i < box.size(); ++i) {
                    if (box.get(i).label.equals(label)) {
                        box.remove(i);
                        break;
                    }
                }
            } else {
                var spl = s.split("=");
                var label = spl[0];
                int focal = Integer.parseInt(spl[1]);
                int h = hash(label);
                var box = boxes.get(h);
                Integer found = null;
                for (int i = 0; i < box.size(); ++i) {
                    if (box.get(i).label.equals(label)) {
                        found = i;
                        break;
                    }
                }
                //System.out.println(found);
                if (found == null) {
                    box.add(new Lens(label, focal));
                } else {
                    box.set(found, new Lens(label, focal));
                }
            }
            //System.out.println(boxes);
        }

        long sum = 0;
        for (int i = 0; i < 256; ++i) {
            var box = boxes.get(i);
            for (int j = 0; j < box.size(); ++j) {
                int focal = box.get(j).focal;
                sum += (i + 1) * (j + 1) * focal;
            }
        }
        System.out.println(sum);
    }
}
