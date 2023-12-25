import subprocess
import time

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from pathlib import Path
import logging

_cur_folder = Path(__file__).parent

logging.basicConfig(level=logging.DEBUG)

class BuildExt(build_ext):
    # build_temp: build/temp.macosx-12-x86_64-cpython-311
    # 也可能是 /var/folders/dt/jq_9y6kj5xd2y2cfnblpyhdm0000gn/T/tmp8qjde7ot.build-temp
    def build_extension(self, ext: Extension) -> None:
        logging.info('name: ', ext.name, 'build_temp: ', self.build_temp)
        build_path = _cur_folder / self.build_temp
        print(f'build_path: {build_path.resolve()}')
        gen_cmd = ['cmake', '-S', _cur_folder / 'third_party/leveldb', '-B', build_path,
                   '-DBUILD_SHARED_LIBS=ON', '-DLEVELDB_BUILD_TESTS=OFF', '-DLEVELDB_BUILD_BENCHMARKS=OFF']
        subprocess.run(gen_cmd)
        build_cmd = ['cmake', '--build', build_path]
        subprocess.run(build_cmd)
        subprocess.run(['open', build_path])
        time.sleep(30000000)
        raise ValueError("test")


setup(
    ext_modules=[Extension("leveldb", [])],
    cmdclass={
        'build_ext': BuildExt
    }
)
