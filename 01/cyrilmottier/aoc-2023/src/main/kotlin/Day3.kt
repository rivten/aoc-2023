fun main(args: Array<String>) {
    val board = readInput("Day3")
    val boardHeight = board.size
    val boardWidth = board[0].length

    fun checkPartDigit(row: Int, col: Int): Boolean {
        for (i in -1..1) {
            for (j in -1..1) {
                if (i == 0 && j == 0) continue
                val cell = board.getOrNull(row + i)?.getOrNull(col + j) ?: continue
                if (cell !in '0'..'9' && cell != '.') {
                    return true
                }
            }
        }
        return false
    }

    val partNumbers = mutableListOf<Int>()
    for (row in 0..<boardHeight) {
        var isPartNumber = false
        var number = 0
        for (col in 0..<boardWidth) {
            when (val c = board[row][col]) {
                in '0'..'9' -> {
                    isPartNumber = isPartNumber || checkPartDigit(row, col)
                    number = number * 10 + c.digitToInt()
                    println("Checking $row, $col, $isPartNumber, $number")
                }

                else -> {
                    if (isPartNumber) {
                        partNumbers += number
                    }
                    isPartNumber = false
                    number = 0
                }
            }
        }
        if (isPartNumber) {
            partNumbers += number
        }
    }

    println(partNumbers.sum())
}
