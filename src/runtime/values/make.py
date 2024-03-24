from .derived import BooleanVal, NumberVal, NullVal, NativeFunctionVal

# sorta like C macros

def make_number(n : float = 0) -> NumberVal :
    return NumberVal(
        value=n
    )

def make_null() -> NullVal :
    return NullVal()

def make_bool(val : bool = True) :
    return BooleanVal(
        value=val
    )

def make_native_fn(callback) :
    return NativeFunctionVal(
        callback=callback
    )
