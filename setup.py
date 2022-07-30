from setuptools import setup

setup(name='quordle',
      version='0.1',
      description='A tool for exploring Quordle strategies',
      long_description=open('README.txt').read(),
      install_requires=['numpy'],
      classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.7',
            'Topic :: Games/Entertainment',
            'Intended Audience :: Other Audience'
            
      ],
      url='https://github.com/rmgoetz/quordle',
      author='Ryan Goetz',
      author_email='ryan.m.goetz@gmail.com',
      license='MIT',
      packages=['quordle'],
      zip_safe=False)
