import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

class Day01 {
    private static int findCalibrationPart1(String line) {
        var numbers = line
            .chars()
            .filter(
                c -> c >= '0' && c <= '9'
            )
            .map(c -> c - '0')
            .boxed()
            .toList();
        return numbers.get(0) * 10 + numbers.get(numbers.size() - 1);
    }

    private static Integer getNumberAtIndex(String line, int i) {
        if (line.charAt(i) >= '0' && line.charAt(i) <= '9') {
            return line.charAt(i) - '0';
        }

        if (i + 3 > line.length()) {
            return null;
        }

        var sub3 = line.substring(i, i + 3);
        if (sub3.equals("one")) {
            return 1;
        }
        if (sub3.equals("two")) {
            return 2;
        }
        if (sub3.equals("six")) {
            return 6;
        }

        if (i + 4 > line.length()) {
            return null;
        }

        var sub4 = line.substring(i, i + 4);
        if (sub4.equals("four")) {
            return 4;
        }
        if (sub4.equals("five")) {
            return 5;
        }
        if (sub4.equals("nine")) {
            return 9;
        }

        if (i + 5 > line.length()) {
            return null;
        }

        var sub5 = line.substring(i, i + 5);
        if (sub5.equals("three")) {
            return 3;
        }
        if (sub5.equals("seven")) {
            return 7;
        }
        if (sub5.equals("eight")) {
            return 8;
        }

        return null;
    }

    private static int findCalibrationPart2(String line) {
        int firstNumber = -1;
        int lastNumber = -1;
        for (int i = 0; i < line.length(); i++) {
            Integer number = getNumberAtIndex(line, i);
            if (number != null) {
                if (firstNumber == -1) {
                    firstNumber = number;
                }
                lastNumber = number;
            }
        }
        return 10 * firstNumber + lastNumber;
    }

    public static void main(String[] args) {
        var bi = new BufferedReader(new InputStreamReader(System.in));
        var calibration = bi
            .lines()
            .mapToInt(Day01::findCalibrationPart2)
            .sum();
        System.out.println(calibration);
    }
}
