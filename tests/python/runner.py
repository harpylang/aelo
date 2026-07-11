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
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tests.python._internal.issue.test_issue_initialization import (
    TestIssueInitialization,
)
from tests.python._internal.issue.test_issue_set_field import TestIssueSetField
from tests.python._internal.issue.test_issue_generate_markdown import (
    TestIssueGenerateMarkdown,
)
from tests.python._internal.issue.test_issue_save_local import TestIssueSaveLocal
from tests.python._internal.issue.test_issue_send_to_github import TestIssueSendToGithub
from tests.python.tooling.test_tool_checker_initialization import (
    TestToolCheckerInitialization,
)
from tests.python.tooling.test_tool_checker_get_first_line import (
    TestToolCheckerGetFirstLine,
)
from tests.python.tooling.test_tool_checker_verify import TestToolCheckerVerify
from tests.python.tooling.test_tool_checker_main_pipeline import (
    TestToolCheckerMainPipeline,
)
from tests.python.scripts.test_script_discoverer_module_loader import (
    TestScriptDiscovererModuleLoader,
)
from tests.python.scripts.test_script_discoverer_resolution import (
    TestScriptDiscovererResolution,
)
from tests.python.scripts.test_discovery_presenter import (
    TestDiscoveryPresenter,
)
from tests.python.scripts.test_scripts_main_pipeline import TestScriptsMainPipeline

if __name__ == "__main__":
    unittest.main()
