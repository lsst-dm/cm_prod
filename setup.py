from setuptools import setup

setup(
    name="cm_prod",
    author="Eric Charles, Hsin-Fang Chiang, Colin Slater",
    author_email="echarles@slac.stanford.edu",
    url="https://github.com/lsst-dm/cm_prod",
    packages=["lsst.cm.prod"],
    package_dir={"": "python"},
    description="Campaign Managment Production configurations",
    setup_requires=["setuptools_scm"],
    long_description=open("README.rst").read(),
    package_data={"": ["README.rst", "LICENSE"]},
    use_scm_version={"write_to": "python/lsst/cm/prod/_version.py"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[],
    tests_require=["pytest", "pytest-cov"],
)
