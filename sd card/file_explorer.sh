#!/bin/bash

echo "Enter your raspiberry pi's IP address: "
read IP

echo "#!/bin/bash
if [[ \$EUID > 0 ]]; then
  echo \"This script requires sudo\"
  exit 1
fi
sed -i \"539s/kill()/kill('SIGINT')/\" /opt/brickpiexplorer/app.js
printf '%s\n' 539m540 540-m539- w q | ed -s /opt/brickpiexplorer/app.js" > fix.sh

scp fix.sh pi@$IP:~/
ssh -t pi@$IP 'sudo bash ~/fix.sh'
rm fix.sh