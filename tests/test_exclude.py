import torf

import pytest


@pytest.fixture
def content(tmp_path):
    content = tmp_path / 'content' ; content.mkdir()
    for i in range(1, 5):
        ext = 'jpg' if i % 2 == 0 else 'txt'
        (content / f'file{i}.{ext}').write_text('<data>')
    subdir = content / 'subdir' ; subdir.mkdir()
    for i in range(1, 4):
        ext = 'jpg' if i % 2 == 0 else 'pdf'
        (subdir / f'file{i}.{ext}').write_text('<data>')
    return content

def test_exclude_globs_with_singlefile_torrent_and_existing_path(create_torrent, content):
    torrent = create_torrent(path=content / 'file1.txt')
    assert torrent.metainfo['info']['name'] == 'file1.txt'
    assert torrent.metainfo['info']['length'] == 6
    torrent.exclude_globs.append('*.txt')
    assert torrent.metainfo['info']['name'] == 'file1.txt'
    assert 'length' not in torrent.metainfo['info']

def test_exclude_globs_with_singlefile_torrent_and_nonexisting_path(create_torrent):
    torrent = create_torrent()
    torrent.metainfo['info']['name'] = 'foo.txt'
    torrent.metainfo['info']['length'] = 123
    torrent.exclude_globs.append('foo.*')
    assert torrent.metainfo['info']['name'] == 'foo.txt'
    assert 'length' not in torrent.metainfo['info']

def test_exclude_globs_with_multifile_torrent_and_existing_path(create_torrent, content):
    torrent = create_torrent(path=content)
    assert torrent.metainfo['info']['files'] == [{'length': 6, 'path': ['file1.txt']},
                                                 {'length': 6, 'path': ['file2.jpg']},
                                                 {'length': 6, 'path': ['file3.txt']},
                                                 {'length': 6, 'path': ['file4.jpg']},
                                                 {'length': 6, 'path': ['subdir', 'file1.pdf']},
                                                 {'length': 6, 'path': ['subdir', 'file2.jpg']},
                                                 {'length': 6, 'path': ['subdir', 'file3.pdf']}]
    torrent.exclude_globs.extend(('*1.???', 'subdir/*.pdf'))
    assert torrent.metainfo['info']['files'] == [{'length': 6, 'path': ['file2.jpg']},
                                                 {'length': 6, 'path': ['file3.txt']},
                                                 {'length': 6, 'path': ['file4.jpg']},
                                                 {'length': 6, 'path': ['subdir', 'file2.jpg']}]

def test_exclude_globs_with_multifile_torrent_and_nonexisting_path(create_torrent):
    torrent = create_torrent()
    torrent.metainfo['info']['name'] = 'content'
    torrent.metainfo['info']['files'] = [{'length': 6, 'path': ['file1.txt']},
                                         {'length': 6, 'path': ['file2.jpg']},
                                         {'length': 6, 'path': ['file3.txt']},
                                         {'length': 6, 'path': ['subdir', 'file1.pdf']},
                                         {'length': 6, 'path': ['subdir', 'file2.jpg']},
                                         {'length': 6, 'path': ['subdir', 'file3.pdf']}]
    torrent.exclude_globs.extend(('*.jpg', 'subdir/*3.*'))
    assert torrent.metainfo['info']['files'] == [{'length': 6, 'path': ['file1.txt']},
                                                 {'length': 6, 'path': ['file3.txt']},
                                                 {'length': 6, 'path': ['subdir', 'file1.pdf']}]