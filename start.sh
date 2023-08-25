set -eu

export PYTOHONNUNBUFFERED=true

VIRUALENV=.data/venv

if [ ! -d $VIRUALENV ]; then
    python3 -m venv $VIRUALENV
fi

if [ ! -f $VIRUALENV/bin/pip ]; then
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py $VIRUALENV
fi

$VIRUALENV/bin/pip install -r requirements.txt

$VIRUALENV/bin/python3 app.py
Footer