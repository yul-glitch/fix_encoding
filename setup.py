from setuptools import setup


setup(
    name='fix_encoding',
    version='0.0.2',
    license='GPLv2+',
    url='https://github.com/yul-glitch/fix_encoding',
    description='Cross-platform clipboard utilities supporting both binary and text data.',
    author_email='yulquen@protonmail.com',
    author='Aymeric Guth',
    packages=['fix_encoding'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v2 or later(GPLv2+)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
    ],
    # entry_points={
    #     'console_scripts': ['fix_encoding = fix_encoding.cli:main']
    # },
)
