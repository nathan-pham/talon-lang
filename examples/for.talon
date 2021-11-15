let for = function(value) {
    function(callback) {
        if(value > 0) {
            callback(value)
            return for(value - 1)(callback)
        } else {
            return value
        }
    }
}

# for(10)(function(value) {
    # print(value)
# })