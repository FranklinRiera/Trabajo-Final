# Instrucciones Terraform & Ansible para crear el cliente que consume la API generar facturas 

Estas instrucciones contienen las indicaciones necesarias para desplegar el cliente, quien podrá generar sus facturas digitales.

## Desplegar la VM en AWS e instalar el Cliente

### 1. Crear una nueva ACCESS KEY en AWS

After you create your service account, download your service account key.

- Select your service account from the list
- Select the "Keys" tab
- Download the .csv with your credentials
- In the drop down menu, select "Create new key"
- Click "Create" to create the key and save the key file to your system

### 2. Descargar el codigo del siguiente repositorio

Utilizar la siguiente linea de comandos para descargar el proyecto desde el repositorio

```bash
git clone https://diegomonterob.me:8080/cloud_computing/franklin.riera.git
```

### 3. Configurar el archivo main.tf con las credenciales del ACCESS KEY de AWS

Colocar las credenciales Access Key y Secret KEY de AWS en el archivo main.tf

### 4. Install Terraform and Ansible

- Follow the [Install Terraform instructions](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) for Linux and verify the installation.
- Follow the [Install Ansible instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible) for Linux:

```bash
apt update
apt install ansible
```

### 5. Desplegar la VM en AWS e instalar el Cliente

Para crear la VM en AWS, ejecuta la siguiente los siguientes comandos

#### Initialize the directory
When you create a new configuration, you need to initialize the directory with terraform init. This step downloads the providers defined in the configuration.

Initialize the directory:

```bash
terraform init
```
You can also make sure your configuration is syntactically valid and internally consistent by using the `terraform validate` command.

```bash
terraform validate
```
#### Apply the configuration now with the `terraform apply` command. 

```bash
terraform apply
```

#### Cnfigure the Clientinventory.yml
- Replace the IP in this file with the client_IP to finish terraform

#### Execute the Ansible playbook

```bash
ansible-playbook Clientplaybook.yml -i Clientinventory.yml
```

### 6. Verify the HTTP APP

- Abre tu navegador de preferencia e ingresa la dirección IP mostrada al ejecutar terraform

### 7. Genera tus facturas electrónicas

- Ingresa la clave de acceso o el número de autorización de tu comprobante electronico para proceder con la creacion de tus facturas.
- Genera una lista de comprobantes almacenados al dar clic sobre el boton listar.
