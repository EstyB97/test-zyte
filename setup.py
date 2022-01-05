from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '14.7.4',
    packages     = find_packages(),
    package_data={
        'laptopsdirect': ['resources/*.txt']
    },
    scripts      = ['bin/aoscript.py'],
    entry_points = {'scrapy': ['settings = LaptopsDirect.settings']},
    zip_safe=False,
)