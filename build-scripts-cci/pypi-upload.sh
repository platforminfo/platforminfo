set -e

swupd bundle-add python-basic

PYPI_CONFIG="${HOME}/.pypirc"
pip install --upgrade pip
pip install twine
echo $'[distutils]\nindex-servers = pypi\n[pypi]' > $PYPI_CONFIG
echo "username=$PYPI_USERNAME" >> $PYPI_CONFIG
echo "password=$PYPI_PASSWORD" >> $PYPI_CONFIG
twine upload /tmp/dist/*.whl
