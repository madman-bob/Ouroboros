from unittest import TestCase

from ouroboros import ouroboros_eval, ouroboros_exec


class TestFunctions(TestCase):
    def test_function_basic(self):
        self.assertEqual(
            ouroboros_eval(
                '{ return 1 }()'
            ),
            1
        )

    def test_function_arguments_implicit_return(self):
        self.assertEqual(
            ouroboros_eval(
                'x => (x + 1) 1'
            ),
            2
        )

    def test_function_arguments_explicit_return(self):
        self.assertEqual(
            ouroboros_eval("""
                (x => {
                    return (x + 1);
                }) 1
            """),
            2
        )

    def test_function_multiple_arguments(self):
        self.assertEqual(
            ouroboros_eval("""
                (x => y => {
                    return (x + y);
                }) 1 2
            """),
            3
        )

    def test_double_return(self):
        self.assertEqual(
            ouroboros_exec("""
                my-return = {
                    return (return 1);
                };

                my-return();

                return 2;
            """),
            1
        )

    def test_fibonacci_iterative(self):
        self.assertEqual(
            ouroboros_exec("""
                fib = n => {
                    if (n < 2) {
                        return n;
                    };

                    i = 2;
                    a = 0;
                    b = 1;
                    c = 1;

                    while (i < n) {
                        i = i + 1;
                        a = b;
                        b = c;
                        c = a + b;
                    };

                    return c;
                };
                
                return [fib 1, fib 2, fib 3, fib 4, fib 5, fib 6];
            """).list,
            [1, 1, 2, 3, 5, 8]
        )

    def test_fibonacci_recursive(self):
        self.assertEqual(
            ouroboros_exec("""
                fib = (n => {
                    if (n < 2) {
                        return n;
                    };
                    return fib(n - 1) + fib(n - 2);
                });
                
                return [fib 1, fib 2, fib 3, fib 4, fib 5, fib 6];
            """).list,
            [1, 1, 2, 3, 5, 8]
        )
