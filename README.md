# ciat-alliance

Para iniciar la aplicacion:

1. Iniciar Docker Compose:

`docker-compose up --build`

El proceso tardará un poco la primera vez mientras instala las dependencias y procede a crear la base de datos.

Prueba Tecnica: 

    En un esfuerzo por mejorar la eficiencia y sostenibilidad de la agricultura local, una organización de apoyo a los campesinos desea desarrollar un sistema de monitoreo de actividades agronómicas en fincas. Este sistema ayudará a los campesinos a llevar un registro detallado de sus actividades diarias, tales como siembra, riego, fertilización, cosecha, y otras labores agrícolas. El objetivo es proporcionar a los campesinos una herramienta que les permita optimizar sus procesos y tomar decisiones informadas basadas en datos históricos y actuales.
    Para llevar a cabo esta iniciativa, se cuenta con las siguientes bases de datos debidamente pobladas:

    - Actividades Agronómicas: registros de actividades con fecha, tipo de actividad, insumos utilizados, y duración.
    - Parcelas de la Finca: detalles de cada parcela con ubicación (latitud, longitud), tamaño, y tipo de cultivo actual.

    Con esta información, se busca desarrollar un sistema de información que permita a los campesinos visualizar y gestionar sus actividades agronómicas, facilitando el monitoreo y la toma de decisiones en su finca. Su misión es diseñar y desarrollar un sistema de información que permita a los campesinos monitorear y gestionar sus actividades agronómicas diarias en su finca. La solución debe ser fácilmente desplegable usando una imagen de Docker.

    Como entregables se solicita lo siguiente:

    - Defina el alcance de su solución
    - Lista de requerimientos debidamente clasificados
    - Arquitectura de software de la solución propuesta
    - Modelo de la base de datos (pueder SQL o NoSQL)
    - Sistema de información que ayude a la solución

## Alcance de la Solución

El sistema de monitoreo de actividades agronómicas permitirá a los campesinos:

- Registrar y gestionar sus actividades diarias en la finca.
- Visualizar las actividades realizadas en cada parcela.
- Tomar decisiones informadas basadas en datos históricos y actuales.

## Lista de Requerimientos

### Requerimientos Funcionales

1. **Usuarios y Niveles de Permisos:**
   - Autenticación de usuarios.
   - Roles y permisos (admin, campesinos).

1. **Gestión de Actividades Agronómicas:**
   - Registrar nuevas actividades (siembra, riego, fertilización, cosecha, etc.) (Admin).
   - Editar actividades existentes. (Admin)
   - Visualizar actividades por fecha y tipo.

2. **Gestión de Parcelas:**
   - Registrar y actualizar detalles de cada parcela (ubicación, tamaño, tipo de cultivo) (Admin).
   - Visualizar parcelas en un mapa.

3. **Reportes y Análisis:**
   - Generar reportes de actividades por parcela y por tipo de actividad.
   - Visualizar tendencias y estadísticas de actividades agronómicas.


### Requerimientos No Funcionales

1. **Usabilidad:**
   - Interfaz de usuario intuitiva y fácil de usar.
   - Accesibilidad en dispositivos de escritorio.

2. **Desempeño:**
   - Respuesta rápida en el registro y visualización de datos.
   - Capacidad de manejar múltiples usuarios concurrentemente.

3. **Escalabilidad:**
   - Facilidad para añadir nuevas funcionalidades.
   - Soporte para grandes volúmenes de datos.

4. **Seguridad:**
   - Protección de datos sensibles.
   - Control de acceso basado en roles.

## 3. Arquitectura de Software de la Solución Propuesta

### Componentes Principales

1. **Frontend:**
   - Aplicación web responsiva usando Dash (React/Python).
   - Interfaz gráfica para la gestión de actividades y parcelas.

2. **Backend:**
   - API RESTful desarrollada en Python (framework Flask).
   - Control de autenticación y autorización.
   - Lógica de negocio para el manejo de actividades y parcelas.

3. **Base de Datos:**
   - Sistema de gestión de bases de datos relacional MySQL.

4. **Docker:**
   - Imágenes Docker para el despliegue del frontend, backend y base de datos.
   - Archivo `docker-compose.yml` para la orquestación de los servicios.

### Diagrama de Arquitectura

```
          +-------------------+
          |                   |
          |     Frontend      |
          |       (Dash)      |
          |                   |
          +---------+---------+
                    |
                    | REST API
                    |
          +---------+---------+
          |                   |
          |      Backend      |
          |      (Flask)      |
          |                   |
          +---------+---------+
                    |
                    |
          +---------+---------+
          |                   |
          |    Base de Datos  |
          |      (MySQL)      |
          |                   |
          +-------------------+
```

## 4. Modelo de la Base de Datos (MySQL)

### Tablas

1. **usuarios**
2. **parcelas**
3. **actividades**

#### Tabla `usuarios`

```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'campesino') NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla `parcelas`

```sql
CREATE TABLE parcelas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    latitud DECIMAL(9, 6) NOT NULL,
    longitud DECIMAL(9, 6) NOT NULL,
    tamaño DECIMAL(10, 2) NOT NULL,
    tipo_cultivo VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

#### Tabla `actividades`

```sql
CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parcela_id INT NOT NULL,
    fecha TIMESTAMP NOT NULL,
    tipo_actividad VARCHAR(255) NOT NULL,
    insumos_utilizados TEXT,
    duracion INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcela_id) REFERENCES parcelas(id) ON DELETE CASCADE
);
```