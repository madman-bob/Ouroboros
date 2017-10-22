from unittest import TestCase

from ouroboros import ouroboros_exec


class TestFlowControls(TestCase):
    def test_if(self):
        self.assertEqual(
            ouroboros_exec("""
                if (2 == (1 + 1)) {
                    return 1;
                };
                return 2;
            """),
            1
        )

    def test_while(self):
        self.assertEqual(
            ouroboros_exec("""
                i = 0;
                total = 0;
                while (i < 10) {
                    i = (i + 1);
                    total = (total + i);
                };
                return total;
            """),
            55
        )
