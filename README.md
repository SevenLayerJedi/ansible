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

#### GIT Clone Repo
cd /opt
sudo git clone https://github.com/SevenLayerJedi/ansible.git

#### Make Admin Owner
sudo chown admin:admin -R /opt/ansible/

#### Fix SSH Key Permission
chmod 600 keys/pinode

#### Install venv
sudo apt install python3.11-venv

#### Create Virtual Environment
sudo python3 -m venv venv

#### Activate the Environment
source venv/bin/activate

#### Upgrade PIP
pip install pip --upgrade

#### Install requirements.txt
pip install -r requirements.txt

#### Example run playbook
ansible-playbook -i inventory.ini playbooks/testtask.yml


#### Create Docker Container from Dockerfile
docker build -t nmap .


####
docker run -v /opt/docker/nmap:/opt/docker/nmap nmap 8.8.8.8 -p 53 -oA /opt/docker/nmap/test

####




