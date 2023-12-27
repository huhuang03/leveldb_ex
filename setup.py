import platform
import shutil
import subprocess
from distutils.command.build_ext import build_ext as _du_build_ext
from pathlib import Path

from setuptools import setup, Extension
from setuptools.extension import Library
from setuptools.command.build_ext import build_ext
from distutils import log

try:
    # Attempt to use Cython for building extensions, if available
    from Cython.Distutils.build_ext import build_ext as _build_ext
    # Additionally, assert that the compiler module will load
    # also. Ref #1229.
    __import__('Cython.Compiler.Main')
except ImportError:
    _build_ext = _du_build_ext

_cur_folder = Path(__file__).parent


class BuildExt(build_ext):
    def build_extension(self, ext: Extension) -> None:
        build_path = _cur_folder / self.build_temp
        gen_cmd = ['cmake', '-S', _cur_folder / 'third_party/leveldb', '-B', build_path,
                   '-DBUILD_SHARED_LIBS=ON', '-DLEVELDB_BUILD_TESTS=OFF',
                   '-DLEVELDB_BUILD_BENCHMARKS=OFF', '-DCMAKE_BUILD_TYPE=Release']
        subprocess.run(gen_cmd)
        build_cmd = ['cmake', '--build', build_path]
        subprocess.run(build_cmd)
        _open_folder(build_path)
        # time.sleep(300000)
        self.try_copy(ext)

    def try_copy(self, ext: Extension):
        ext_root = Path(self.build_lib) / ext.name
        ext_root.mkdir(exist_ok=True)
        # copy all dylib in temp to ext_root
        build_tmp_path = Path(self.build_temp)
        for f in build_tmp_path.iterdir():
            if f.is_file() and f.suffix == '.dylib':
                dest_path = ext_root / f.name
                shutil.copy(f, dest_path)


def _open_folder(folder):
    if platform.system() != 'Windows':
        subprocess.run(['open', folder])


setup(
    ext_modules=[Library("leveldb", [])],
    cmdclass={
        'build_ext': BuildExt
    }
)
