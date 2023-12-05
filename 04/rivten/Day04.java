import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Set;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Arrays;
import java.util.stream.Collectors;
import java.util.function.Function;

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

        private int matchingCount() {
            var common = new HashSet<Integer>(winning);
            common.retainAll(you);
            return common.size();
        }

        private int points() {
            var matchingCount = matchingCount();
            if (matchingCount == 0) {
                return 0;
            } else {
                return 1 << (matchingCount - 1);
            }
        }
    }

    public static void main(String[] args) {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        var cards = bi.lines()
            .map(Card::parse)
            .toList();
        var cardCount = new HashMap<Integer, Integer>();
        for (int cardIndex = 0; cardIndex < cards.size(); ++cardIndex) {
            cardCount.put(cardIndex + 1, 1);
        }
        int cardIndex = 1;
        for (var card: cards) {
            var matchingCount = card.matchingCount();
            var currentCardCount = cardCount.get(cardIndex);
            for (int i = 0; i < matchingCount; ++i) {
                var cardIndexToAdd = cardIndex + i + 1;
                var oldCardCount = cardCount.get(cardIndexToAdd);
                var newCardCount = oldCardCount + currentCardCount;
                cardCount.put(cardIndexToAdd, newCardCount);
            }
            cardIndex++;
        }
        System.out.println(cardCount.values().stream().reduce(0, (acc, v) -> acc + v));
    }
}
