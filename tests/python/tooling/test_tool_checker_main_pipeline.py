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
import argparse

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.tooling import main, TOOL_TABLE


class TestToolCheckerMainPipeline(unittest.TestCase):
    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("builtins.print")
    def test_main_list_argument(
        self, mock_print: unittest.mock.MagicMock, mock_parse: unittest.mock.MagicMock
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=True, get_version=None, search=None, all=False
        )

        main()

        mock_print.assert_any_call("Registered baseline configurations:")
        for tool in TOOL_TABLE.keys():
            self.assertTrue(
                any(tool in call.args[0] for call in mock_print.call_args_list)
            )

    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("sys.exit")
    @unittest.mock.patch("builtins.print")
    def test_main_get_version_tracked_tool(
        self,
        mock_print: unittest.mock.MagicMock,
        mock_exit: unittest.mock.MagicMock,
        mock_parse: unittest.mock.MagicMock,
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=False, get_version="rustc", search=None, all=False
        )

        main()

        mock_print.assert_called_once_with(f"rustc: {TOOL_TABLE['rustc']}")
        mock_exit.assert_not_called()

    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("sys.exit")
    def test_main_get_version_untracked_tool_exits(
        self, mock_exit: unittest.mock.MagicMock, mock_parse: unittest.mock.MagicMock
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=False, get_version="unknown_tool", search=None, all=False
        )

        main()

        mock_exit.assert_called_once_with(1)

    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("scripts.tooling.ToolChecker.verify")
    @unittest.mock.patch("sys.exit")
    def test_main_search_happy_path(
        self,
        mock_exit: unittest.mock.MagicMock,
        mock_verify: unittest.mock.MagicMock,
        mock_parse: unittest.mock.MagicMock,
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=False, get_version=None, search="rustc", all=False
        )
        mock_verify.return_value = True

        main()

        mock_verify.assert_called_once()
        mock_exit.assert_not_called()

    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("scripts.tooling.ToolChecker.verify")
    @unittest.mock.patch("sys.exit")
    def test_main_search_verification_fails_exits(
        self,
        mock_exit: unittest.mock.MagicMock,
        mock_verify: unittest.mock.MagicMock,
        mock_parse: unittest.mock.MagicMock,
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=False, get_version=None, search="rustc", all=False
        )
        mock_verify.return_value = False

        main()

        mock_exit.assert_called_once_with(1)

    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("scripts.tooling.ToolChecker.verify")
    @unittest.mock.patch("sys.exit")
    def test_main_all_success_pipeline(
        self,
        mock_exit: unittest.mock.MagicMock,
        mock_verify: unittest.mock.MagicMock,
        mock_parse: unittest.mock.MagicMock,
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=False, get_version=None, search=None, all=True
        )
        mock_verify.return_value = True

        main()

        self.assertEqual(mock_verify.call_count, len(TOOL_TABLE))
        mock_exit.assert_not_called()

    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("scripts.tooling.ToolChecker.verify")
    @unittest.mock.patch("sys.exit")
    def test_main_all_pipeline_one_tool_fails_exits(
        self,
        mock_exit: unittest.mock.MagicMock,
        mock_verify: unittest.mock.MagicMock,
        mock_parse: unittest.mock.MagicMock,
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=False, get_version=None, search=None, all=True
        )
        # O primeiro retorna True, o segundo falha retornando False
        mock_verify.side_effect = [True, False] + [True] * (len(TOOL_TABLE) - 2)

        main()

        mock_exit.assert_called_once_with(1)
