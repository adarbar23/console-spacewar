
MY_VENV="venv-console-spacewar"

echo "Purge and recreate virtual environment named $MY_VENV..."
vex -r $MY_VENV pip --version
vex -m $MY_VENV python --version
echo "Download requirements and keep downloaded packages..."
vex $MY_VENV pip install -r requirements.txt

echo "vex $MY_VENV python spacewar.py" > vr.sh
echo "vex $MY_VENV" > vs.sh
echo ""
echo "To (R)un in venv $MY_VENV: vr.sh"
echo "(S)hell, in venv $MY_VENV: vs.sh"
echo ""