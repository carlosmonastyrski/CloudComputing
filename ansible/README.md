<a name="br1"></a>**UNIVERSIDAD DE HUELVA**

**MASTER EN INGENIERÍA EN INFORMÁTICA**

**Cátedra: Cloud Computing**

**Infraestructura como Código**

Ciclo lectivo 2022-2023

Profesor: José Luis Álvarez Macías

Alumno: Monastyrski, Carlos Alberto




<a name="br2"></a>Infraestructura como Código

Instala Ansible en una máquina de tu elección

Utilicé pip, ya que no tenía la posibilidad de utilizar sudo:

Crea dos máquinas virtuales utilizando un Playbook para crear las máquinas con Ansible

Fue necesario configurar los permisos y generar un archivo JSON paraque en el playbook se pudiera autenticar ansible al realizar laspeticiones:

$ gcloud config set project smart-howl-365613$ gcloud iam service-accounts create autenticacion$ gcloud projects add-iam-policy-binding smart-howl-365613--member

"serviceAccount:1003776626205-compute@developer.gserviceaccount.com" --role "roles/editor"

$ gcloud iam service-accounts keys create permisos --iam-account1003776626205-compute@developer.gserviceaccount.com

Una vez realizado esto, cree mi Playbook infra.yml:

\- name: 'Deploy gcp vm'

hosts: localhost

connection: local

become: false

gather\_facts: no




<a name="br3"></a>vars:

gcp\_project: smart-howl-365613

zone: europe-west1-b

auth\_kind: serviceaccount

image: ubuntu-20-04

gcp\_region: europe-west1

service\_account\_file: ~/permisos.json

machine\_type: n1-standard-1

network: default

\# Roles & Tasks

tasks:

\- name: create a disk

gcp\_compute\_disk:

name: disk-instance

size\_gb: 50

source\_image: projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts

zone: "{{ zone }}"

project: "{{ gcp\_project }}"

auth\_kind: "{{ auth\_kind }}"

service\_account\_file: "{{ service\_account\_file }}"

state: present

register: disk

\- name: create a address

gcp\_compute\_address:

name: address-instance

region: "{{ gcp\_region }}"

project: "{{ gcp\_project }}"

auth\_kind: "{{ auth\_kind }}"

service\_account\_file: "{{ service\_account\_file }}"

state: present

register: address

\- name: create a address2

gcp\_compute\_address:

name: address-instance2

region: "{{ gcp\_region }}"

project: "{{ gcp\_project }}"

auth\_kind: "{{ auth\_kind }}"

service\_account\_file: "{{ service\_account\_file }}"

state: present

register: address2



<a name="br4"></a>- name: create a disk 2

gcp\_compute\_disk:

name: disk-instance2

size\_gb: 50

source\_image: projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts

zone: "{{ zone }}"

project: "{{ gcp\_project }}"

auth\_kind: "{{ auth\_kind }}"

service\_account\_file: "{{ service\_account\_file }}"

state: present

register: disk2

\- name: create a instance

gcp\_compute\_instance:

name: instance1

machine\_type: "{{ machine\_type }}"

project: "{{ gcp\_project }}"

zone: "{{ zone }}"

state: present

auth\_kind: "{{ auth\_kind }}"

service\_account\_file: "{{ service\_account\_file }}"

disks:

\- auto\_delete: 'true'

boot: 'true'

source: "{{ disk }}"

network\_interfaces:

\- network:

access\_configs:

\- name: external-nat

nat\_ip: "{{ address }}"

type: ONE\_TO\_ONE\_NAT

\- name: create a instance

gcp\_compute\_instance:

name: instance2

machine\_type: "{{ machine\_type }}"

project: "{{ gcp\_project }}"

zone: "{{ zone }}"

disks:

\- auto\_delete: 'true'

boot: 'true'

source: "{{ disk2 }}"

network\_interfaces:

\- network:

access\_configs:




<a name="br5"></a>- name: external-nat

nat\_ip: "{{ address2 }}"

type: ONE\_TO\_ONE\_NAT

state: present

auth\_kind: "{{ auth\_kind }}"

service\_account\_file: "{{ service\_account\_file }}"

Y lo ejecute con ansible-playbook infra.yml:

Y quedaron creadas ambas instancias:

Crea un inventario con esas máquinas

nano inventory.ini

[server]

35\.195.6.122

[db]

104\.155.28.188

Crea un Playbook para hacer ping a ambasmáquinas

En este paso, antes tenemos que habilitar la comunicación mediante SSH entre lasmáquinas, añadiendo la clave ssh que se generó en mi terminal de cloud en~/.ssh/authorized\_keys de ambas instancias.

Y con esto creamos el playbook:

\- name: Ping a la db

hosts: db



<a name="br6"></a>gather\_facts: false

tasks:

\- name: Realizar un ping a la db

ping:

\- name: Ping al server

hosts: server

gather\_facts: false

tasks:

\- name: Realizar un ping al server

ping:

Y lo ejecutamos con ansible-playbook -i inventory.ini ping.yml

Crea un Playbook para instalar Apache y PHP, enwebserver, y MySQL en database

El playbook que cree se llamó: install-features.yml:

\- hosts: server

become: true

tasks:

\- name: Actualizar apt-get

apt:

update\_cache: yes

\- name: Instalar Apache

apt:

name: apache2

state: present

\- name: Instalar PHP

apt:

name:

\- libapache2-mod-php

\- php

\- php-cli

\- php-mysql



<a name="br7"></a>state: present

\- hosts: db

become: true

tasks:

\- name: Actualizar apt-get

apt:

update\_cache: yes

\- name: Instalar MySQL

apt:

name: mysql-server

state: present

Y lo ejecuté con: ansible-playbook -i inventory.ini install-features.yml

Fue necesario antes de ejecutar esta línea modificar en las instancias para que no solicite laclave de sudo para ejecutar los comandos:

sudo visudo




<a name="br8"></a>Y al final del archivo se agrega el nombre del usuario de nuestra terminal seguido porALL=(ALL) NOPASSWD: ALL
