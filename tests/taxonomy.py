from __future__ import absolute_import

import unittest

from taxonomy import DoubleLinkedList, ListItem


class TestDoubleLinkedListBase(unittest.TestCase):
    def setUp(self):
        self.dllist = DoubleLinkedList()

    def tearDown(self):
        del(self.dllist)

    def test_add_item_exits_in_tree(self):
        self.dllist.add('1', 'First')
        self.assertTrue(len(self.dllist.tree), 1)
        self.assertTrue('1' in self.dllist.tree)

    def test_add_first_item_doesnt_change_tail(self):
        self.dllist.add('1', 'First')
        self.assertEqual(self.dllist.tail,  None)

    def test_add_item_changes_head_always(self):
        self.dllist.add('1', 'First')
        self.assertEqual(self.dllist.head,  self.dllist['1'])
        self.assertIsInstance(self.dllist.head, ListItem)

    def test_add_sets_tree_next_pointer(self):
        self.dllist.add('1', 'First')
        self.dllist.add('2', 'Second')
        self.assertEqual(self.dllist['1'].next_item, self.dllist['2'])

    def test_add_sets_tree_prev_pointer(self):
        self.dllist.add('1', 'First')
        self.dllist.add('2', 'Second')
        self.assertTrue(self.dllist['2'].prev_item, self.dllist['1'])

    def test_set_next_pointer_no_tail(self):
        item = ListItem(('2', 'Second'))
        self.dllist.add('1', 'First')
        self.assertEqual(self.dllist.set_next_pointer(item), None)

    def test_set_prev_pointer_no_tail(self):
        item = ListItem(('2', 'Second'))
        self.dllist.add('1', 'First')
        self.assertEqual(self.dllist.set_prev_pointer(item), None)

    def test_set_next_pointer_with_tail_override(self):
        item = ListItem(('3', 'Third'))
        self.dllist.add('1', 'First')
        self.dllist.add('2', 'Second')
        self.assertEqual(self.dllist.set_next_pointer(item), item)

    def test_set_prev_pointer_with_tail_override(self):
        item = ListItem(('3', 'Third'))
        self.dllist.add('1', 'First')
        self.dllist.add('2', 'Second')
        self.assertEqual(self.dllist.set_prev_pointer(item), item)

    def test_set_next_pointer_with_tail(self):
        self.dllist.add('1', 'First')
        self.dllist.add('2', 'Second')
        self.assertEqual(self.dllist.set_next_pointer(), self.dllist['2'])

    def test_set_prev_pointer_with_tail(self):
        self.dllist.add('1', 'First')
        self.dllist.add('2', 'Second')
        self.assertEqual(self.dllist.set_prev_pointer(), self.dllist['1'])


class TestDoubleLinkedListMethod(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.dllist = DoubleLinkedList()
        self.dllist.add('1', 'First')
        self.dllist.add('2', 'Second')
        self.dllist.add('3', 'Third')
        self.dllist.add('4', 'Fourth')

        self.tree_length = len(self.dllist.tree)

    def test_flatten_default(self):
        result = self.dllist.flatten('1', False)
        self.assertEqual(['First', 'Second', 'Third', 'Fourth'], result)

    def test_flatten_with_max_items(self):
        result = self.dllist.flatten('1', False, max_items=3)
        self.assertTrue(len(result), 3)
        self.assertEqual(['First', 'Second', 'Third'], result)

    def test_print_nav_reverse(self):
        result = self.dllist.flatten('4', True)
        self.assertEqual(['Fourth', 'Third', 'Second', 'First'], result)

    def test_print_nav_reverse_with_max(self):
        result = self.dllist.flatten('4', True, max_items=3)
        self.assertEqual(['Fourth', 'Third', 'Second'], result)
