"""Static Galaxy file sources - ftp and libraries."""

from typing import (
    cast,
    Optional,
)

from .posix import PosixFilesSource
from .posix import PosixFilesSourceProperties
from typing_extensions import Unpack

class UserFtpFilesSource(PosixFilesSource):
    plugin_type = "gxftp"

    def __init__(self, label="FTP Directory", doc="Galaxy User's FTP Directory", root="${user.ftp_dir}", **kwd):
        posix_kwds = dict(
            id="_ftp",
            root=root,
            label=label,
            doc=doc,
            writable=True,
        )
        posix_kwds.update(kwd)
        if "delete_on_realize" not in posix_kwds:
            file_sources_config = kwd["file_sources_config"]
            posix_kwds["delete_on_realize"] = file_sources_config.ftp_upload_purge
        super().__init__(**posix_kwds)

    def get_prefix(self):
        return None

    def get_scheme(self):
        return "gxftp"


class LibraryImportFilesSource(PosixFilesSource):
    plugin_type = "gximport"

    def __init__(
        self,
        label="Library Import Directory",
        doc="Galaxy's library import directory",
        root="${config.library_import_dir}",
        **kwd,
    ):
        posix_kwds = dict(
            id="_import",
            root=root,
            label=label,
            doc=doc,
        )
        posix_kwds.update(kwd)
        super().__init__(**posix_kwds)

    def get_prefix(self):
        return None

    def get_scheme(self):
        return "gximport"


class UserLibraryImportFilesSource(PosixFilesSource):
    plugin_type = "gxuserimport"

    def __init__(
        self,
        label="Library User Import Directory",
        doc="Galaxy's user library import directory",
        root="${config.user_library_import_dir}/${user.email}",
        **kwd,
    ):
        posix_kwds = dict(
            id="_userimport",
            root=root,
            label=label,
            doc=doc,
        )
        posix_kwds.update(kwd)
        super().__init__(**posix_kwds)

    def get_prefix(self):
        return None

    def get_scheme(self):
        return "gxuserimport"


class UserHomeFilesSource(PosixFilesSource):
    plugin_type = "gxuserhome"

    def __init__(self, **kwd: Unpack[PosixFilesSourceProperties]):
        posix_kwds: PosixFilesSourceProperties = dict(
            id="_userhome",
            root="/fp/homes01/u01/${user.username}/",
            label="User Home Directory",
            doc="Galaxy User's Home Directory",
            writable=True,
        )
        posix_kwds.update(kwd)
        super().__init__(**posix_kwds)

    def get_prefix(self) -> Optional[str]:
        return None

    def get_scheme(self) -> str:
        return "gxuserhome"


class UserProjectFilesSource(PosixFilesSource):
    plugin_type = "gxuserprojects"

    def __init__(self, **kwd: Unpack[PosixFilesSourceProperties]):
        posix_kwds: PosixFilesSourceProperties = dict(
            id="_userprojects",
            root="/fp/projects01/",
            label="User Projects Directory",
            doc="Galaxy User's Projects Directory",
            writable=True,
        )
        posix_kwds.update(kwd)
        super().__init__(**posix_kwds)

    def get_prefix(self) -> Optional[str]:
        return None

    def get_scheme(self) -> str:
        return "gxuserprojects"


__all__ = ("UserFtpFilesSource", "LibraryImportFilesSource", "UserLibraryImportFilesSource", "UserHomeFilesSource", "UserProjectFilesSource")
