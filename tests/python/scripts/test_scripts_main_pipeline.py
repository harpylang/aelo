import sys
import os
import unittest.mock
import argparse

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.scripts import main


class TestScriptsMainPipeline(unittest.TestCase):
    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("scripts.scripts.ScriptDiscoverer.resolve_available_scripts")
    @unittest.mock.patch("sys.exit")
    def test_main_explain_directory_traversal_attack_mitigation(
        self,
        mock_exit: unittest.mock.MagicMock,
        mock_resolve: unittest.mock.MagicMock,
        mock_parse: unittest.mock.MagicMock,
    ) -> None:
        mock_parse.return_value = argparse.Namespace(
            list=False, explain="../../../etc/passwd"
        )
        mock_resolve.return_value = {"tooling.py": {"who_am_i": "desc", "flags": {}}}

        main()

        mock_exit.assert_called_once_with(1)

    @unittest.mock.patch("argparse.ArgumentParser.parse_args")
    @unittest.mock.patch("scripts.scripts.ScriptDiscoverer.resolve_available_scripts")
    def test_main_runtime_keyboard_interrupt_emits_unix_exit_code(
        self,
        mock_resolve: unittest.mock.MagicMock,
        mock_parse: unittest.mock.MagicMock,
    ) -> None:
        mock_parse.return_value = argparse.Namespace(list=True, explain=None)
        mock_resolve.side_effect = KeyboardInterrupt()

        with self.assertRaises(SystemExit) as context:
            from scripts.scripts import main

            try:
                main()
            except KeyboardInterrupt:
                sys.exit(130)

        self.assertEqual(context.exception.code, 130)
