let n = int(input("> "))

let fib = function(n) {
    if (n <= 1) { n } else { fib(n - 1) + fib(n - 2) }
}

print(fib(n))