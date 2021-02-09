#!/bin/bash
# Author Vivilian Kumar
set -x

if [ -f /home/stack/venv/salt-ssh/bin/activate ];
then
    function salt {
        source ~/venv/salt-ssh/bin/activate
        salt-ssh -c /home/stack/salt/etc/salt/ --log-file /home/stack/salt/var/log/salt/ssh --no-host-keys "$@";
        deactivate;
    }
else
    alias salt='/usr/bin/salt-ssh -c /home/stack/salt/etc/salt/ --log-file /home/stack/salt/var/log/salt/ssh --no-host-keys'
fi

# CBIS Health-Check:

source stackrc

echo "salt "*Controller*" cmd.run "clustercheck""
salt "*Controller*" cmd.run "clustercheck"

echo -e "\n df -kh"
df -kh

echo -e "\n salt "*" cmd.run "ceph health""
salt "*" cmd.run "ceph health"

echo -e "\n heat stack-list"
heat stack-list

echo -e "\n ironic node-list"
ironic node-list

echo -e "\n nova list"
nova list

echo -e "\n nova service-list"
nova service-list

echo -e "\n ntpstat"
ntpstat

echo -e "\n ntpq -p"
ntpq -p

echo -e "\n salt "*Controller*" cmd.run "ntpq -p""
salt "*Controller*" cmd.run "ntpq -p"

echo -e "\n salt "*" cmd.run "df -kh""
salt "*" cmd.run "df -kh"

echo -e "\n salt "*Controller*" cmd.run "ntpstat""
salt "*Controller*" cmd.run "ntpstat"

echo -e "\n salt '*' cmd.run 'ntpstat'"
salt '*' cmd.run 'ntpstat'

echo -e "\n salt "*" cmd.run "hwclock --systohc""
salt "*" cmd.run "hwclock --systohc"

source overcloudrc

echo -e "\n nova list --all --fields=host,name,status"
nova list --all --fields=host,name,status

echo -e "\n salt "Controller-0" cmd.run "sudo ceph osd tree""
salt "Controller-0" cmd.run "sudo ceph osd tree"

echo -e "\n nova service-list"
nova service-list

echo -e "\n cinder service-list"
cinder service-list

echo -e "\n heat service-list |grep controller-0 |grep up |wc -l"
heat service-list |grep controller-0 |grep up |wc -l

echo -e "\n heat service-list"
heat service-list

echo -e "\n salt "*" cmd.run "free -h""
salt "*" cmd.run "free -h"

echo -e "\n salt "*" cmd.run "mpstat""
salt "*" cmd.run "mpstat"

echo -e "\n neutron agent-list"
neutron agent-list

echo -e "\n sudo systemctl status ntpd"
sudo systemctl status ntpd

echo -e "\n salt "Controller*" cmd.run "sudo pcs status""
salt "Controller*" cmd.run "sudo pcs status"

echo -e "\n salt '*' cmd.run 'sudo systemctl --failed | grep -i fail'"
salt '*' cmd.run 'sudo systemctl --failed | grep -i fail'

# CBAM Health-Check:

echo -e "\n Enter ssh -i <ssh key> cbam@<cbam VIP>"
read SSHCBAM
$SSHCBAM  /bin/bash << EOF
echo -e "\n systemctl status cbam-reconfigure.service"
systemctl status cbam-reconfigure.service

echo -e "\n DNS Verification"
nslookup google.com

echo -e "\n NTP Verification"
ntpq -p

echo -e "\n systemctl status cbam-operability-distribution.service"
systemctl status cbam-operability-distribution.service

echo -e "\n sudo systemctl status cbam-component-catalog.service"
sudo systemctl status cbam-component-catalog.service

echo -e "\n sudo systemctl status cbam-component-alma.service"
sudo systemctl status cbam-component-alma.service

echo -e "\n sudo systemctl status cbam-scheduler.service"
sudo systemctl status cbam-scheduler.service

exit
EOF

