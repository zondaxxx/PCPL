module Program

open LabFunctions

let demonstrate () =
    printfn "Лабораторная работа №4. Функции и обработка данных в F#"
    printfn "Рулев К. А., ИУ5-35Б"
    printfn "\n1. Кортеж аргументов: %A" (tupledOperations (10, 3))
    printfn "   Каррированные аргументы: %A" (curriedOperations 10 3)
    printfn "2. Рекурсивная сумма 1..10: %d" (sumRange 1 10)
    printfn "3. Хвостовая сумма 1..10: %d" (sumRangeTail 1 10)
    printfn "   Хвостовая сумма 1..100000: %d" (sumRangeTail 1 100000)
    printfn "4. Автомат, команды [Hold; Next; Next; Next]: %A"
        (runTrafficLight [Hold; Next; Next; Next])
    printfn "5. Суммирование лямбдой, кортеж: %d"
        (applyTupled (1, 2, 3, fun a b c -> a + b + c))
    printfn "   Суммирование лямбдой, каррирование: %d"
        (applyCurried 1 2 3 (fun a b c -> a + b + c))
    printfn "6. Обобщённый кортеж: %A" (makeTriple true [1; 2] 'x')
    printfn "   Типы int, float, string выведены: %A" (inferredTriple 5 2.5 "F#")
    printfn "7. Двухэтапное обобщение: int = %d; float = %.1f; string = %s"
        (sumThreeInts 1 2 3)
        (sumThreeFloats 1.5 2.5 3.5)
        (sumThreeStrings "F#" " " "работает")
    printfn "8. Чётные числа, квадраты и кубы: %A" evenPowers
    printfn "9. Квадраты через if: %A" (squaresIf [-3; 0; 2])
    printfn "   Квадраты через match: %A" (squaresMatch [-3; 0; 2])
    let values = [5; 2; 4; 1; 3]
    printfn "   Исходный список для пунктов 10-12: %A" values
    printfn "10. Вложенные вызовы: sum = %d; fold = %d; zip = %A"
        (sumOrdinary values) (foldOrdinary values) (zipOrdinary values)
    printfn "11. Оператор |>: sum = %d; fold = %d; zip = %A"
        (sumPipeline values) (foldPipeline values) (zipPipeline values)
    printfn "12. Композиция >>: sum = %d; fold = %d; zip = %A"
        (sumComposition values) (foldComposition values) (zipComposition values)

[<EntryPoint>]
let main argv =
    match argv with
    | [||] -> demonstrate (); 0
    | [|"--test"|] -> Tests.run () |> ignore; 0
    | [|"--all"|] -> demonstrate (); printfn ""; Tests.run () |> ignore; 0
    | _ ->
        eprintfn "Использование: dotnet run -- [--test|--all]"
        2
