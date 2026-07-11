#     )
#  ( /(                                   (           (
#  )\())    )  (           (              )\       (  )\
# ((_)\  ( /(  )(   `  )   )\ )     __ ((((_)(    ))\((_) (
#  _((_) )(_))(()\  /(/(  (()/(    / /  )\ _ )\  /((_)_   )\
# | || |((_)_  ((_)((_)_\  )(_))  / /   (_)_\(_)(_)) | | ((_)
# | __ |/ _` || '_|| '_ \)| || | /_/     / _ \  / -_)| |/ _ \
# |_||_|\__,_||_|  | .__/  \_, |        /_/ \_\ \___||_|\___/
#                  |_|     |__/
#
# Copyright 2026 Ismael Moreira
#
# This file is distributed under the BSD 3-Clause License.
#
# See the LICENSE.txt file for more information.
import sys
import os
import unittest
import unittest.mock

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.tooling import ToolChecker, TOOL_TABLE


class TestToolCheckerInitialization(unittest.TestCase):
    def test_init_happy_path(self) -> None:
        checker: ToolChecker = ToolChecker("rustc")

        self.assertEqual(checker.tool, "rustc")
        self.assertEqual(checker.expected_version, TOOL_TABLE["rustc"])
        self.assertEqual(checker.executable, "rustc")

    def test_init_python_alias_mapping(self) -> None:
        checker: ToolChecker = ToolChecker("python")

        self.assertEqual(checker.tool, "python")
        self.assertEqual(checker.expected_version, TOOL_TABLE["python"])
        self.assertEqual(checker.executable, "python3")

    @unittest.mock.patch("builtins.print")
    def test_init_error_untracked_tool(
        self, mock_print: unittest.mock.MagicMock
    ) -> None:
        with self.assertRaises(KeyError):
            ToolChecker("invalid_tool_name_999")

        mock_print.assert_called_once_with(
            "[Error] The tool 'invalid_tool_name_999' is not recognized or tracked by this repository."
        )
