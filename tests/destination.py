from __future__ import absolute_import

import os
import unittest

from common import current_dir
from destination import Destination
from taxonomy import DoubleLinkedList
from StringIO import StringIO


class TestDesintationClassMethods(unittest.TestCase):
    def test_sanitize_name(self):
        self.assertEqual(Destination.sanitize_name('Africa'), 'africa')
        self.assertEqual(Destination.sanitize_name('Port Sudan'), 'port_sudan')
        self.assertEqual(Destination.sanitize_name('KwaZulu-Natal'), 'kwazulu-natal')

    def test_sanitize_heading(self):
        self.assertEqual(Destination.sanitize_heading('africa'), 'Africa')
        self.assertEqual(Destination.sanitize_heading('Port_sudan'), 'Port Sudan')
        self.assertEqual(Destination.sanitize_heading('KwaZulu-Natal'), 'Kwazulu-Natal')


class TestDestination(unittest.TestCase):
    def setUp(self):
        self.fixture_name = os.path.join(current_dir(), 'tests/fixtures', 'destination_small.xml')
        self.destination = Destination('testing', StringIO())  # fake a file handle

    def test_init(self):
        message = "file_pointer is invalid or no write permissions"
        self.assertRaises(Exception, message, Destination, 'testing', 'not_file')
        self.assertRaises(Exception, message, Destination, 'testing', open(self.fixture_name, 'r'))

    def test_build_block(self):
        expected = "<h2>Money</h2><p>Testing of the buffer</p>\n"
        block = self.destination.build_block('money', 'Testing of the buffer')
        self.assertEqual(block, expected)
        self.assertEqual(self.destination.filled_items, ['money'])

    def test_build_block_appends(self):
        expected = "<h2>Money</h2><p>Testing of the buffer</p>\n"
        block = self.destination.build_block('money', 'Testing of the buffer')
        block = self.destination.build_block('history', 'more testing')
        expected += "<h2>History</h2><p>more testing</p>\n"
        self.assertEqual(block, expected)
        self.assertEqual(self.destination.filled_items, ['money', 'history'])

    def test_non_processed_build_block(self):
        destination = Destination('testing', StringIO(), tags_to_capture=['history', 'overview'])
        block = self.destination.build_block('air', 'i produce nothing')
        self.assertEqual(block, '')

    def test_some_processed_build_block(self):
        destination = Destination('testing', StringIO(), tags_to_capture=['money', 'history'])
        expected = "<h2>Money</h2><p>Testing of the buffer</p>\n"
        block = self.destination.build_block('money', 'Testing of the buffer')
        block = self.destination.build_block('air', '')
        self.assertEquals(block, expected)
        block = self.destination.build_block('history', 'Testing')
        expected += "<h2>History</h2><p>Testing</p>\n"
        self.assertEqual(block, expected)

    def test_get_nav_top(self):
        taxonomy = DoubleLinkedList()
        taxonomy.add('1', 'One')
        taxonomy.add('2', 'Two')
        taxonomy.add('3', 'Three')
        taxonomy.add('4', 'Four')
        taxonomy.add('5', 'Five')
        result = Destination.get_nav(taxonomy, '1')
        self.assertEqual(['Two', 'Three'], result)

    def test_get_nav_middle(self):
        taxonomy = DoubleLinkedList()
        taxonomy.add('1', 'One')
        taxonomy.add('2', 'Two')
        taxonomy.add('3', 'Three')
        taxonomy.add('4', 'Four')
        taxonomy.add('5', 'Five')
        result = Destination.get_nav(taxonomy, '3')
        self.assertEqual(['One', 'Two', 'Four', 'Five'], result)

    def test_get_nav_end(self):
        taxonomy = DoubleLinkedList()
        taxonomy.add('1', 'One')
        taxonomy.add('2', 'Two')
        taxonomy.add('3', 'Three')
        taxonomy.add('4', 'Four')
        taxonomy.add('5', 'Five')
        result = Destination.get_nav(taxonomy, '5')
        self.assertEqual(['Three', 'Four'], result)
