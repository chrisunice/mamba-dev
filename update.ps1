# Simulating network drive
# This is necessary only on the unclass side
subst U: C:\VaultNet\

# Update pip
python -m pip install --upgrade pip

# Reinstall mamba-ui manually
pip uninstall mamba_ui -y
pip install mamba_ui --no-index --find-links=U:\PyPI

# Reinstall lodat manually
pip uninstall lodat -y
pip install lodat --no-index --find-links=U:\PyPI

# Install the package requirements
pip install -r .\requirements.txt

# Install the dev requirements
pip install -r .\dev-requirements.txt
