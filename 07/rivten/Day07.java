import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Comparator;
import java.util.Collections;
import java.util.stream.Collectors;

class Day07 {

    private enum Card {
        Two,
        Three,
        Four,
        Five,
        Six,
        Seven,
        Eight,
        Nine,
        Ten,
        Jack,
        Queen,
        King,
        Ace,
    }

    static class HandComparator implements Comparator<List<Card>> {
        @Override
        public int compare(List<Card> a, List<Card> b) {
            var ra = rankHand(a);
            var rb = rankHand(b);
            if (ra == rb) {
                for (int i = 0; i < a.size(); ++i) {
                    if (a.get(i) != b.get(i)) {
                        return a.get(i).compareTo(b.get(i));
                    }
                }
                return 0;
            } else {
                return ra.compareTo(rb);
            }
        }

        private enum HandType {
            HighCard,
            OnePair,
            TwoPair,
            ThreeOfAKind,
            FullHouse,
            FourOfAKind,
            FiveOfAKind,
        }

        private static HandType rankHand(List<Card> hand) {
            var counts = new HashMap<Integer, List<Card>>();
            for (int i = 1; i <= 5; ++i) {
                counts.put(i, new ArrayList<Card>());
            }
            var seen = new HashSet<Card>();
            for (int i = 0; i < hand.size(); ++i) {
                Card c = hand.get(i);
                if (seen.contains(c)) {
                    continue;
                }

                int cardCount = 1;
                for (int j = i + 1; j < hand.size(); ++j) {
                    Card c2 = hand.get(j);
                    if (c == c2) {
                        cardCount++;
                    }
                }

                seen.add(c);
                counts.get(cardCount).add(c);
            }

            if (!counts.get(5).isEmpty()) {
                return HandType.FiveOfAKind;
            }
            if (!counts.get(4).isEmpty()) {
                return HandType.FourOfAKind;
            }
            if (!counts.get(3).isEmpty()) {
                if (!counts.get(2).isEmpty()) {
                    return HandType.FullHouse;
                } else {
                    return HandType.ThreeOfAKind;
                }
            }
            if (counts.get(2).size() > 1) {
                return HandType.TwoPair;
            }
            if (!counts.get(2).isEmpty()) {
                return HandType.OnePair;
            }

            return HandType.HighCard;
        }
    }

    private record HandBid(List<Card> hand, int bid) {}

    private static Card charToCard(int c) {
        return switch (c) {
            case '2' -> Card.Two;
            case '3' -> Card.Three;
            case '4' -> Card.Four;
            case '5' -> Card.Five;
            case '6' -> Card.Six;
            case '7' -> Card.Seven;
            case '8' -> Card.Eight;
            case '9' -> Card.Nine;
            case 'T' -> Card.Ten;
            case 'J' -> Card.Jack;
            case 'Q' -> Card.Queen;
            case 'K' -> Card.King;
            case 'A' -> Card.Ace;
            default -> null;
        };
    }

    public static void main(String[] args) {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        var hands = bi.lines()
            .map(l -> {
                var s = l.split(" ");
                var cards = s[0].chars()
                    .mapToObj(Day07::charToCard)
                    .toList();
                return new HandBid(cards, Integer.parseInt(s[1]));
            })
            .collect(Collectors.toList());
        hands.sort(new Comparator<HandBid>() {
            static final HandComparator hc = new HandComparator();

            @Override
            public int compare(HandBid a, HandBid b) {
                return hc.compare(a.hand, b.hand);
            }
        });
        int sol = 0;
        for (int i = 0; i < hands.size(); ++i) {
            sol += (i + 1) * hands.get(i).bid;
        }
        System.out.println(sol);
    }
}
