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
import importlib.util
import os
import typing
import types


class ScriptDiscoverer(object):
    """
    Handles dynamic scanning, isolation, and metadata reflection of internal
    repository pipeline scripts.
    """

    def __init__(self, directory: str) -> None:
        self.directory: str = os.path.abspath(directory)
        self.target_suffix: str = ".py"
        self.ignored_files: typing.Set[str] = {"scripts.py", "__init__.py"}

    def _load_module_from_path(
        self, module_name: str, file_path: str
    ) -> typing.Optional[types.ModuleType]:
        """
        Dynamically binds and injects a script file context into the Python runtime scope.
        """
        try:
            spec: typing.Optional[importlib.machinery.ModuleSpec] = (
                importlib.util.spec_from_file_location(module_name, file_path)
            )

            if spec is None or spec.loader is None:
                return None

            module: types.ModuleType = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return module
        except Exception:
            return None
