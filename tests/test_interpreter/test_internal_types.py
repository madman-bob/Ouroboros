from unittest import TestCase

from ouroboros import ouroboros_exec


class TestInternalTypes(TestCase):
    def test_list_append(self):
        self.assertEqual(
            ouroboros_exec("""
                l = [1, 2, 3];
                l.append 4;
                return l;
            """).list,
            [1, 2, 3, 4]
        )

    def test_list_map(self):
        original_list, mapped_list = ouroboros_exec("""
            original_list = [1, 2, 3];
            mapped_list = original_list.map(x => x + 1);
            return [original_list, mapped_list];
        """).list

        self.assertEqual(original_list.list, [1, 2, 3])
        self.assertEqual(mapped_list.list, [2, 3, 4])

    def test_list_filter(self):
        original_list, filtered_list = ouroboros_exec("""
            original_list = [1, 2, 3];
            filtered_list = original_list.filter(x => x != 2);
            return [original_list, filtered_list];
        """).list

        self.assertEqual(original_list.list, [1, 2, 3])
        self.assertEqual(filtered_list.list, [1, 3])

    def test_list_reduce(self):
        l, item = ouroboros_exec("""
            l = [1, 2, 3];
            item = l.reduce(x => y => x + y) 0;
            return [l, item];
        """).list

        self.assertEqual(l.list, [1, 2, 3])
        self.assertEqual(item, 6)

