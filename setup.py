from setuptools import setup, find_packages

setup(
    name='html22text',
    version='1.0.0',
    description='Convert HTML into Markdown or plain text in a smart way',
    long_description='Convert HTML into Markdown or plain text in a smart way',
    keywords='txt plaintext markdown export',
    url='https://github.com/twardoch/html22text',
    author='Adam Twardoch',
    author_email='adam+github@twardoch.com',
    license='MIT',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['html22text=html22text.__main__:cli'],
    }
)
