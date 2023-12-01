import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

static int findCalibration(String line) {
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

void main() {
    var bi = new BufferedReader(new InputStreamReader(System.in));
    var calibration = bi
        .lines()
        .mapToInt(l -> findCalibration(l))
        .sum();
    System.out.println(calibration);
}
