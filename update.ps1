python -m pip install --upgrade pip
pip install -r .\requirements.txt

pip uninstall lodat -y
pip install lodat --no-index --find-links=U:\PyPI

pip uninstall mamba_ui -y
pip install mamba_ui --no-index --find-links=U:\PyPI
