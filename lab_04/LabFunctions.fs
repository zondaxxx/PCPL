module LabFunctions

// 1. Аргументы-кортеж и каррированные аргументы; результат - кортеж.
let tupledOperations (a: int, b: int) = (a + b, a - b, a * b)
let curriedOperations (a: int) (b: int) = (a + b, a - b, a * b)

// 2. После рекурсивного вызова ещё выполняется сложение.
let rec sumRange first last =
    if first > last then 0L
    elif first = last then int64 first
    else int64 first + sumRange (first + 1) last

// 3. Аккумулятор переносит промежуточную сумму в следующий вызов.
let sumRangeTail first last =
    let rec loop current total =
        if current > last then total
        else
            let nextTotal = total + int64 current
            if current = last then nextTotal
            else loop (current + 1) nextTotal
    loop first 0L

// 4. Светофор: красный -> зелёный -> жёлтый -> красный.
type Light = Red | Green | Yellow
type Signal = Next | Hold

let runTrafficLight signals =
    let rec red remaining history =
        match remaining with
        | [] -> List.rev history
        | Hold :: rest -> red rest (Red :: history)
        | Next :: rest -> green rest (Green :: history)
    and green remaining history =
        match remaining with
        | [] -> List.rev history
        | Hold :: rest -> green rest (Green :: history)
        | Next :: rest -> yellow rest (Yellow :: history)
    and yellow remaining history =
        match remaining with
        | [] -> List.rev history
        | Hold :: rest -> yellow rest (Yellow :: history)
        | Next :: rest -> red rest (Red :: history)
    red signals [Red]

// 5. Функция суммирования передаётся как значение.
let applyTupled (a: int, b: int, c: int, operation) = operation a b c
let applyCurried (a: int) (b: int) (c: int) operation = operation a b c

// 6. В первом случае три независимых обобщённых типа.
let makeTriple a b c = (a, b, c)

// Без аннотаций: операнды задают int, float и string соответственно.
let inferredTriple a b c = (a + 0, b + 0.0, c + "")

// 7. Этап 1: inline-обобщение по поддерживаемому оператору (+).
let inline addThree a b c = a + b + c

// Этап 2: конкретизация обобщённой функции для трёх типов.
let sumThreeInts: int -> int -> int -> int = addThree
let sumThreeFloats: float -> float -> float -> float = addThree
let sumThreeStrings: string -> string -> string -> string = addThree

// 8. Списковое включение с фильтрацией чётных чисел.
let evenPowers =
    [ for value in 1 .. 10 do
          if value % 2 = 0 then
              yield (value, value * value, value * value * value) ]

// 9. Head и Tail доступны только после проверки непустого списка.
let rec squaresIf (values: int list) =
    if values.IsEmpty then []
    else values.Head * values.Head :: squaresIf values.Tail

let rec squaresMatch = function
    | [] -> []
    | (values: int list) ->
        values.Head * values.Head :: squaresMatch values.Tail

// 10. Обычные вложенные вызовы: map -> filter -> sort -> агрегирование.
let sumOrdinary values =
    List.sum (List.sort (List.filter (fun x -> x % 2 = 0)
        (List.map (fun x -> x * x) values)))

let foldOrdinary values =
    List.fold (+) 0 (List.sort (List.filter (fun x -> x % 2 = 0)
        (List.map (fun x -> x * x) values)))

let zipOrdinary values =
    let even = List.sort (List.filter (fun x -> x % 2 = 0) values)
    List.zip even (List.map (fun x -> x * x) even)

// 11. Те же три вычисления с оператором потока (|>).
let sumPipeline values =
    values
    |> List.map (fun x -> x * x)
    |> List.filter (fun x -> x % 2 = 0)
    |> List.sort
    |> List.sum

let foldPipeline values =
    values
    |> List.map (fun x -> x * x)
    |> List.filter (fun x -> x % 2 = 0)
    |> List.sort
    |> List.fold (+) 0

let zipPipeline values =
    let even = values |> List.filter (fun x -> x % 2 = 0) |> List.sort
    even |> List.map (fun x -> x * x) |> List.zip even

// 12. Композиция (>>) строит функцию до передачи ей списка.
let sumComposition =
    List.map (fun x -> x * x)
    >> List.filter (fun x -> x % 2 = 0)
    >> List.sort
    >> List.sum

let foldComposition =
    List.map (fun x -> x * x)
    >> List.filter (fun x -> x % 2 = 0)
    >> List.sort
    >> List.fold (+) 0

let zipComposition =
    List.filter (fun x -> x % 2 = 0)
    >> List.sort
    >> (fun even -> (List.map (fun x -> x * x) >> List.zip even) even)
