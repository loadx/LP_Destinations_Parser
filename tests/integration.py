import os
import unittest

from main import process_taxonomies
from utils import current_dir


class IntegrationTestTaxonomy(unittest.TestCase):
    def test_loading_xml_produces_(self):
        result = process_taxonomies(os.path.join(current_dir(), 'tests/fixtures/taxonomies_small.xml'))
        self.assertEqual(len(result.tree), 9)

        # depth works correctly
        self.assertEqual(result['355614'].prev_item, result['355611'])
        self.assertEqual(result['355616'].prev_item, result['355611'])
