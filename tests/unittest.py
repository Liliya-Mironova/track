import unittest
from app.DoubleLinkedList import DoubleLinkedList


class TestListMethods(unittest.TestCase):
    def setUp(self):
        self.num_elements = 3
        self.shift = 2
        self.dll = DoubleLinkedList()
        for i in range(self.num_elements):
            self.dll.push(i)

        # empty:
        self.to_empty_data = 1
        self.empty_list = DoubleLinkedList()

        # one_elem:
        self.one_elem_list = DoubleLinkedList()
        self.one_data = 0
        self.one_elem_list.push(self.one_data)

    def test_push(self):
        length = self.dll.len()
        for i in range(self.num_elements, self.num_elements + self.shift):
            self.dll.push(i)
            length += 1
            self.assertEqual(self.dll.len(), length)
            self.assertTrue(self.dll.contains(i))
            self.assertEqual(self.dll.get_last().data, i)

        # (empty):
        self.empty_list.push(self.to_empty_data)
        self.assertEqual(self.empty_list.len(), 1)
        self.assertTrue(self.empty_list.contains(self.to_empty_data))

    def test_pop(self):
        length = self.dll.len()
        for i in range(self.num_elements):
            result = self.dll.pop()
            length -= 1
            self.assertEqual(self.dll.len(), length)
            self.assertEqual(self.num_elements - i - 1, result)

        # empty:
        with self.assertRaises(RuntimeError):
            self.empty_list.pop()

        # one_elem:
        data = self.one_elem_list.get_first().data
        elem = self.one_elem_list.pop()
        self.assertEqual(self.one_elem_list.len(), 0)
        self.assertEqual(data, elem)

    def test_shift(self):
        length = self.dll.len()
        for i in range(self.num_elements, self.num_elements + self.shift):
            self.dll.shift(i)
            length += 1
            self.assertEqual(self.dll.len(), length)
            self.assertTrue(self.dll.contains(i))
            self.assertEqual(self.dll.get_first().data, i)

        # (empty):
        self.empty_list.shift(self.to_empty_data)
        self.assertEqual(self.empty_list.len(), 1)
        self.assertEqual(self.empty_list.get_first().data, self.to_empty_data)

    def test_unshift(self):
        length = self.dll.len()
        for i in range(self.num_elements):
            self.dll.unshift()
            length -= 1
            self.assertFalse(self.dll.contains(i))
            self.assertEqual(self.dll.len(), length)

        # empty:
        with self.assertRaises(RuntimeError):
            self.empty_list.unshift()

        # one_elem:
        self.one_elem_list.delete(self.one_data)

    def test_contains(self):
        for i in range(self.num_elements):
            self.assertTrue(self.dll.contains(i))
            self.dll.delete(i)
            self.assertFalse(self.dll.contains(i))

        self.dll.push(0)
        for i in range(self.num_elements, self.num_elements + self.shift):
            self.assertFalse(self.dll.contains(i))

        # empty:
        self.assertFalse(self.one_elem_list.contains(1))

        # one_elem:
        self.assertTrue(self.one_elem_list.contains(self.one_data))
        self.assertFalse(self.one_elem_list.contains(self.to_empty_data))

    def test_delete(self):
        length = self.dll.len()
        for i in range(self.num_elements):
            self.dll.delete(i)
            length -= 1
            self.assertFalse(self.dll.contains(i))
            self.assertEqual(self.dll.len(), length)

        for i in range(self.num_elements, self.num_elements + self.shift + 2):
            self.dll.push(i)

        self.dll.delete(self.num_elements + self.shift + 1)

        # empty:
        with self.assertRaises(RuntimeError):
            self.empty_list.delete(1)

        # one_elem:
        self.one_elem_list.delete(0)

    def test_get_first(self):
        for i in range(self.num_elements):
            self.assertEqual(self.dll.get_first().data, i)
            self.dll.unshift()

        # empty:
        self.assertIsNone(self.empty_list.get_first())

        # one_elem:
        self.assertEqual(self.one_elem_list.get_first().data, self.one_data)

    def test_get_last(self):
        for i in range(self.num_elements):
            self.assertEqual(self.dll.get_last().data, self.num_elements-i-1)
            self.dll.pop()

        # empty - error
        self.assertIsNone(self.empty_list.get_last())

        # one_elem:
        self.assertEqual(self.one_elem_list.get_last().data, self.one_data)

    def test_len(self):
        length = self.dll.len()
        for i in range(self.num_elements, self.num_elements + self.shift):
            self.dll.push(i)
            length += 1
            self.assertEqual(self.dll.len(), length)

        for i in range(self.num_elements + self.shift):
            self.dll.pop()
            length -= 1
            self.assertEqual(self.dll.len(), length)

        # empty:
        self.assertEqual(self.empty_list.len(), 0)

        # one_elem:
        self.assertEqual(self.one_elem_list.len(), 1)


if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/unittest.py
