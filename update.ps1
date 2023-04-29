# Update pip and grab all requirements
python -m pip install --upgrade pip
pip install -r .\requirements.txt

# Update requirements file
pip-chill > .\requirements.txt

# Reinstall lodat
pip uninstall lodat -y
pip install lodat --no-index --find-links=U:\PyPI

# Reinstall mamba user interface
pip uninstall mamba_ui -y
pip install mamba_ui --no-index --find-links=U:\PyPI
