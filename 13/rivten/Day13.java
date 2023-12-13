import java.io.*;
import java.util.*;
import java.util.stream.*;

class Day13 {

    private static int findReflectionIndex(List<String> block) {
        var storage = new HashMap<String, List<Integer>>();
        Integer reflectionStart = null;
        for (int y = 0; y < block.size(); ++y) {
            String line = block.get(y);

            if (reflectionStart != null) {
                if (2 * reflectionStart - 1 - y < 0) {
                    return reflectionStart;
                }
            }

            var reflections = storage.get(line);
            //System.out.println(storage + " " + line + " " + reflectionStart + " " + y + " " + (reflectionStart != null ? 2 * reflectionStart - 1 - y : ""));
            if (reflections == null) {
                reflectionStart = null;
                var ys = new ArrayList<Integer>();
                ys.add(y);
                storage.put(line, ys);
            } else {
                reflections.add(y);
                if (reflectionStart == null) {
                    if (reflections.contains(y - 1)) {
                        reflectionStart = y;
                    }
                } else if (!reflections.contains(2 * reflectionStart - 1 - y)) {
                    reflectionStart = null;
                }
            }
        }

        return reflectionStart == null ? 0 : reflectionStart;
    }

    private static long score(List<String> block) {
        // horizontal reflection
        var horizIndex = findReflectionIndex(block);

        // vertical reflection
        var transposedBlocks = new ArrayList<String>();
        for (int i = 0; i < block.get(0).length(); ++i) {
            transposedBlocks.add(new String());
        }
        for (int i = 0; i < block.get(0).length(); ++i) {
            for (int j = 0; j < block.size(); ++j) {
                var s = transposedBlocks.get(i);
                s += block.get(j).charAt(i);
                transposedBlocks.set(i, s);
            }
        }
        var vertIndex = findReflectionIndex(transposedBlocks);
        assert vertIndex == 0 || horizIndex == 0;
        assert vertIndex != 0 || horizIndex != 0;
        
        return 100 * horizIndex + vertIndex;
    }

    public static void main(String[] args) {
        var br = new BufferedReader(new InputStreamReader(System.in));

        var lines = br.lines().toList();
        var currentBlock = new ArrayList<String>();
        long sum = 0;
        for(String line: lines) {
            if (line.length() == 0) {
                sum += score(currentBlock);
                currentBlock = new ArrayList<String>();
            } else {
                currentBlock.add(line);
            }
        }
        sum += score(currentBlock);
        System.out.println(sum);
    }
}
