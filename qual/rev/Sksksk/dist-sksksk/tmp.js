const S = x => y => z => x(z)(y(z));
const K = x => y => x;

// a->b->c->b(a b c)
// x0->x1->x2->x1(x0(x1)(x2))
const a = S(S(K(S))(K)) 

// a->b->c->d->a c(b c d)
// x3->x4->x5->x6->x3(x5)(x4(x5)(x6))
const b = S(K(S))(S(K(S(K(S))(K))))

// a->b->c->a(b c)
// x7->x8->x9->x7(x8(x9))
const c = S(K(S))(K)

// a->b->a(a b)
// x10->x11->x10(x10(x11))
const d = S(S(K(S))(K))(S(K)(K))

// S(K(S))(S(K(S(K(S))(K))))(S(S(K(S))(K))(S(K)(K)))(S(S(K(S))(K))(S(S(K(S))(K))(S(K)(K))))
// a->b->a(a(a(a(a b))))
// x12->x13->x12(x12(x12(x12(x12(x13)))))
const e = b(d)(a(d))

// a->b->b a
// x14->x15->x15(x14)
const f = S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))

// S(K(S(K(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K)(K))))))))(S(K(S(K(S(K)(K)))))(S(K(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(K))))))(S(K(S(K(K))))(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(S(K(S(K(S(S(K)(K))))))(S(K(S(K(K))))(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))))))(K)))))
// a->b->c->a(c->(a->b->a)((a->b->c->a c(b c))((a->b->c->a c(b c))(a->b->a)(a->b->a))) c((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))((a->b->a)(a->b->a))))((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))((a->b->c->a c(b c))(a->b->a)(a->b->a))))((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))(a->b->a)(a->b->a)))(a->b->a))) b c))(b->c)(c->(a->b->a) c((a->b->a) c))
// x16->x17->x18->
const g = S(K(S(K(S(K(f(S(K)(K))))))))(S(K(S(K(S(K)(K)))))(S(K(S(K(S(S(K(f))(K))))))(S(K(S(K(K))))(S(K(S(S(K(f))(S(K(S(K(S(S(K)(K))))))(S(K(S(K(K))))(f))))))(K)))))

// S(K(S(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K(S(K(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K)(K))))))))(S(K(S(K(S(K)(K)))))(S(K(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(K))))))(S(K(S(K(K))))(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(S(K(S(K(S(S(K)(K))))))(S(K(S(K(K))))(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))))))(K)))))))))(K)
// (a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))((a->b->c->a c(b c))(a->b->a)(a->b->a))))((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))(a->b->a)(a->b->a)))(a->b->a))(a->b->c->a(c->(a->b->a)((a->b->c->a c(b c))((a->b->c->a c(b c))(a->b->a)(a->b->a))) c((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))((a->b->a)(a->b->a))))((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))((a->b->c->a c(b c))(a->b->a)(a->b->a))))((a->b->c->a c(b c))((a->b->a)((a->b->c->a c(b c))(a->b->a)(a->b->a)))(a->b->a))) b c))(b->c)(c->(a->b->a) c((a->b->a) c))))))(a->b->a)
// 
const h = S(K(S(f(g))))(K)

// a->b->a b(b->c->(a->b->a) c(b c))
const i = S(S)(K(K(S(K))))

// S(K(S(K(S(S(S(K)(K))(K(K(S(K)))))(K(K))))))(S(K(S(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K(S(K(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K)(K))))))))(S(K(S(K(S(K)(K)))))(S(K(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(K))))))(S(K(S(K(K))))(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(S(K(S(K(S(S(K)(K))))))(S(K(S(K(K))))(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))))))(K)))))))))(K))
const j = S(K(S(K(S(S(S(K)(K))(K(K(S(K)))))(K(K))))))(h)

// S(S(K(S))(S(K(S(K(S(S)(K(K(S(K))))))))(S(K(S(K(S(S(S(K)(K))(K(K(S(K)))))(K(K))))))(S(K(S(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K(S(K(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K)(K))))))))(S(K(S(K(S(K)(K)))))(S(K(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(K))))))(S(K(S(K(K))))(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(S(K(S(K(S(S(K)(K))))))(S(K(S(K(K))))(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))))))(K)))))))))(K)))))(S(K(S(S(K(S(K(S(S(S(K)(K))(K(K(S(K)))))(K(K))))))(S(K(S(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K(S(K(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))(S(K)(K))))))))(S(K(S(K(S(K)(K)))))(S(K(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(K))))))(S(K(S(K(K))))(S(K(S(S(K(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))(S(K(S(K(S(S(K)(K))))))(S(K(S(K(K))))(S(K(S(S(K)(K))))(S(K(S(K)(K)))(K))))))))(K)))))))))(K)))))(K))
const l = S(S(K(S))(S(K(S(K(i))))(j)))(S(K(S(j)))(K))

const flag = S(S(l(b(c(c(d)(e))(c(d)(e)))(a(d))))(K(S(S(l(c(c(d)(a(d)))(g(c(e)(b(d)(d))))))(K(S(S(l(b(c(b(c(d)(h(e)(d)))(e))(c(a(d))(a(d))))(d)))(K(S(S(l(c(b(c(d)(a(d)))(e))(b(c(d)(a(d)))(e))))(K(S(S(l(c(a(d))(a(c(c(c(d)(d))(d))(e)))))(K(S(S(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(K(S(S(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(K(S(S(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(K(S(S(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(K(S(S(l(c(e)(g(c(b(d)(d))(e)))))(K(S(S(l(c(e)(a(c(d)(e)))))(K(S(S(l(c(a(d))(g(c(e)(c(c(d)(d))(d))))))(K(S(S(l(c(c(d)(a(d)))(g(c(e)(b(d)(d))))))(K(S(S(l(c(b(e)(d))(b(e)(d))))(K(S(S(l(c(c(d)(e))(a(c(d)(e)))))(K(S(S(l(b(c(c(d)(e))(c(d)(e)))(a(d))))(K(S(S(l(c(e)(g(c(b(d)(d))(e)))))(K(S(S(l(c(g(c(d)(e)))(a(c(d)(e)))))(K(S(S(l(c(a(b(d)(e)))(a(e))))(K(S(S(l(g(c(c(d)(e))(a(c(d)(e))))))(K(S(S(l(c(c(c(d)(d))(c(d)(d)))(b(d)(e))))(K(S(S(l(c(b(e)(d))(b(e)(d))))(K(S(S(l(a(c(e)(c(d)(e)))))(K(S(S(l(c(e)(a(c(d)(e)))))(K(S(S(l(a(c(e)(c(d)(e)))))(K(S(S(l(c(b(e)(b(d)(d)))(b(d)(e))))(K(S(S(l(c(e)(g(c(b(d)(d))(e)))))(K(S(S(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(K(S(S(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(K(S(S(l(c(e)(b(d)(c(a(d))(b(d)(e))))))(K(S(S(l(g(c(b(b(d)(d))(e))(b(d)(c(d)(e))))))(K(l(c(e)(c(e)(e))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K))))))(K(S(K)))

// Print the function flag to the console