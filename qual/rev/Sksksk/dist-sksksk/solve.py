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

# print(flag) # <function <lambda>.<locals>.<lambda>.<locals>.<lambda> at 0x104cc85e0>
