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

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts._internal.issue import (
    Issue,
    IssueType,
    _BUG_FIELDS,
    _FEATURE_FIELDS,
    _BUG_REPORT_LABELS,
    _FEATURE_REQUEST_LABELS,
)


class TestIssueInitialization(unittest.TestCase):
    def test_init_bug_report_happy_path(self) -> None:
        issue: Issue = Issue(IssueType.BugReport, "Fix: Segfault on x86-64")

        self.assertEqual(issue.issue_type, IssueType.BugReport)
        self.assertEqual(issue.title, "Fix: Segfault on x86-64")
        self.assertEqual(issue.labels, _BUG_REPORT_LABELS)
        self.assertEqual(issue._expected_fields, _BUG_FIELDS)
        self.assertEqual(issue.fields, {})

    def test_init_feature_request_happy_path(self) -> None:
        issue: Issue = Issue(IssueType.FeatureRequest, "Feat: Add Morello pipeline")

        self.assertEqual(issue.issue_type, IssueType.FeatureRequest)
        self.assertEqual(issue.title, "Feat: Add Morello pipeline")
        self.assertEqual(issue.labels, _FEATURE_REQUEST_LABELS)
        self.assertEqual(issue._expected_fields, _FEATURE_FIELDS)
        self.assertEqual(issue.fields, {})

    def test_init_error_empty_title(self) -> None:
        with self.assertRaises(ValueError) as context:
            Issue(IssueType.BugReport, "")

        self.assertEqual(str(context.exception), "The issue title cannot be blank.")

    def test_init_error_whitespace_only_title(self) -> None:
        with self.assertRaises(ValueError) as context:
            Issue(IssueType.FeatureRequest, "     \n\t  ")

        self.assertEqual(str(context.exception), "The issue title cannot be blank.")

    def test_init_with_weird_characters_in_title(self) -> None:
        weird_title: str = "🛑 Bug \\x00; drop csv trash; -- \n"
        issue: Issue = Issue(IssueType.BugReport, weird_title)

        self.assertEqual(issue.title, weird_title)
