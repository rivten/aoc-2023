import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;
import java.util.stream.Collectors;

class Day04 {

    private record Card(Set<Integer> winning, Set<Integer> you) {
        private static Set<Integer> parseCards(String raw) {
            return Arrays.stream(raw.split(" "))
                .filter(s -> s.length() != 0)
                .map(String::trim)
                .map(Integer::parseInt)
                .collect(Collectors.toSet());
        }

        private static Card parse(String line) {
            var cards = line.split(":")[1];
            var cardsSplitted = cards.split("\\|");
            var winningCards = cardsSplitted[0];
            var youCards = cardsSplitted[1];
            return new Card(parseCards(winningCards), parseCards(youCards));
        }

        private int points() {
            var common = new HashSet<Integer>(winning);
            common.retainAll(you);
            if (common.size() == 0) {
                return 0;
            } else {
                return 1 << (common.size() - 1);
            }
        }
    }

    public static void main(String[] args) {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        var sol = bi.lines()
            .map(Card::parse)
            .mapToInt(Card::points)
            .sum();
        System.out.println(sol);
    }
}
