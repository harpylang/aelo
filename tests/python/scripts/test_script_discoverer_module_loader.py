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
import typing
import types

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.scripts import ScriptDiscoverer


class TestScriptDiscovererModuleLoader(unittest.TestCase):
    @unittest.mock.patch("importlib.util.spec_from_file_location")
    def test_load_module_raises_syntax_error_returns_none_safely(
        self, mock_spec_from_file: unittest.mock.MagicMock
    ) -> None:
        mock_spec: unittest.mock.MagicMock = unittest.mock.MagicMock()
        mock_spec.loader.exec_module.side_effect = SyntaxError(
            "Invalid python syntax inside script"
        )

        mock_spec_from_file.return_value = mock_spec

        discoverer: ScriptDiscoverer = ScriptDiscoverer("dummy_path")
        result: typing.Optional[types.ModuleType] = discoverer._load_module_from_path(
            "corrupted", "corrupted.py"
        )

        self.assertIsNone(result)

    @unittest.mock.patch("importlib.util.spec_from_file_location")
    def test_load_module_system_permission_denied_returns_none(
        self, mock_spec_from_file: unittest.mock.MagicMock
    ) -> None:
        mock_spec_from_file.side_effect = PermissionError("OS Denied Access")

        discoverer: ScriptDiscoverer = ScriptDiscoverer("dummy_path")
        result: typing.Optional[types.ModuleType] = discoverer._load_module_from_path(
            "corrupted", "corrupted.py"
        )

        self.assertIsNone(result)
