import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;
import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;
import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;
import java.util.ArrayList;

class Day03 {

    private record P(int line, int col) {
        private Set<P> around() {
            var s = new HashSet<>(Arrays.asList(
                new P(line - 1, col - 1),
                new P(line - 1, col),
                new P(line - 1, col + 1),
                new P(line, col - 1),
                new P(line, col + 1),
                new P(line + 1, col - 1),
                new P(line + 1, col),
                new P(line + 1, col + 1)
            ));
            return s;
        }
    }

    private interface EngineContent {}

    private record Symbol(char c) implements EngineContent {
        private int gearValue(P p, Map<P, EngineContent> engine) {
            var prox = new ArrayList<Number>();
            for (var entry: engine.entrySet()) {
                if (entry.getValue() instanceof Number) {
                    var n = (Number)entry.getValue();
                    if (n.isPointInContact(entry.getKey(), p)) {
                        prox.add(n);
                    }
                }
            }
            if (prox.size() == 2) {
                return prox.get(0).value * prox.get(1).value;
            } else {
                return 0;
            }
        }
    }

    private record Number(int value, int len) implements EngineContent {
        private boolean isPart(P p, Map<P, EngineContent> engine) {
            for (int charIndex = 0; charIndex < len; ++charIndex) {
                for (var testP : new P(p.line, p.col + charIndex).around()) {
                    var maybeContent = engine.get(testP);
                    if (maybeContent != null && maybeContent instanceof Symbol) {
                        return true;
                    }
                }
            }
            return false;
        }

        private boolean isPointInContact(P p, P otherP) {
            for (int charIndex = 0; charIndex < len; ++charIndex) {
                for (var testP : new P(p.line, p.col + charIndex).around()) {
                    if (testP.line == otherP.line && testP.col == otherP.col) {
                        return true;
                    }
                }
            }
            return false;
        }
    }

    private static Map<P, EngineContent> parse() {
        var content = new BufferedReader(new InputStreamReader(System.in)).lines().toList();
        var engine = new HashMap<P, EngineContent>();
        int numberValue = 0;
        int numberLen = 0;
        boolean parsingNumber = false;
        for (int lineIndex = 0; lineIndex < content.size(); ++lineIndex) {
            var line = content.get(lineIndex);
            for (int colIndex = 0; colIndex < line.length(); ++colIndex) {
                char c = line.charAt(colIndex);
                if (c == '.') {
                    if (parsingNumber) {
                        parsingNumber = false;
                        engine.put(new P(lineIndex, colIndex - numberLen), new Number(numberValue, numberLen));
                    }
                    continue;
                } else if (c >= '0' && c <= '9') {
                    if (parsingNumber) {
                        numberValue *= 10;
                        numberValue += c - '0';
                        numberLen++;
                    } else {
                        parsingNumber = true;
                        numberValue = c - '0';
                        numberLen = 1;
                    }
                } else {
                    if (parsingNumber) {
                        parsingNumber = false;
                        engine.put(new P(lineIndex, colIndex - numberLen), new Number(numberValue, numberLen));
                    }
                    engine.put(new P(lineIndex, colIndex), new Symbol(c));
                }
            }
            if (parsingNumber) {
                parsingNumber = false;
                engine.put(new P(lineIndex, line.length() - numberLen), new Number(numberValue, numberLen));
            }
        }

        return engine;
    }

    public static void main(String[] args) {
        var engine = parse();
        int sum = 0;
        for (var entry: engine.entrySet()) {
            // PART 1
            //if (entry.getValue() instanceof Number) {
            //    var n = (Number)entry.getValue();
            //    if (n.isPart(entry.getKey(), engine)) {
            //        sum += n.value();
            //    } else {
            //        System.out.println(entry);
            //    }
            //}

            // PART 2
            if (entry.getValue() instanceof Symbol && ((Symbol)entry.getValue()).c == '*') {
                var gearValue = ((Symbol)entry.getValue()).gearValue(entry.getKey(), engine);
                sum += gearValue;
            }
        }
        System.out.println(sum);
    }
}
