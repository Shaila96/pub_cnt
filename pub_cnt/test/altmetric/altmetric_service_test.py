import unittest
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from altmetric.altmetric_service import AltmetricService

class AltmetricServiceTests(unittest.TestCase):
  def test_canary(self):
    self.assertTrue(True)
