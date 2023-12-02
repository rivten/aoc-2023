import kotlin.math.max

fun main(args: Array<String>) {
    val gameRexeg = "Game (\\d+)".toRegex()
    val setColorRexeg = "(\\d+) (red|green|blue)".toRegex()

    val out = readInput("Day2")
        .map { it.split(":") }
        .map { (game, sets) ->
            val gameId = gameRexeg.find(game)!!.groupValues[1].toInt()
            val pairs = sets.split(";").map { set ->
                set.split(", ").map { setColor ->
                    val count = setColorRexeg.find(setColor)!!.groupValues[1].toInt()
                    val color = setColorRexeg.find(setColor)!!.groupValues[2]
                    color to count
                }
            }
            gameId to pairs.map { it.toMap() }
        }
        .map { (game, sets) ->
            val minimum = sets.foldRight(Triple(0, 0, 0)) { item, acc ->
                Triple(
                    max(acc.first, item.getOrDefault("red", 0)),
                    max(acc.second, item.getOrDefault("green", 0)),
                    max(acc.third, item.getOrDefault("blue", 0)),
                )
            }
            game to minimum
        }
        .sumOf { it.second.first * it.second.second * it.second.third }

    println(out)
}
