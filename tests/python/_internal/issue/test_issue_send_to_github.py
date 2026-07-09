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

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

import unittest
import unittest.mock
import subprocess
import typing

from scripts._internal.issue import Issue, IssueType


class TestIssueSendToGithub(unittest.TestCase):
    def setUp(self) -> None:
        self.issue: Issue = Issue(IssueType.BugReport, "GitHub Send Bug")

        self.issue.set_field("description", "Crash on launch")
        self.issue.set_field("environment-info", "Target: Morello")

    def test_send_to_github_validation_failure(self) -> None:
        invalid_issue: Issue = Issue(IssueType.BugReport, "Invalid")
        success: bool = invalid_issue.send_to_github()

        self.assertFalse(success)

    @unittest.mock.patch("subprocess.run")
    @unittest.mock.patch("os.path.exists")
    @unittest.mock.patch("os.remove")
    def test_send_to_github_happy_path(
        self,
        mock_remove: unittest.mock.MagicMock,
        mock_exists: unittest.mock.MagicMock,
        mock_run: unittest.mock.MagicMock,
    ) -> None:
        mock_process: unittest.mock.MagicMock = unittest.mock.MagicMock()

        mock_process.stdout = "https://github.com/harpylang/aelo/issues/0xdeadc0de\n"
        mock_run.return_value = mock_process
        mock_exists.return_value = True

        success: bool = self.issue.send_to_github()

        self.assertTrue(success)
        mock_run.assert_called_once()

        called_arguments: typing.List[str] = mock_run.call_args[0][0]

        self.assertEqual(called_arguments[0], "gh")
        self.assertEqual(called_arguments[1], "issue")
        self.assertEqual(called_arguments[2], "create")
        self.assertIn("--title", called_arguments)
        self.assertIn("GitHub Send Bug", called_arguments)
        self.assertIn("--label", called_arguments)
        self.assertIn("bug", called_arguments)

        mock_remove.assert_called_once()

    @unittest.mock.patch("subprocess.run")
    def test_send_to_github_cli_returns_non_zero_exit_code(
        self, mock_run: unittest.mock.MagicMock
    ) -> None:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="gh", stderr="GraphQL Error: Repository not found"
        )

        success: bool = self.issue.send_to_github()

        self.assertFalse(success)

    @unittest.mock.patch("subprocess.run")
    def test_send_to_github_binary_not_found_in_path(
        self, mock_run: unittest.mock.MagicMock
    ) -> None:
        mock_run.side_effect = FileNotFoundError()

        success: bool = self.issue.send_to_github()

        self.assertFalse(success)

    @unittest.mock.patch("subprocess.run")
    @unittest.mock.patch("os.path.exists")
    @unittest.mock.patch("os.remove")
    def test_send_to_github_ensures_cleanup_on_exception(
        self,
        mock_remove: unittest.mock.MagicMock,
        mock_exists: unittest.mock.MagicMock,
        mock_run: unittest.mock.MagicMock,
    ) -> None:
        mock_run.side_effect = RuntimeError("Unexpected OS failure")
        mock_exists.return_value = True

        with self.assertRaises(Exception):
            self.issue.send_to_github()

        mock_remove.assert_called_once()
