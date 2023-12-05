import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;
import java.util.List;
import java.util.ArrayList;
import java.util.Optional;
import java.util.stream.LongStream;
import java.util.stream.Stream;

class Day05 {

    // end is non-inclusive
    private record Interval(long start, long end) {
        private boolean isIn(long in) {
            return in >= start && in < end;
        }

        private Interval intersection(Interval other) {
            if (this.start > other.start) {
                return other.intersection(this);
            }

            if (this.end < other.start) {
                // empty intersection
                return new Interval(0, 0);
            } else if (this.end < other.end) {
                return new Interval(other.start, this.end);
            } else {
                return other;
            }
        }

        private boolean empty() {
            return start == end;
        }

        private List<Interval> sub(Interval other) {
            var result = new ArrayList<Interval>();
            var intersection = this.intersection(other);
            if (intersection.empty()) {
                result.add(this);
            } else {
                //if (this.start == 46 && other.start == 56) {
                //    System.out.println(this);
                //    System.out.println(other);
                //    System.out.println(intersection);
                //}
                if (intersection.start == this.start) {
                    if (intersection.end < this.end) {
                        result.add(new Interval(intersection.end, this.end));
                    } else {
                        // substract all, do nothing
                    }
                } else { // intersection.start > this.start
                    if (intersection.end < this.end) {
                        result.add(new Interval(this.start, intersection.start));
                        result.add(new Interval(intersection.end, this.end));
                    } else {
                        result.add(new Interval(this.start, intersection.start));
                    }
                }
            }
            return result;
        }
    }

    private record Range(Interval interval, long dst) {
        private Optional<Long> map(long in) {
            if (interval.isIn(in)) {
                return Optional.of(in - interval.start + dst);
            } else {
                return Optional.empty();
            }
        }
    }

    private record Mapping(List<Range> ranges) {
        private List<Interval> map(Interval interval) {
            //if (interval.start == 46 && this.ranges.get(0).interval.start == 56) {
            //    System.out.println(">>>");
            //    System.out.println(this);
            //    System.out.println(interval);
            //}
            var intervals = new ArrayList<Interval>();

            var remainingParts = new ArrayList<Interval>();
            remainingParts.add(interval);

            for (var range: ranges) {
                //if (interval.start == 46 && this.ranges.get(0).interval.start == 56) {
                //    System.out.println("$$");
                //    System.out.println(ranges);
                //}
                var intersection = interval.intersection(range.interval);
                if (!intersection.empty()) {
                    //if (interval.start == 46 && this.ranges.get(0).interval.start == 56) {
                    //    System.out.println("found intersection");
                    //    System.out.println(intersection);
                    //    System.out.println(interval);
                    //    System.out.println(range.interval);
                    //}
                    intervals.add(new Interval(
                        intersection.start - range.interval.start + range.dst,
                        intersection.end - range.interval.start + range.dst
                    ));
                    var nextRemainingParts = new ArrayList<Interval>();
                    for (var remainingPart: remainingParts) {
                        var substraction = remainingPart.sub(range.interval);
                        //if (interval.start == 46 && this.ranges.get(0).interval.start == 56) {
                        //    System.out.println("bb");
                        //    System.out.println(remainingPart);
                        //    System.out.println(range.interval);
                        //    System.out.println(substraction);
                        //}
                        for (var s: substraction) {
                            nextRemainingParts.add(s);
                        }
                    }
                    remainingParts = nextRemainingParts;
                    //if (interval.start == 46 && this.ranges.get(0).interval.start == 56) {
                    //    System.out.println("aa");
                    //    System.out.println(remainingParts);
                    //}
                }
            }

            // add all non-mapped parts of the initial interval
            for (var remainingPart: remainingParts) {
                intervals.add(remainingPart);
            }

            return intervals;
        }

        private long map(long in) {
            for (var range: ranges) {
                var maybeOut = range.map(in);
                if (maybeOut.isPresent()) {
                    return maybeOut.get();
                }
            }
            return in;
        }
    }

    private record Almanac(List<Interval> seeds, Mapping[] mappings) {
        private long getLoc(long seed) {
            var currentIndex = seed;
            for (var mapping: mappings) {
                currentIndex = mapping.map(currentIndex);
            }
            return currentIndex;
        }

        private long getSmallestLoc(Interval seed) {
            //System.out.println(">>");
            //System.out.println(seed);
            var currentIntervals = new ArrayList<Interval>();
            currentIntervals.add(seed);
            for (var mapping: mappings) {
                //System.out.println(">>>$");
                //System.out.println(mapping);
                //System.out.println(currentIntervals);
                var nextIntervals = new ArrayList<Interval>();
                for (var interval: currentIntervals) {
                    for (var i: mapping.map(interval)) {
                        nextIntervals.add(i);
                    }
                }
                //System.out.println(nextIntervals);
                currentIntervals = nextIntervals;
            }
            //System.out.println("$$");
            //System.out.println(currentIntervals);
            return currentIntervals.stream()
                .mapToLong(Interval::start)
                .min()
                .getAsLong();
        }
    }

    private static Almanac parse(String content) {
        var mappings = new Mapping[7];
        var seeds = new ArrayList<Interval>();
        var paragraphIndex = 0;
        for (var paragraph: content.split("\n\n")) {
            if (paragraphIndex == 0) {
                long lastSeedSrc = 0;
                var seedNumberIndex = 0;
                var seedsRaw = paragraph.split(":")[1];
                for (var seedRaw: seedsRaw.trim().split(" ")) {
                    if (seedNumberIndex % 2 == 0) {
                        lastSeedSrc = Long.parseLong(seedRaw);
                    } else {
                        var seedLen = Long.parseLong(seedRaw);
                        seeds.add(new Interval(lastSeedSrc, lastSeedSrc + seedLen));
                    }
                    seedNumberIndex++;
                }
            } else {
                var mappingIndex = paragraphIndex - 1;
                var rawLines = paragraph.split("\n");
                var ranges = new ArrayList<Range>();
                for (int i = 1; i < rawLines.length; ++i) {
                    // starting at one to skip the first line
                    var rawLine = rawLines[i];
                    var rawInts = rawLine.split(" ");
                    var src = Long.parseLong(rawInts[1]);
                    var len = Long.parseLong(rawInts[2]);
                    var range = new Range(
                        new Interval(src, src + len),
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
            .mapToLong(almanac::getSmallestLoc)
            .min()
            .getAsLong();
        System.out.println(sol);
    }
}
