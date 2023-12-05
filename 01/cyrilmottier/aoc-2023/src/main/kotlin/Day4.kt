import kotlin.math.pow

fun main(args: Array<String>) {
    val result = readInput("Day4")
        .filter { it.isNotEmpty() }
        .map { line ->
            println(line)
            val (_, numbersRaw) = line.split(Regex(": +"))
            val (winningNumbers, numbers) = numbersRaw.split(Regex(" \\| +"))
            val wn = winningNumbers.split(Regex(" +")).map { it.toInt() }
            val n = numbers.split(Regex(" +")).map { it.toInt() }
            wn to n
        }
        .map {
            it.second.intersect(it.first.toSet())
        }
        .sumOf { 2.0.pow((it.size - 1).toDouble()).toInt() }
    println(result)
}
