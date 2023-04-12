 # Capturador de documentos.
 ## Captura un documento de identidad por ambas caras, permitiendo recortar el area deseada, lo importa a un PDF donde se ubica ambas caras en una hoja: la cara frontal sobre la cara posterior.

 ## Para ejecutar use:

 ´´´ python

git clone
cd capturaImagen
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 capturaImagen.py

Tambien puede ejecutar:
chmod 777 capturaImagen.sh # Para dar permisos de Exec.
./capturaImagen.sh

Copie el fichero 'superservicios_capturaImagen.desktop' en '/usr/share/applications' para crear un acceso directo en aplicaciones para todos los usuarios.
 ´´´
