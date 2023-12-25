import platform
import subprocess
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

_cur_folder = Path(__file__).parent


class BuildExt(build_ext):
    # build_temp: build/temp.macosx-12-x86_64-cpython-311
    # 也可能是 /var/folders/dt/jq_9y6kj5xd2y2cfnblpyhdm0000gn/T/tmp8qjde7ot.build-temp
    def build_extension(self, ext: Extension) -> None:
        build_path = _cur_folder / self.build_temp
        gen_cmd = ['cmake', '-S', _cur_folder / 'third_party/leveldb', '-B', build_path,
                   '-DBUILD_SHARED_LIBS=ON', '-DLEVELDB_BUILD_TESTS=OFF',
                   '-DLEVELDB_BUILD_BENCHMARKS=OFF', '-DCMAKE_BUILD_TYPE=Release']
        subprocess.run(gen_cmd)
        build_cmd = ['cmake', '--build', build_path]
        subprocess.run(build_cmd)
        _open_folder(build_path)


def _open_folder(folder):
    if platform.system() != 'Windows':
        subprocess.run(['open', folder])


setup(
    ext_modules=[Extension("leveldb", [])],
    cmdclass={
        'build_ext': BuildExt
    }
)
