# Build code for deployment to work
#pip-chill > .\requirements.txt

# Remove any old dependencies
del .\dependencies\*

# Download from internet's PyPI
pip download -r .\requirements.txt --dest .\dependencies\

# Download from local PyPI
pip download mamba-ui --no-index --find-links U:\PyPI --dest .\dependencies\

