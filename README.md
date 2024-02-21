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


#### Build nmap docker image
docker build -t nmap /opt/ansible/registry/nmap

#### Make nmap dir
sudo mkdir -p /opt/docker/nmap && sudo chmod 777 -R /opt/docker

#### Run nmap docker container
docker run --rm -v /opt/docker/nmap:/opt/docker/nmap nmap 8.8.8.8 -p 53 -oA /opt/docker/nmap/test


#### Build masscan docker image
docker build -t masscan /opt/ansible/registry/masscan

#### Make masscan dir
sudo mkdir -p /opt/docker/nmap && sudo chmod 777 -R /opt/docker

#### Run masscan docker container
docker run --rm -v /opt/docker/masscan:/opt/output masscan 8.8.8.8 -p53 --rate 100 -oX /opt/output/masscan_test.xml



#### Build nikto docker image
docker build -t nikto /opt/ansible/registry/nikto2

#### Make nikto dir
sudo mkdir -p /opt/docker/nikto && sudo chmod 777 -R /opt/docker

#### Run nikto docker container
docker run --rm -v /opt/docker/nikto:/opt/output nikto -h http://www.foo.com -output /opt/output/nikto_example.xml





docker run --rm -d -v /opt/docker/masscan:/opt/output --entrypoint "/bin/sh" masscan -c '/masscan/bin/masscan 8.8.8.8 -p53 --rate 100 -oX /opt/output/masscan_test_223.xml;echo $(date +%s) > /opt/output/finish_time.txt'



####
docker container commit c8cc94cb108a nmap:latest



####
docker push bugbountytools/nmap:latest


docker tag nmap:latest bugbountytools/nmap:latest

docker push bugbountytools/nmap:latest

docker pull bugbountytools/nmap


docker build -t bugbountytools/nmap /opt/ansible/registry/nmap

docker push bugbountytools/nmap:latest


docker run --rm -v /opt/docker/nmap:/opt/docker/nmap bugbountytools/nmap -sC -sV -p53 8.8.8.8


