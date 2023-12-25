from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class BuildExt(build_ext):
    def build_extension(self, ext: Extension) -> None:
        print('name: ', ext.name, 'build_temp: ', self.build_temp)
        raise ValueError("test")


setup(
    ext_modules=[Extension("leveldb", [])],
    cmdclass={
        'build_ext': BuildExt
    }
)
