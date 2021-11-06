let n = int(input("> "))

let fib = fn(n) {
    if (n <= 1) {
        return n
    } else {
        return fib(n - 1) + fib(n - 2)
    }
}

print(fib(n))