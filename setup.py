from setuptools import setup, find_packages

setup(
    name="wedding_blog_generator",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "openai",
        "unidecode",
    ],
    entry_points={
        "console_scripts": [
            "wedding-blog-generator=wedding_blog_generator.main:main",
        ],
    },
)