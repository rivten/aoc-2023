val digits = listOf("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

private fun findDigit(input: String, forward: Boolean): Int {
    var range: IntProgression = input.indices
    if (!forward) {
        range = range.reversed()
    }
    for (i in range) {
        val c = input[i]
        if (c.isDigit()) {
            return c.toString().toInt()
        } else {
            val substring = input.substring(i..<input.length)
            val match = digits.withIndex().firstOrNull { substring.startsWith(it.value) }?.index
            if (match != null) {
                return match
            }
        }
    }
    throw IllegalStateException()
}

fun main(args: Array<String>) {
    val calibrationSum = readInput("Day1").sumOf { line ->
        val first = findDigit(line, true)
        val last = findDigit(line, false)
        first * 10 + last
    }
    println(calibrationSum)
}
