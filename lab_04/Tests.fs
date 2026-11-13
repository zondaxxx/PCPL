module Tests

open LabFunctions

let run () =
    let mutable checks = 0
    let equal label expected actual =
        checks <- checks + 1
        if expected <> actual then
            failwithf "%s: ожидалось %A, получено %A" label expected actual

    equal "Кортеж аргументов" (13, 7, 30) (tupledOperations (10, 3))
    equal "Каррированные аргументы" (13, 7, 30) (curriedOperations 10 3)
    equal "Частичное применение" (13, 7, 30) ((curriedOperations 10) 3)

    for first, last, expected in [1, 10, 55L; -3, 3, 0L; 5, 5, 5L; 3, 1, 0L] do
        equal "Обычная рекурсия" expected (sumRange first last)
        equal "Хвостовая рекурсия" expected (sumRangeTail first last)
    equal "Большой диапазон и int64" 5000050000L (sumRangeTail 1 100000)
    equal "Верхняя граница int" 2147483647L (sumRangeTail System.Int32.MaxValue System.Int32.MaxValue)
    equal "Пустая последовательность команд" [Red] (runTrafficLight [])
    equal "Цикл автомата" [Red; Green; Yellow; Red] (runTrafficLight [Next; Next; Next])
    equal "Удержание в каждом состоянии"
        [Red; Red; Green; Green; Yellow; Yellow; Red]
        (runTrafficLight [Hold; Next; Hold; Next; Hold; Next])

    equal "Лямбда, кортеж" 6 (applyTupled (1, 2, 3, fun a b c -> a + b + c))
    equal "Лямбда, каррирование" 6 (applyCurried 1 2 3 (fun a b c -> a + b + c))
    equal "Переданная операция действительно вызывается" 14 (applyCurried 2 3 4 (fun a b c -> a + b * c))
    equal "Разные обобщённые типы" (true, [1; 2], 'x') (makeTriple true [1; 2] 'x')
    equal "Выведение int, float, string" (5, 2.5, "F#") (inferredTriple 5 2.5 "F#")
    equal "Обобщённое сложение int" 6 (sumThreeInts 1 2 3)
    equal "Обобщённое сложение float" 7.5 (sumThreeFloats 1.5 2.5 3.5)
    equal "Обобщённое сложение string" "F# работает" (sumThreeStrings "F#" " " "работает")
    equal "Списковое включение"
        [(2, 4, 8); (4, 16, 64); (6, 36, 216); (8, 64, 512); (10, 100, 1000)] evenPowers

    for values, expected in [[], []; [-3; 0; 2], [9; 0; 4]; [5], [25]] do
        equal "Head/Tail, if" expected (squaresIf values)
        equal "Head/Tail, match" expected (squaresMatch values)

    for values, expectedSum, expectedZip in
        [ [5; 2; 4; 1; 3], 20, [(2, 4); (4, 16)]
          [], 0, []
          [1; 3; 5], 0, []
          [-2; 4; 0; 2; -2], 28, [(-2, 4); (-2, 4); (0, 0); (2, 4); (4, 16)] ] do
        for calculate in [sumOrdinary; foldOrdinary; sumPipeline; foldPipeline; sumComposition; foldComposition] do
            equal "Агрегирование и fold во всех стилях" expectedSum (calculate values)
        for calculate in [zipOrdinary; zipPipeline; zipComposition] do
            equal "zip во всех стилях" expectedZip (calculate values)

    printfn "Проверки пройдены: %d." checks
    checks
