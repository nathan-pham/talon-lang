# import & export
import "examples/for"

# assignment, conditional, and function
let fib = function(n) {
    if (n <= 1) { n } else { fib(n - 1) + fib(n - 2) }
}

let results = []

for(10)(function(value) {
    let n = int(input("> "))
    results.append(fib(n))

    # comments
    # print(value)
})

for(len(results) - 1)(function(value) {
    print(results[value])
})