
MY_VENV="venv-console-spacewar"

echo "Upgrade tools..."
pip install --user --upgrade pip
pip install --user --upgrade virtualenv
pip install --user --upgrade vex
echo "Purge and recreate virtual environment named $MY_VENV..."
vex -r $MY_VENV pip --version
vex -m $MY_VENV python --version
echo "Download requirements and keep downloaded packages..."
vex $MY_VENV pip install -r requirements.txt

echo "vex $MY_VENV python spacewar.py" > run-dev.sh
echo "vex $MY_VENV" > sh-dev.sh
echo ""
echo "To run in venv $MY_VENV: run-dev.sh"
echo "Shell, in venv $MY_VENV: sh-dev.sh"
echo ""