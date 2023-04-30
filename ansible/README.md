# Infraestructura como Código

# Paso 1: Instalar Ansible en una máquina de tu elección

Utilicé pip, ya que no tenía la posibilidad de utilizar sudo:

```
pip install ansible
```

# Paso 2: Crear dos máquinas virtuales utilizando un Playbook para crear las máquinas con Ansible

Fue necesario configurar los permisos y generar un archivo JSON para que en el playbook se pudiera autenticar ansible al realizar las  peticiones:

```
$ gcloud config set project smart-howl-365613
$ gcloud iam service-accounts create autenticacion
$ gcloud projects add-iam-policy-binding smart-howl-365613 --member "serviceAccount:1003776626205-compute@developer.gserviceaccount.com" --role "roles/editor"
$ gcloud iam service-accounts keys create permisos --iam-account:1003776626205-compute@developer.gserviceaccount.com
```

Una vez realizado esto, cree mi Playbook infra.yml:
* [infra.yml](infra.yml)

Y lo ejecute con ansible-playbook infra.yml:
```
ansible-playbook infra.yml
```

# Paso 3: Crear un inventario con esas máquinas

```
nano inventory.ini
```
```
[server]
35\.195.6.122

[db]
104.155.28.188
```
* [inventory.init](inventory.ini)

# Paso 4: Crear un Playbook para hacer ping a ambas máquinas

En este paso, antes tenemos que habilitar la comunicación mediante SSH entre las máquinas, añadiendo la clave ssh que se generó en mi terminal de cloud en ~/.ssh/authorized\_keys de ambas instancias.
Y con esto creamos el playbook:
* [ping.yml](ping.yml)

Y lo ejecutamos con 
```
ansible-playbook -i inventory.ini ping.yml
```

# Paso 5: Crear un Playbook para instalar Apache y PHP, en webserver, y MySQL en database

El playbook que cree se llamó: [install-features.yml](install-features.yml):

Y lo ejecuté con: 
```
ansible-playbook -i inventory.ini install-features.yml
```

Fue necesario antes de ejecutar esta línea modificar en las instancias para que no solicite la  clave de sudo para ejecutar los comandos:
```
sudo visudo
```
Y al final del archivo se agrega el nombre del usuario de nuestra terminal seguido por
```
ALL=(ALL) NOPASSWD: ALL
```