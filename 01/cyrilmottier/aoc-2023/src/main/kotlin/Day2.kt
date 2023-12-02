val gameRexeg = "Game (\\d+)".toRegex()
val setColorRexeg = "(\\d+) (red|green|blue)".toRegex()

fun main(args: Array<String>) {
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
        .filter { game ->
            game.second.all { set ->
                set.getOrDefault("red", 0) <= 12
                        && set.getOrDefault("green", 0) <= 13
                        && set.getOrDefault("blue", 0) <= 14

            }
        }
        .sumOf { it.first }

    println(out)
}
