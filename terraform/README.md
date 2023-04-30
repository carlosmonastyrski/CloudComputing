# Infraestructura como Código: Terraform

## Paso 1: Instalación de Terraform

Lo primero que debemos hacer es instalar Terraform en la terminal en la que estamos trabajando, para ello ejecutamos el comando:

```
 wget https://releases.hashicorp.com/terraform/1.4.2/terraform_1.4.2_linux_amd64.zip
```

Esto nos descargará el .zip, por lo cual lo descomprimimos:

```
unzip terraform_1.4.2_linux_amd64.zip
```

Movemos el archivo a la carpeta usr/local/bin que contiene los comandos de la terminal

```
sudo mv terraform /usr/local/bin
```

## Paso 2: Crear un primer fichero de configuración (main.tf)

```
provider "google" {
  credentials = "${file("account.json")}"
  project      = "agile-alignment-384815"
  region       = "europe-central2"
}
```
* [main.tf](main.tf)
Como se puede ver, se hace uso de un archivo llamado account.json, el cual se puede generar desde la opción de IAM (cuentas de servicio) y generar dicho archivo de credenciales. Una vez en nuestro poder tendremos que cargarlo en el entorno donde se esté trabajando

## Paso 3: Crear el archivo para crear una dos maquinas virtuales y un load balancer entre ellas

* [machines.tf](machines.tf)

## Paso 4: Ejecutar los comandos de Terraform

```
terraform init
```

```
terraform plan
```

```
terraform apply
```


## Opcional: Destruir los cambios

Para eliminar todo lo que hayamos creado anteriormente podemos simplemente ejecutar:

```
terraform destroy
```