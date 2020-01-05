import torf

import pytest
import os
import random
import string
from types import SimpleNamespace
import time
from collections import OrderedDict, abc
import contextlib
import functools
import math

@contextlib.contextmanager
def _random_seed(seed):
    random.seed(seed)
    yield
    random.seed()

@pytest.fixture
def random_seed():
    return functools.partial(_random_seed)


TESTDIR_BASE = 'test_files'

letters = string.ascii_letters + string.digits + '    ²öäåóíéëúæøœœï©®¹³¤óíïœ®øï'
def _randstr():
    length = random.randint(10, 20)
    return ''.join(random.choice(letters) for _ in range(length))


def _mktempdir(tmpdir_factory, subdir=None):
    path = tmpdir_factory.mktemp(TESTDIR_BASE, numbered=True)
    if subdir is None:
        subdir = ''
    subdir += ':' + _randstr()
    return path.mkdir(subdir)


def _generate_random_file(dirpath, filename=None, hidden=False):
    filesize = random.randint(1e3, 1e6)
    filecontent = bytearray(random.getrandbits(8) for _ in range(filesize))
    if filename is None:
        filename = ''
    filename += ':' + _randstr()
    if hidden:
        filename = '.' + filename
    filepath = os.path.join(TESTDIR_BASE, dirpath, filename)
    with open(filepath, 'wb') as f:
        f.write(filecontent)
    assert os.path.getsize(filepath) == filesize
    return filepath

def _generate_empty_file(dirpath, filename=None, hidden=False):
    if filename is None:
        filename = ''
    filename += ':' + _randstr()
    if hidden:
        filename = '.' + filename
    filepath = os.path.join(TESTDIR_BASE, dirpath, filename)
    with open(filepath, 'w') as f:
        f.write('')
    assert os.path.getsize(filepath) == 0
    return str(filepath)



@pytest.fixture
def valid_singlefile_metainfo():
    return OrderedDict([
        (b'announce', b'http://localhost'),
        (b'comment', b'This is a test comment'),
        (b'created by', b'The creator'),
        (b'creation date', 1513440897),
        (b'info', OrderedDict([
            (b'length', 500000),
            (b'name', b'Torrent for testing'),
            (b'piece length', 32768),
            (b'pieces', b'\x00' * 20 * 16),
            (b'private', 1)
        ]))
    ])

@pytest.fixture
def valid_multifile_metainfo():
    return OrderedDict([
        (b'announce', b'http://localhost'),
        (b'comment', b'This is a test comment'),
        (b'created by', b'The creator'),
        (b'creation date', 1513440897),
        (b'info', OrderedDict([
            (b'files', [{b'length': 123, b'path': [b'A file']},
                        {b'length': 456, b'path': [b'Another file']},
                        {b'length': 789, b'path': [b'A', b'third', b'file in a subdir']}]),
            (b'name', b'Torrent for testing'),
            (b'piece length', 32768),
            (b'pieces', b'\x00' * 20),
            (b'private', 1)
        ]))
    ])


@pytest.fixture
def generate_random_Torrent_args():
    def f():
        args = {
            'exclude' : random.choice(([], ['no*matches'])),
            'trackers' : random.choice(([],
                                        ['http://localhost:123/announce'],
                                        ['http://localhost:123/announce', 'http://localhost:456/announce'],
                                        [['http://localhost:123/announce', 'http://localhost:456/announce'],
                                         ['http://localhost:789/announce', 'http://localhost:111/announce']])),
            'webseeds' : random.choice(([],
                                        ['http://localhost:123/webseed'],
                                        ['http://localhost:123/webseed', 'http://localhost:456/webseed'])),
            'httpseeds' : random.choice(([],
                                         ['http://localhost:123/httpseed'],
                                         ['http://localhost:123/httpseed', 'http://localhost:456/httpseed'])),
            'comment'       : _randstr(),
            'creation_date' : random.randint(0, int(time.time())),
            'created_by'    : _randstr(),
            'source'        : _randstr(),
            'piece_size'    : random.choice((None, 2**14, 2**15, 2**16, 2**17, 2**18, 2**19, 2**20)),
        }

        # Remove random items from args
        return dict(random.sample(tuple(args.items()), random.randint(0, len(args))))
    return f

@pytest.fixture
def mktorrent(generate_random_Torrent_args):
    def _mktorrent(**kwargs):
        return torf.Torrent(**{**generate_random_Torrent_args(),
                               **kwargs})
    return _mktorrent

@pytest.fixture(scope='session')
def singlefile_content_empty(tmpdir_factory):
    content_path = _mktempdir(tmpdir_factory)
    filepath = _generate_empty_file(content_path, filename='empty Ꝼile')
    return SimpleNamespace(path=str(filepath))

@pytest.fixture(scope='session')
def multifile_content_empty(tmpdir_factory):
    content_path = _mktempdir(tmpdir_factory, subdir='ęmpty directorý')
    for _ in range(2):
        _generate_empty_file(content_path)
    _generate_empty_file(content_path, hidden=True)
    return SimpleNamespace(path=str(content_path))


@pytest.fixture(scope='session')
def singlefile_content(tmpdir_factory):
    random.seed(0)  # Make sure random file names and content are identical every time
    content_path = _mktempdir(tmpdir_factory)
    filepath = _generate_random_file(content_path, filename='sinģle fíle')
    random.seed()  # Re-enable randomness

    exp_pieces = b'\xc8\xfa\x0fV\x95\xecl\x97t\xb2v\x84S\x98{\x92[ \x13\xe5\x04\xef-\xb0;sF\xc2\x93W\xcf\xc6X\x14\x9b]_r\xfb\x80\'}\xe5\xc4\x05\xdct\xb5^\xe9\x7f0b|\xc9\xf1\x9d\xd7G\x06 ,l8m\x01\xbf2\xf6:\x03r-\x8d\x1f,\x8bk:\xad\xdbN\xa2V\x96/\xf2@w\xa5\x98\xf8\t3fU\x13;\x90\xc0F\xe3[\x15\xea\x8f\x92\xcdN:\xc1\x0fG\x9b\xeb\xd9\x93A\xca\xa7L\xd2\x9ef|\xddd\xd4\x94.f\xee\xea3\xa8\x04|\xe9h\xa7\xa1t\xa2\xb5\xb3*\x89\xf7\x14\xdf\x16M/\xc6\xa5\x85\xdaF\xca\xa7?\x9d\xe1zd\xc8\xe1\x1d\x1epC\x06+\xe1Q\x0fi\x9fv\x19\xa2(\xd0\x90\xb3\xb0\xcf\xa9\x1cy\xf0\x96\x17\n\x05\xa5*IZJ\x8c\xbb\x87\xdd\xed|d.\xf0\xb9\xfe\x00\xa6\nufY\x18\xe35\xee\xdf\xa6D\xed<\xc5W\x0fa\x80\xc6}\xdd\xf4\xbd\xc1:\xe3\xda\nj\xbag\x93\xd0\xdc\xbd\xb8\xfb\xc2\x99\x9a/&\x1d\xf3\xe9\xa3,\x9b>\'\xa5\xaa~\xabb\x81\x88\x80^\xddd\xc7\xea\x83n\x05%\x8f4\x8a\x82\xe2\xff[\xab\xa8\x92\x1f\xaarG\xc5\x00\xcae\x9e\x93\xc4\x9015\x02\xe7\x8a\xb1I\xa6\x16DF\x8a\x0b\xeb\xca@\th?WL\xe0Vf\xc9X>##?t\x08\xdf[\xac\x16\x7f\xe9\x1a\xc4\x11\x0c\xc9\xac?\xded\xed\xf5\x1b\xd0Qq\x90_\x88]\xbf\xb7\xbc\xf5\x8et4f<\x14\xb6\x98\xbb\xdd0H\x14\xfaZ\xc1\x07l3\xd6""l\x99X@\xb7\x9c\xbc/h\xe9\xc0\x83\x0e\xfb\x91\x83\xdf\x1d+\xf6\xd1_\xb8\x04\xdd\xb8\x05\'\x1c\x1b\x94\x1cl\x9a_[An:\xcdw\xe8\xfb\xbf\xb9\x82olQ6<U\r\x9e0/\x89\xc6\xe4\x9cl<\xd5\xf9\xca\x96\x01\xd5\xc3\x1dk\x1b1\xc2X\xe9\x164\x9d\x05\x19\x85c\x0e\x847b\xdb[\xa8\x8e\xc1\x04,\x1c\xc2\x0e\x85`+3\xb1\xe6\xac&F\xb9\xf6\x0e\\\x1fS\xbd\xed\xc6l\x89\x18\x8eI?\x9aqR1&k\x14ce i\xb4;C\xfe\x1dh\xe4\xd3>\xa4\x15\x9f\xd2c#\x1b\x9a\xb6\x84\x88@\x89\xdd\x01\x18H\xbce\rK1aS\xd8\xb8\xffD\x9f\x89\xd4\xb59y7\xff\x8b\xc1\xc3\t\xdd\x9e\xa6\xa7\x02:\xa5\xea<\xb9\x95\xd7ePU~\xbc\x16\x9a\x0f\xb1h\xad4\xfa\x18yv\x95\x96\x0cRo\x88\xe6L\x08\xfd\x94gh\x92\'w\xb3\xd1BCqC\x12_\x1f\x92\xfc\xc6\xfd\t\xcd\xab\xe0\xbd\xcc\x06\xf9\xa7\xb1e\xa9\xbe\x0c\x8d\xfcI\x00\x0e\xd7\xbe\x0c&\xf2\xc5\xa5Yl\xf8\xc0\x8e.\x97\x0c\xd5zp~8\xc0g\xa6C\x16\xd0v\x1e\xa1\xa37\xceM[\xd6\x18\xc6\xa5\xc9\xbc\x11\x99\xc4\xe9\x0f9\xab\x98\x01\xaf\xe22\n_\x83\x9b\xdegG\xb4#\xd6\x17\xf1z4\x11v\xef\xcf!\x03\xdc\x14_\x9e;\'\xdckvHh\xd5x\xf48\xdaFa\xae\x02\xf0\x16| \xa3\x97\xe5\xed\xf6\x11$\xe4\xacb\xaf\x8a\x07fH\x96\x00\x00\x98\x87(\x97\xcd!\xff\xf8a\x02\xc4\xca\xff\xef\xe1P\x01_\x9b\x9b\x83:\x7f\xdd\x92\xfb\xe9\x94\xc3SEWh\x18\xb3\x9c\xd8\xf9M\x1d!\xd25\xcb'

    exp_metainfo = {'announce'      : 'http://localhost:123',
                    'created by'    : 'mktorrent 1.0',
                    'creation date' : 1513522263,
                    'info': {'name'         : os.path.basename(filepath),
                             'piece length' : 2**14,
                             'pieces'       : exp_pieces,
                             'length'       : os.path.getsize(filepath)}}

    exp_attrs = SimpleNamespace(path=str(filepath),
                                infohash='7febf5a5a6e6bac79df2eb4340a63009109fecd5',
                                infohash_base32=b'P7V7LJNG425MPHPS5NBUBJRQBEIJ73GV',
                                size=os.path.getsize(filepath),
                                pieces=math.ceil(os.path.getsize(filepath) / exp_metainfo['info']['piece length']))

    return SimpleNamespace(path=exp_attrs.path,
                           exp_metainfo=exp_metainfo,
                           exp_attrs=exp_attrs)

@pytest.fixture(scope='session')
def multifile_content(tmpdir_factory):
    random.seed(0)  # Make sure random file names and content are identical every time
    content_path = _mktempdir(tmpdir_factory, subdir='Multifile torrent')
    for n in range(2):
        _generate_random_file(content_path, filename=f'File {n}')
    subdir_path = content_path.mkdir('subdir')
    _generate_random_file(subdir_path, filename='File in subdir')
    random.seed()  # Re-enable randomness

    exp_files=[{'length': 649406, 'path': ['File 0:JïYR WN93kœ']},
               {'length': 199019, 'path': ['File 1:aä¤ELYœPTófsdtœe©í']},
               {'length': 333198, 'path': ['subdir', 'File in subdir:F³bæ¹inRf ¤RTggTSóz']}]

    exp_pieces = b'BHG\xb7[\xdf\xaa\xf1\xf3<\xd3C\xeb\xab\xecjZ3\x06\x97\x0c*\xb7G3\xc5G\xe3\x0e\xdb\x96\xf1V-D@\xdd\t\xcf\x88GB\xa3\xdf\xdd\x1fxCQd=8\xc7\x81\x96\x0f\xaf(-\xe6FB\x10\xd1\xbf\xad\x88\x1d\x1d\xc3\x03\xb3\x08\xc0\xe0\x0b\x8a\\\x19\xdf\xed\x03\xdb\x7f\x17o3uI\xef(\n\x80\xdbbF\x91\xd90%\xe6\xfay\x16O\x06n-\xad\x1b\x06\x98SJ:\xf3d64=\xf2\xc8\t~\xbf\x08\xdd\x1am\xae\xbe\xed\xf1\x94\x8f\x08X5\x85\x0e\xa2wM\xa3\x14K,\x9dO\xd2n\xb6\x98\x16\xe6s\xa2\t\t0\xa4\x05\xd1\x95*\x02S\xf1y\x14\xf3G\xf8]eUD\x81`_m\xeaW\x0e\xb5\xc1r\n2\xf0Qo\r\xba\x07\xb3!Vr\xacn\x06\xeb\x1a\xce9\x0e\xa1j\xb1\xf9\xc9\xe0J\xda\xa2v\xe4d\'\x8cf5!Z\xd4g[\x9b\xf4fr\xc2\xee\xb3;\xe7\xe3\x9e\xe0\x06}\xe3\xe6\xc9\xa2\xf9t\x0c\xe1\xf5h\xfe\x13\xf5\xe4\xaa\xd6\x01\x91\xe3\xb7\xb2x\xe1\xd7\xb1o\x10\xe7\xd6\xd2b%d\xae\xe4\x8a\x910\x1b\xb6\x1b\xda\x944\xce\t\xd6\xdf%*n\x05\x16\xd9\x8ft\xed\xb7\xeb"\xfd\xb0Q+t\xbdy|\xed\x01<\xb9\xd2"@\xa2\x85\xa6\x8a\x1d|\x89Z\x13w\xdb\xe7\xdd\xe2\xcey\x00R\xa3[k\x8e\xde\x98""\xfd\xc0]{\xc2H\n%8 \xd3\x01\xd2i\x9f\xf0n\x05^\x90\xbc\xcb\xb5\x8a\xde$\xef\xbd\x02\x83\xe2m\x93:K\x10\xfc\xc7\xb6\xf5\xcf\x9a!\xe06as\x8b`\xda\x12\xf3\x13\xc73\xbf\xad\xcc\x86V\x14Tm5\xb4&C\x8c\x89\x17*\x83A\xc9o\x04\x9e\xe8p\x0e\x1fIx\xf2\\\xc9\xca\x8c\xd1\xfb#\x08\xeb\x0eq\xf3\r].\xacfH\xea\xc1q\xcc\x1bw\xe3\xe6-o\xf6Hb\x85\xc7\xefk\xa5\xc7\xea\xd1\xa0\xb4h\xb7\xdd\x9fe/\x98g\xef\xea6\x02f\x1a\xc1\xe5N\xf3\x10\x04\xe0\x004!\xca\x81\xa4\xfc\x12\xceS\x9c\x8e,L82\xbb\x83\x8f\x95#\x93\xe2\x83\xaf\xfd\xe9T|@oy\x07x[rp;\x89\xe0a\xdc\xee\xcekW\xaf/\xe8g\x19 \x1b\xd8\x8e.\xc2B\xaf\x94\xd9\xa5X\x94\x85\xc0\xa8\x047\xa6\xcc\xa0i( \x04\x98\xce>A\x87\x92\x8d_\xe8\x8d\xa4\xf2(\xa6\x88\xc7\xfe \xee\xdbe\xc9\r\x19{\xc8T\xc9JU[\x1d\xd3\xb0\xc6-\xdc\xc0YS\xae\x01\x12t(\xc7`m\xc6\x8c\xa8Xr\xb27\xf2\xec\xa3\x0b\r\xfe\xc4\xc0\xf0At\x00Y\xb5\x1b\xebE\x8c:p\xd4\xc1\x80k\x13\xc8I\xfe$\xday\xd2\xcc/\x00\n\t\x02B\xfa\r\x13o\x0f\x8d\xd9<7\xb5\xd0\xa3/\xee\xac\xae&"\x83\xa4)\x10L\xd0-q\xab \x9c\\\xc0\x92\x07MC\x85D\x17Z\xa49\xe3U\xa9\xc4\xc8z|\x1c\xe2\x03\t\x1d\x03\xe2J\x0fM\xfa5!\x98>5\x19h\xbc;{H\xa1\x14\xe7\xcb.X\x93\x7f\x0c\x15\xad'

    exp_metainfo = {'announce'      : 'http://localhost:123',
                    'created by'    : 'mktorrent 1.0',
                    'creation date' : 1513521463,
                    'info': {'name'         : os.path.basename(content_path),
                             'piece length' : 2**15,
                             'pieces'       : exp_pieces,
                             'files'        : exp_files}}

    exp_attrs = SimpleNamespace(path=str(content_path),
                                infohash='0e2e012468101efec5b1ac81ded6b8d95591c1fb',
                                infohash_base32=b'BYXACJDICAPP5RNRVSA55VVY3FKZDQP3',
                                size=sum(fileinfo['length'] for fileinfo in exp_files))

    return SimpleNamespace(path=exp_attrs.path,
                           exp_metainfo=exp_metainfo,
                           exp_attrs=exp_attrs)


def _write_content_file(filepath, spec):
    if isinstance(spec, (int, float)):
        filepath.write_bytes(bytes(random.getrandbits(8)
                                   for _ in range(int(spec))))
    elif isinstance(spec, str):
        filepath.write_text(spec)
    elif isinstance(spec, (bytes, bytearray)):
        filepath.write_bytes(spec)
    else:
        raise RuntimeError(f'Invalid spec for {filepath}: {spec!r}')

def _random_size(piece_size, min_pieces=1, max_pieces=10):
    size = int(random.choice((
        piece_size * random.randrange(1, max_pieces),
        piece_size * (random.randrange(1, max_pieces) + random.random()),
        piece_size * (random.randrange(0, max_pieces) + max(0.1, random.random())),
    )))
    if int(size / torf.Torrent.piece_size_min) < min_pieces:
        size = min_pieces * torf.Torrent.piece_size_min
    print('random size:', size, 'pieces:', size / torf.Torrent.piece_size_min)
    return size

def _create_content_file(tmp_path, filename, spec):
    filepath = tmp_path / filename
    _write_content_file(filepath, spec)
    return filepath
@pytest.fixture
def create_content_file(tmp_path):
    func = functools.partial(_create_content_file, tmp_path)
    func.piece_size = torf.Torrent.piece_size_min
    func.random_size = functools.partial(_random_size, func.piece_size)
    return func

def _create_content_dir(tmp_path, dirname, *files):
    content_path = tmp_path / dirname
    content_path.mkdir()
    for filepath, spec in files:
        parts = [part for part in filepath.split(os.sep) if part]
        dirpath = content_path
        for part in parts[:-1]:
            dirpath = dirpath / part
            if not os.path.exists(dirpath):
                dirpath.mkdir()
        filepath = dirpath / parts[-1]
        _write_content_file(filepath, spec)
    return content_path
@pytest.fixture
def create_content_dir(tmp_path):
    func = functools.partial(_create_content_dir, tmp_path)
    func.piece_size = torf.Torrent.piece_size_min
    func.random_size = functools.partial(_random_size, func.piece_size)
    return func



@pytest.fixture
def generated_singlefile_torrent(mktorrent, singlefile_content):
    torrent = mktorrent()
    torrent.path = singlefile_content.path
    torrent.generate()
    return torrent

@pytest.fixture
def generated_multifile_torrent(mktorrent, multifile_content):
    torrent = mktorrent()
    torrent.path = multifile_content.path
    torrent.generate()
    return torrent


@contextlib.contextmanager
def _create_torrent(tmpdir, **kwargs):
    torrent_file = str(tmpdir.join('test.torrent'))
    try:
        t = torf.Torrent(**kwargs)
        t.generate()
        t.write(torrent_file)
        yield torrent_file
    finally:
        if os.path.exists(torrent_file):
            os.remove(torrent_file)

@pytest.fixture
def create_torrent(tmpdir):
    return functools.partial(_create_torrent, tmpdir)
