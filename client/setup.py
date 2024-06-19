from setuptools import setup
from setuptools.command.build_py import build_py
from distutils.spawn import spawn, find_executable

class Build(build_py):
    def run(self):
        spawn([find_executable('protoc'), '--python_out=.', 'rabbitmq_client/proto/message.proto'])
        build_py.run(self)


setup(
    name='rabbitmq_client',
    version='1.0.0',
    author='R&EC SPb ETU',
    author_email='info@nicetu.spb.ru',
    url='http://nicetu.spb.ru',
    description='Работа с брокером сообщений, клиентская часть',
    long_description="",
    zip_safe=False,
    packages=['rabbitmq_client'],
    cmdclass={
        'build_py': Build
    },
)
