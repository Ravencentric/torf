import errno
import os

from . import _errors as error
from . import _stream as stream


class find_torrent_files:
    def __init__(self, *paths):
        self._paths = paths
        self._counter = 0

    def __iter__(self):
        """
        Find torrent files recursively beneath each path in `paths`

        Each list item is a 4-tuple that contains the torrent file path or ``None``,
        a counter that increments for each torrent file, the total number of torrent
        files and an exception or ``None``.
        """
        for path in self._paths:
            yield from self._find(path)

    def _find(self, path):
        if os.path.isdir(path):
            try:
                for name in os.listdir(path):
                    subpath = os.sep.join((str(path), name))
                    yield from self._find(subpath)
            except OSError as e:
                yield None, self._counter, error.ReadError(e.errno, str(path))

        elif os.path.basename(path).lower().endswith('.torrent'):
            self._counter += 1
            yield path, self._counter, None

        elif not os.path.exists(path):
            yield None, self._counter, error.ReadError(errno.ENOENT, str(path))

    @property
    def total(self):
        """Total number of torrents beneath all paths"""
        # Get a sequence of all torrents without changing self._counter.
        items = tuple(type(self)(*self._paths))
        if items:
            # Last item should contain the number of torrents found.
            return items[-1][1]
        else:
            return 0


def is_file_match(torrent, candidate):
    """
    Whether `torrent` contains the same files as `candidate`

    Both arugments are :class:`~.Torrent` objects.

    The torrents match if they both share the same ``name`` and ``files`` or
    ``length`` fields in their :attr:`~.Torrent.metainfo`.

    This is a quick check that doesn't require any system calls.
    """
    # Compare relative file paths and file sizes.
    # Order is important.
    torrent_info, candidate_info = torrent.metainfo['info'], candidate.metainfo['info']
    torrent_id = _get_filepaths_and_sizes(torrent_info)
    candidate_id = _get_filepaths_and_sizes(candidate_info)
    return torrent_id == candidate_id

def _get_filepaths_and_sizes(info):
    name = info['name']

    # Singlefile torrent
    length = info.get('length', None)
    if length:
        return [(name, length)]

    # Multifile torrent
    files = info.get('files', None)
    if files:
        files_and_sizes = []
        for file in files:
            files_and_sizes.append((
                os.sep.join((name, *file['path'])),
                file['length'],
            ))
        return sorted(files_and_sizes)

    else:
        raise RuntimeError(f'Unable to find file sizes in {info!r}')


def is_content_match(torrent, candidate):
    """
    Whether `torrent` contains the same files as `candidate`

    Both arugments are :class:`~.Torrent` objects.

    If a `candidate` matches, a few piece hashes from each file are compared to
    the corresponding hashes from `candidate` to detect files name/size
    collisions.

    This is relatively slow and should only be used after :func:`is_file_match`
    returned `True`.
    """
    if not torrent.path:
        raise RuntimeError(f'Torrent does not have a file system path: {torrent!r}')

    # Compare some piece hashes for each file
    with stream.TorrentFileStream(candidate, content_path=torrent.path) as tfs:
        check_piece_indexes = set()
        for file in candidate.files:
            all_file_piece_indexes = tfs.get_piece_indexes_of_file(file)
            middle_piece_index = int(len(all_file_piece_indexes) / 2)
            some_file_piece_indexes = (
                all_file_piece_indexes[:1]
                + [middle_piece_index]
                + all_file_piece_indexes[-1:]
            )
            check_piece_indexes.update(some_file_piece_indexes)

        for piece_index in sorted(check_piece_indexes):
            if not tfs.verify_piece(piece_index):
                return False
    return True


def copy(from_torrent, to_torrent):
    """
    """
    source_info = from_torrent.metainfo['info']
    to_torrent.metainfo['info']['pieces'] = source_info['pieces']
    to_torrent.metainfo['info']['piece length'] = source_info['piece length']