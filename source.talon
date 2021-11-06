let n = int(input("> "))

let fib = function(n) {
    if (n <= 1) {
        return n
    } else {
        return fib(n - 1) + fib(n - 2)
    }
}

# lmao

print(fib(n))