import sys

# Increase Python's recursion limit.
# SKI combinators and Church numerals can lead to deep recursion.
# The required limit can be very high depending on the flag length and complexity.
# Start with a high value; adjust if RecursionError still occurs.
sys.setrecursionlimit(250000) # Adjusted from 200k as some complex cases might need more

# --- Provided SKI Combinator Definitions ---
s = lambda x: lambda y: lambda z: x(z)(y(z))
k = lambda x: lambda y: x
a = s(s(k(s))(k))
b = s(k(s))(s(k(s(k(s))(k))))
c = s(k(s))(k)
d = s(s(k(s))(k))(s(k)(k))
e = b(d)(a(d))
f = s(k(s(s(k)(k))))(s(k(s(k)(k)))(k))
g = s(k(s(k(s(k(f(s(k)(k))))))))(s(k(s(k(s(k)(k)))))(s(k(s(k(s(s(k(f))(k))))))(s(k(s(k(k))))(s(k(s(s(k(f))(s(k(s(k(s(s(k)(k))))))(s(k(s(k(k))))(f))))))(k)))))
h = s(k(s(f(g))))(k)
i = s(s)(k(k(s(k))))
j = s(k(s(k(s(s(s(k)(k))(k(k(s(k)))))(k(k))))))(h)
l = s(s(k(s))(s(k(s(k(i))))(j)))(s(k(s(j)))(k))
flag = s(s(l(b(c(c(d)(e))(c(d)(e)))(a(d))))(k(s(s(l(c(c(d)(a(d)))(g(c(e)(b(d)(d))))))(k(s(s(l(b(c(b(c(d)(h(e)(d)))(e))(c(a(d))(a(d))))(d)))(k(s(s(l(c(b(c(d)(a(d)))(e))(b(c(d)(a(d)))(e))))(k(s(s(l(c(a(d))(a(c(c(c(d)(d))(d))(e)))))(k(s(s(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(k(s(s(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(k(s(s(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(k(s(s(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(k(s(s(l(c(e)(g(c(b(d)(d))(e)))))(k(s(s(l(c(e)(a(c(d)(e)))))(k(s(s(l(c(a(d))(g(c(e)(c(c(d)(d))(d))))))(k(s(s(l(c(c(d)(a(d)))(g(c(e)(b(d)(d))))))(k(s(s(l(c(b(e)(d))(b(e)(d))))(k(s(s(l(c(c(d)(e))(a(c(d)(e)))))(k(s(s(l(b(c(c(d)(e))(c(d)(e)))(a(d))))(k(s(s(l(c(e)(g(c(b(d)(d))(e)))))(k(s(s(l(c(g(c(d)(e)))(a(c(d)(e)))))(k(s(s(l(c(a(b(d)(e)))(a(e))))(k(s(s(l(g(c(c(d)(e))(a(c(d)(e))))))(k(s(s(l(c(c(c(d)(d))(c(d)(d)))(b(d)(e))))(k(s(s(l(c(b(e)(d))(b(e)(d))))(k(s(s(l(a(c(e)(c(d)(e)))))(k(s(s(l(c(e)(a(c(d)(e)))))(k(s(s(l(a(c(e)(c(d)(e)))))(k(s(s(l(c(b(e)(b(d)(d)))(b(d)(e))))(k(s(s(l(c(e)(g(c(b(d)(d))(e)))))(k(s(s(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(k(s(s(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(k(s(s(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(k(s(s(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(k(l(c(e)(c(e)(e))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k))))))(k(s(k)))
# --- End of Provided Definitions ---

# Buffer to store the output characters
output_chars_buffer = []

# I_combinator = SKK. In Python lambda form: s(k)(k) = lambda x: x
I_combinator = s(k)(k)

# p_processor function:
# Takes a Church-encoded character, decodes it, stores it,
# and returns a function that accepts the continuation.
# This structure is `p = lambda item: lambda continuation: (action_on_item, continuation)[1]`
def p_processor(church_char_code_func):
    def continuation_taker(continuation_expr):
        # Convert Church numeral to integer:
        # A Church numeral `n` is `lambda f: lambda x: f(f(...f(x)...))` (n times).
        # To get integer value, apply it to `f = lambda i: i + 1` and `x = 0`.
        char_code_as_int = church_char_code_func(lambda i: i + 1)(0)
        
        try:
            output_chars_buffer.append(chr(char_code_as_int))
        except ValueError:
            output_chars_buffer.append(f"[Error: InvalidCharCode({char_code_as_int})]")
            
        return continuation_expr # Return the rest of the computation
    
    return continuation_taker

flag(p_processor)

# # --- Execution ---
# print("⏳ Starting evaluation of the combinator expression... This might take a while.")
# try:
#     # Apply the main 'flag' expression to our p_processor.
#     # The 'flag' expression itself is s(A)(B), so it's `lambda z_arg: A(z_arg)(B(z_arg))`.
#     # We pass `p_processor` as this `z_arg`.
#     result_of_flag_application = flag(p_processor)
    
#     print("✅ Evaluation finished.")
    
#     # Verify if the result behaves like the I_combinator
#     # (i.e., returns its argument unchanged).
#     test_object = "test_identity"
#     try:
#         if result_of_flag_application(test_object) == test_object:
#             print("ℹ️ The result of the flag application behaves like the I_combinator (Identity), as expected for this pattern.")
#         else:
#             print("⚠️ The result of the flag application DOES NOT behave like the I_combinator. The output might be incomplete or the pattern is different.")
#     except Exception as e:
#         print(f"⚠️ Error while testing the result with I_combinator behavior: {e}")
#         print("Output might still be valid if the expression doesn't terminate with I.")


#     final_output_string = "".join(output_chars_buffer)
    
#     if final_output_string:
#         print("\n🚩 Captured output string:")
#         print(final_output_string)
#     else:
#         print("\n🚫 No output was captured. Possible reasons:")
#         print("  1. RecursionError occurred (check console output if any part of this message is truncated).")
#         print("  2. The `p_processor` or `I_combinator` logic doesn't match the expression's output mechanism.")
#         print("  3. The expression doesn't encode a string in this specific Church-numeral-list manner.")
#         print("  4. The expression needs to be applied differently.")

# except RecursionError:
#     print("\n❌ RecursionError: The expression is too complex for the current Python recursion limit.")
#     print(f"  Current limit was: {sys.getrecursionlimit()}")
#     print("  Consider increasing it further if you have enough system memory (e.g., `sys.setrecursionlimit(300000)`),")
#     print("  but be aware this can lead to a stack overflow and crash Python.")
#     final_output_string = "".join(output_chars_buffer)
#     if final_output_string:
#         print("\n partiellement captured output string before RecursionError:")
#         print(final_output_string)
# except Exception as e:
#     print(f"\n❌ An unexpected error occurred during evaluation: {type(e).__name__} - {e}")
#     final_output_string = "".join(output_chars_buffer)
#     if final_output_string:
#         print("\n partiellement captured output string before error:")
#         print(final_output_string)