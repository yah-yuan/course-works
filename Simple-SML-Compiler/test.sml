(* A Comment*)
val rent = 1200
val string = "hey Bob"
val phon = 5551337 : int
val pi = 3.14159
val e = 2.718 : real
val nega = ~15
val y = rent + ~nega
val char = #"A"
val mul = pi * 0.1 + 3.0
val side = rent * (phon + nega)
val comp = 1 < 2 andalso 2>0
fun fibo n =
    if n = 0 then 0 else
    if n = 1 then 1 else
    fibo (n - 1) + fibo (n - 2)
fun is_large x = x > 37
fun thermometer temp =
    if temp < 37
    then "Cold"
    else if temp > 37
         then "Warm"
         else "Normal" 