import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;
import java.util.List;
import java.util.ArrayList;

class Day05 {

    private record Range(long src, long len, long dst) {}

    private record Mapping(List<Range> ranges) {
        private long map(long in) {
            for (var range: ranges) {
                if (in >= range.src && in < (range.src + range.len)) {
                    return (in - range.src) + range.dst;
                }
            }
            return in;
        }
    }

    private record Almanac(List<Long> seeds, Mapping[] mappings) {
        private long getLoc(long seed) {
            var currentIndex = seed;
            for (var mapping: mappings) {
                currentIndex = mapping.map(currentIndex);
            }
            return currentIndex;
        }
    }

    private static Almanac parse(String content) {
        var mappings = new Mapping[7];
        var seeds = new ArrayList<Long>();
        var paragraphIndex = 0;
        for (var paragraph: content.split("\n\n")) {
            if (paragraphIndex == 0) {
                var seedsRaw = paragraph.split(":")[1];
                for (var seedRaw: seedsRaw.trim().split(" ")) {
                    seeds.add(Long.parseLong(seedRaw));
                }
            } else {
                var mappingIndex = paragraphIndex - 1;
                var rawLines = paragraph.split("\n");
                var ranges = new ArrayList<Range>();
                for (int i = 1; i < rawLines.length; ++i) {
                    // starting at one to skip the first line
                    var rawLine = rawLines[i];
                    var rawInts = rawLine.split(" ");
                    var range = new Range(
                        Long.parseLong(rawInts[1]),
                        Long.parseLong(rawInts[2]),
                        Long.parseLong(rawInts[0])
                    );
                    ranges.add(range);
                }
                mappings[mappingIndex] = new Mapping(ranges);
            }
            paragraphIndex++;
        }
        return new Almanac(seeds, mappings);
    }

    public static void main(String[] args) {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        var content = bi.lines()
            .collect(Collectors.joining("\n"));

        var almanac = parse(content);
        var sol = almanac.seeds.stream()
            .mapToLong(almanac::getLoc)
            .min()
            .getAsLong();
        System.out.println(sol);
    }
}
