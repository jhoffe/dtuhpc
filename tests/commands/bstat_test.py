import unittest
from unittest.mock import Mock

from dtuhpc.commands import BStat


class BStatTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = Mock()
        self.connection.run.return_value = Mock(stdout="")

    def test_returns_empty_table(self):
        cmd = BStat(self.connection)
        out = cmd.run()

        self.assertListEqual(out.columns, [])
        self.assertListEqual(out.rows, [])


if __name__ == "__main__":
    unittest.main()
