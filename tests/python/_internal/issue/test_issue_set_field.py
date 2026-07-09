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

from scripts._internal.issue import Issue, IssueType, _BUG_FIELDS, _FEATURE_FIELDS


class TestIssueSetField(unittest.TestCase):
    def setUp(self) -> None:
        self.bug_issue: Issue = Issue(IssueType.BugReport, "Bug Title")
        self.feat_issue: Issue = Issue(IssueType.FeatureRequest, "Feat Title")

    def test_set_field_bug_allowed_fields(self) -> None:
        for field in _BUG_FIELDS.keys():
            with self.subTest(field=field):
                self.bug_issue.set_field(field, f"Content for {field}")
                self.assertEqual(self.bug_issue.fields[field], f"Content for {field}")

    def test_set_field_feature_allowed_fields(self) -> None:
        for field in _FEATURE_FIELDS.keys():
            with self.subTest(field=field):
                self.feat_issue.set_field(field, f"Content for {field}")
                self.assertEqual(self.feat_issue.fields[field], f"Content for {field}")

    def test_set_field_strips_whitespace(self) -> None:
        self.bug_issue.set_field("description", "   \n  Text with spaces around  \t ")
        self.assertEqual(
            self.bug_issue.fields["description"], "Text with spaces around"
        )

    def test_set_field_invalid_for_bug_type(self) -> None:
        with self.assertRaises(KeyError) as context:
            self.bug_issue.set_field("poc", "fn main() {}")

        self.assertIn(
            "field is invalid for the Bug Report type", str(context.exception)
        )

    def test_set_field_invalid_for_feature_type(self) -> None:
        with self.assertRaises(KeyError) as context:
            self.feat_issue.set_field("compiler-output", "panic!")

        self.assertIn(
            "field is invalid for the Feature Request type", str(context.exception)
        )

    def test_set_field_completely_random_key(self) -> None:
        with self.assertRaises(KeyError):
            self.bug_issue.set_field("random_garbage_key_123", "value")
