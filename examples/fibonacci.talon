import "examples/for"

let fib = function(n) {
    if (n <= 1) { n } else { fib(n - 1) + fib(n - 2) }
}

for(10)(function(value) {
    let n = int(input("> "))
    print(fib(n))
    # print(value)
})