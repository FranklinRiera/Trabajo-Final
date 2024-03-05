public_ip_API = "3.239.63.97"
public_ip_Client = "44.192.88.252"

Colocar la ip_API en el archivo APIinventory.yml
Colocar la ip_Client en el archivo Clientinventory.yml
Colocar la ip_API en la funcion llamar API del archivo index.html

python3 -m virtualenv ENV 
source ENVbin/activate
cd /opt/myproject/
pip install requests
pip install Flask
pip install boto3
python myproject.py

