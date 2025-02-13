# Configuración del Curso de Ingeniería en IA

¡Bienvenido al curso de Ingeniería en IA! Este documento te guiará a través del proceso de configuración de tu entorno de desarrollo. Cubriremos:

1. [Instalación de Python 3.12](#instalacion-de-python-312)  
2. [Instalación de PyCharm](#instalacion-de-pycharm)  
3. [Instalación de Git y GitHub CLI](#instalacion-de-git-y-github-cli)  
4. [Instalación de Google Cloud CLI](#instalacion-de-google-cloud-cli)  
5. [Creación de un Entorno Virtual y Archivo `.env`](#creacion-de-un-entorno-virtual-y-archivo-env)  

---

## Instalación de Python 3.12

### Windows
1. Ve al sitio oficial de [Python](https://www.python.org/downloads/).
2. Selecciona **Descargar Python 3.12** para Windows.
3. Ejecuta el instalador.
   - Asegúrate de marcar **Agregar Python 3.12 a PATH**.
   - Haz clic en **Instalación personalizada** si deseas seleccionar características específicas.
   - Completa la instalación.

### macOS
1. Ve al sitio oficial de [Python](https://www.python.org/downloads/).
2. Selecciona **Descargar Python 3.12** para macOS.
3. Abre el archivo `.pkg` y sigue los pasos de instalación.
4. Si es necesario, actualiza tu PATH (por ejemplo, editando `~/.zshrc` o `~/.bash_profile`) para que `python3.12` se use por defecto.

### Linux (Ubuntu/Debian)
1. Las distribuciones de Linux pueden no tener Python 3.12 en los repositorios por defecto.
2. Puedes instalarlo vía `apt` (si está disponible) o compilarlo desde el código fuente. Por ejemplo:
   ```bash
   sudo apt-get update
   sudo apt-get install -y build-essential libssl-dev libffi-dev python3.12 python3.12-venv python3.12-dev
   ```
   Si `python3.12` no está disponible, sigue la documentación oficial para compilarlo desde el código fuente o usa un PPA.

---

## Instalación de PyCharm
1. Ve a la [página de descarga de PyCharm](https://www.jetbrains.com/pycharm/download/).
2. Elige la edición Community (gratuita) o la edición Professional (de pago, con características adicionales).
3. Instala según las instrucciones de tu sistema operativo.

### Después de la instalación
- Inicia PyCharm.
- (Opcional) Instala plugins útiles:
  - Integración con GitHub
  - Soporte para Markdown
  - Plugin de Docker (si es relevante)

---

## Instalación de Git y GitHub CLI

### Git
#### Windows
1. Descarga [Git para Windows](https://git-scm.com/).
2. Ejecuta el instalador (elige las opciones por defecto o personaliza según sea necesario).

#### macOS
Verifica si Git ya está instalado:
```bash
git --version
```
Si no está instalado, instala las herramientas de línea de comandos de Xcode o descárgalo desde [git-scm.com](https://git-scm.com/).

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y git
```

### GitHub CLI
1. Sigue la [guía de instalación de GitHub CLI](https://cli.github.com/).
2. Verifica la instalación:
```bash
gh --version
```
3. Autentícate:
```bash
gh auth login
```
Sigue las indicaciones para iniciar sesión con tu cuenta de GitHub.

---

## Instalación de Google Cloud CLI

### Windows (PowerShell):
```powershell
Invoke-WebRequest "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile "GoogleCloudSDKInstaller.exe"
.\GoogleCloudSDKInstaller.exe
```

### macOS/Linux:
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Inicializar el CLI:
```bash
gcloud init
```
Inicia sesión con tu cuenta de Google y configura tu proyecto deseado.

---

## Creación de un Entorno Virtual y Archivo `.env`

### 1. Crear la Carpeta del Proyecto
```bash
mkdir mi-proyecto-ia
cd mi-proyecto-ia
```

### 2. Configurar un Entorno Virtual
Python 3.12 incluye `venv` por defecto:
```bash
python3.12 -m venv venv
```

#### Activar el entorno:
##### Windows (PowerShell/CMD):
```powershell
.\venv\Scripts\activate
```
##### macOS/Linux:
```bash
source venv/bin/activate
```
Una vez activado, tu terminal debería mostrar `(venv)`.

### 3. Instalar Paquetes Requeridos
Dentro del `venv` activado, instala cualquier dependencia necesaria, por ejemplo:
```bash
pip install requests
```
(Las dependencias específicas variarán según el proyecto.)

### 4. Crear un Archivo `.env`
Este archivo almacena información sensible (claves de API, etc.) que no quieres subir a GitHub.

#### Crear `.env`:
```bash
touch .env
```
#### Agregar claves de API:
```bash
OPENAI_API_KEY="sk-123..."
GCP_API_KEY="gcp-123..."
```

#### Excluir `.env` de Git:
Crea (o edita) `.gitignore` en la raíz de tu proyecto:
```bash
touch .gitignore
```
Agrega:
```bash
.env
```

#### Cargar `.env` en tu código:
Instala `python-dotenv`:
```bash
pip install python-dotenv
```

En tu script de Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
gcp_api_key = os.getenv("GCP_API_KEY")

print(f"Clave de OpenAI: {openai_api_key}")
print(f"Clave de GCP: {gcp_api_key}")
```

---

## Verificación Final

### Versión de Python:
```bash
python --version
```
Debe mostrar Python 3.12.x.

### Entorno Virtual:
- ¿Activado? Verifica si tu terminal muestra `(venv)`.

### PyCharm:
- ¿Puedes abrir tu carpeta de proyecto y ejecutar código?

### Git:
```bash
git --version
```
Debe mostrar una versión válida (ej. `2.XX.X`).

### GitHub CLI:
```bash
gh --version
```
Debe mostrar una versión válida y deberías estar autenticado (`gh auth status`).

### Google Cloud CLI:
```bash
gcloud version
```
Debe mostrar la versión del SDK de Google Cloud.

### `.env`:
- Contiene tus claves de API.
- Está listado en `.gitignore`.

---

¡Tu entorno de Ingeniería en IA está listo!
