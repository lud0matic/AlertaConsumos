# 💳 AlertaConsumos

Sistema inteligente para extraer y organizar alertas de consumos de tarjetas Visa y Mastercard directamente desde Gmail.

## 🚀 Gestionado con uv

Este proyecto utiliza [**uv**](https://github.com/astral-sh/uv) como gestor de paquetes y entornos virtuales. **uv** es una herramienta ultra rápida escrita en Rust que reemplaza pip, pip-tools, pipx, poetry, pyenv, virtualenv, y más.

### ¿Por qué uv?

- ⚡ **10-100x más rápido** que pip y pip-tools
- 🔒 **Gestión determinística** de dependencias con lockfile
- 🐍 **Gestión de versiones de Python** integrada
- 📦 **Todo en uno**: maneja paquetes, entornos virtuales y versiones de Python
- 🛠️ **Compatible con pip**: usa los mismos comandos que ya conoces

## ✨ Características

- 📧 **Extracción automática** de emails de:
  - **Visa**: `alertas@infomistarjetas.com`
  - **Mastercard**: `mcalertas@mcalertas.com.ar`
- 📊 **Visualización clara** en formato tabla con columnas alineadas
- 💰 **Cálculo automático** de subtotales por tarjeta
- 📅 **Ordenamiento cronológico** de transacciones (antiguas a recientes)
- 📁 **Exportación a CSV** con timestamp automático
- 🔍 **Información detallada**:
  - Establecimiento/Comercio
  - Monto de la transacción
  - Cantidad de cuotas
  - Fecha y hora
  - Estado de la transacción

## 📋 Requisitos Previos

### Instalar uv

#### macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Con Homebrew (macOS):
```bash
brew install uv
```

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/lud0matic/AlertaConsumos.git
cd AlertaConsumos
```

### 2. Configurar el proyecto con uv

uv se encargará automáticamente de:
- ✅ Crear el entorno virtual
- ✅ Instalar la versión correcta de Python
- ✅ Instalar todas las dependencias

```bash
# Opción 1: Instalar desde pyproject.toml y uv.lock (recomendado)
uv sync

# Opción 2: Instalar desde requirements.txt
uv pip install -r requirements.txt

# Opción 3: Instalar dependencias manualmente
uv pip install simplegmail beautifulsoup4
```

### 2.1 Alternativa: Instalación tradicional con pip

Si prefieres usar pip tradicional:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## ⚙️ Configuración

### Primera vez usando AlertaConsumos

1. Al ejecutar por primera vez, se abrirá tu navegador automáticamente
2. Inicia sesión en tu cuenta de Gmail
3. Autoriza el acceso a la aplicación
4. Las credenciales se guardarán de forma segura para futuros usos

### Personalización

Edita estas variables en `main.py`:

```python
DATE = "2025-07-24"  # Fecha desde la cual buscar emails (YYYY-MM-DD)
EXPORT_CSV = True    # True: exporta a CSV | False: solo muestra en consola
```

## 🚀 Uso

### Ejecutar con uv (recomendado)

```bash
# uv ejecuta el script en el entorno correcto automáticamente
uv run python main.py
```

### Ejecutar tradicional

```bash
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
python main.py
```

### Ejemplo de salida

```
=== VISA ALERTS ===
Establecimiento                          Monto           Cuotas   Fecha y Hora
------------------------------------------------------------------------------------------
MERCADO PAGO*SUPERMERCADO                $12,345.67      1        2025-07-24 10:30:00
NETFLIX.COM                              $4,899.00       1        2025-07-25 14:45:00
UBER *TRIP                               $2,150.50       1        2025-07-26 09:15:00
------------------------------------------------------------------------------------------
SUBTOTAL VISA:                           $19,395.17

=== MASTERCARD ALERTS ===
Comercio                                 Importe         Cuotas   Fecha        Hora
------------------------------------------------------------------------------------------
MERPAGO*RESTAURANT                       $8,750.00       1        28/07/2025   20:30
YPF ESTACION                             $15,000.00      1        29/07/2025   11:45
FARMACIA DEL PUEBLO                      $3,299.90       3        30/07/2025   16:20
------------------------------------------------------------------------------------------
SUBTOTAL MASTERCARD:                     $27,049.90

✓ Datos exportados a: transacciones_20250805_143022.csv
  Total de transacciones: 6
```

## 📁 Estructura del Proyecto

```
AlertaConsumos/
├── .venv/              # Entorno virtual (creado por uv o pip)
├── main.py             # Script principal
├── pyproject.toml      # Configuración del proyecto y dependencias (uv)
├── uv.lock            # Lockfile con versiones exactas (uv)
├── requirements.txt    # Dependencias para pip (compatibilidad)
├── .gitignore         # Archivos ignorados por Git
├── README.md          # Este archivo
└── transacciones_*.csv # Archivos CSV generados (ignorados por Git)
```

### Archivos importantes

#### Archivos de uv
- **`pyproject.toml`**: Configuración central del proyecto
- **`uv.lock`**: Garantiza versiones exactas de dependencias
- **`.python-version`**: Define la versión de Python del proyecto

#### Archivos de compatibilidad
- **`requirements.txt`**: Para usuarios de pip tradicional

## 🔧 Gestión de Dependencias

### Con uv

```bash
# Agregar nueva dependencia
uv add pandas

# Actualizar todas las dependencias
uv sync --upgrade

# Ver dependencias instaladas
uv pip list

# Generar requirements.txt actualizado
uv pip freeze > requirements.txt
```

### Trabajar con diferentes versiones de Python

```bash
# Fijar versión de Python
uv python pin 3.11

# Listar versiones disponibles
uv python list

# Instalar versión específica
uv python install 3.11
```

## 🔐 Seguridad

- ✅ Las credenciales de Gmail se almacenan localmente y están excluidas del repositorio
- ✅ Los archivos CSV con información financiera se ignoran automáticamente
- ✅ El `uv.lock` garantiza versiones seguras y consistentes de dependencias
- ⚠️ **Nunca compartas** tus archivos de credenciales (`token.pickle`, `gmail_token.json`)

## 🐛 Solución de Problemas

### Problemas con uv

#### Comando uv no encontrado
```bash
# Verificar instalación
which uv

# Agregar al PATH si es necesario
export PATH="$HOME/.cargo/bin:$PATH"
```

#### Limpiar y reinstalar
```bash
rm -rf .venv uv.lock
uv sync
```

### Problemas con Gmail

#### Error de autenticación
1. Elimina `token.pickle` y `gmail_token.json`
2. Ejecuta nuevamente: `uv run python main.py`

#### No encuentra emails
- Verifica que la fecha en `DATE` sea correcta
- Revisa la carpeta de spam en Gmail
- Confirma que tienes emails posteriores a la fecha especificada

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Instala dependencias: `uv sync`
4. Desarrolla y prueba: `uv run python main.py`
5. Commit: `git commit -m 'Agrega nueva funcionalidad'`
6. Push: `git push origin feature/nueva-funcionalidad`
7. Abre un Pull Request

## 📚 Enlaces Útiles

- 📖 [Documentación de uv](https://github.com/astral-sh/uv)
- 📧 [SimplegGmail Docs](https://github.com/jeremyephron/simplegmail)
- 🔍 [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- 🐍 [Python Packaging Guide](https://packaging.python.org/)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Disclaimer

AlertaConsumos es una herramienta de uso personal. Asegúrate de cumplir con:
- Los términos de servicio de Gmail
- Las políticas de privacidad de tu proveedor de email
- Las regulaciones locales sobre manejo de datos financieros

---

💡 **Tip**: Para soporte o sugerencias, abre un [issue](https://github.com/tu-usuario/AlertaConsumos/issues) en GitHub.
