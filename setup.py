from setuptools import find_packages, setup

if __name__ == '__main__':
    setup(
        name='django-yarn',

        version='0.0.2',

        description='Use Facebook\'s Yarn package manager with Django.',
        long_description='Use Facebook\'s Yarn package manager with Django.',

        url='https://github.com/mvasilkov/django-yarn',

        author='Mark Vasilkov',
        author_email='mvasilkov@gmail.com',

        license='MIT',

        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
        ],

        keywords='django yarn',

        packages=find_packages(),
    )
