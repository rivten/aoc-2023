fun main(args: Array<String>) {
    val calibrationSum = readInput("Day1").sumOf { line ->
        val first = line.first { it.isDigit() }
        val last = line.last { it.isDigit() }
        first.toString().toInt() * 10 + last.toString().toInt()
    }
    println(calibrationSum)
}
