# ansible



#### Installing Ansible as current user
python3 -m pip install --user ansible

#### Add Ansible path to ~/.bash_profile
export PATH="/Users/slj/Library/Python/3.10/bin/:$PATH"
source ~/.bash_profile

#### Oneliner git Command
git pull;git add .;git commit -a -m "Commit to main";git push

#### Change private key permissions
chmod 600 keys/pinode

#### Run Ansible Test
ansible-playbook -i inventory.ini playbooks/testtask.yml

#### Allow users in sudo group to not type 'sudo'
Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL

#### No sudo for admin
admin   ALL=(ALL) NOPASSWD:ALL


#### Add admin to the sudo user group
sudo usermod -aG sudo admin
