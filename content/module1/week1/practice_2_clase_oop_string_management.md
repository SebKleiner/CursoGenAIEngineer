# OOP en Python para Tareas de Generative AI - Práctica (45 minutos)

## Descripción

En esta sesión práctica, aplicarás los conceptos de Programación Orientada a Objetos (OOP) y gestión de strings en Python para resolver problemas específicos relacionados con tareas de Inteligencia Artificial Generativa (GenAI). A través de ejercicios detallados, consolidarás tu comprensión teórica y aprenderás a implementar soluciones eficientes y escalables utilizando clases avanzadas y técnicas de manipulación de strings.

## Objetivos

- **Implementar clases avanzadas en Python** para estructurar componentes de GenAI.
- **Aplicar principios de OOP** como herencia, polimorfismo y encapsulación en proyectos de GenAI.
- **Manipular y gestionar strings** de manera efectiva para la generación y procesamiento de texto.
- **Desarrollar patrones de diseño** aplicables a tareas específicas de GenAI.
- **Integrar prácticas de OOP y gestión de strings** en un mini-proyecto de GenAI.

## Actividades

### 1. Creación de Clases Avanzadas

#### **Ejercicio 1: Definición de Clases Base y Subclases**

**Objetivo:** Definir una clase base `ModeloGenerativo` y crear subclases especializadas que implementen funcionalidades específicas para diferentes modelos de GenAI.

**Instrucciones:**

1. **Define la clase base `ModeloGenerativo`** con los siguientes atributos y métodos:
    - **Atributos:**
        - `nombre` (str): Nombre del modelo.
        - `version` (str): Versión del modelo.
    - **Métodos:**
        - `__init__(self, nombre, version)`: Constructor para inicializar los atributos.
        - `cargar_modelo(self)`: Método para cargar el modelo (implementación vacía).
        - `generar_texto(self, prompt)`: Método para generar texto basado en un prompt (implementación vacía).

    ```python
    class ModeloGenerativo:
        def __init__(self, nombre, version):
            self.nombre = nombre
            self.version = version
        
        def cargar_modelo(self):
            # Código para cargar el modelo
            pass
        
        def generar_texto(self, prompt):
            # Código para generar texto basado en el prompt
            pass
    ```

2. **Crea una subclase `ModeloGPT`** que herede de `ModeloGenerativo` y añada un atributo `api_key` para la autenticación con la API de GPT. Sobrescribe el método `generar_texto` para utilizar una API específica de GPT.

    ```python
    class ModeloGPT(ModeloGenerativo):
        def __init__(self, nombre, version, api_key):
            super().__init__(nombre, version)
            self.api_key = api_key
        
        def generar_texto(self, prompt):
            # Implementación específica para GPT
            # Por ejemplo, realizar una llamada a la API de OpenAI
            texto_generado = f"Texto generado por {self.nombre} versión {self.version} para el prompt: {prompt}"
            return texto_generado
    ```

#### **Ejercicio 2: Implementación de Encapsulación y Propiedades**

**Objetivo:** Utilizar la encapsulación para proteger los atributos y proporcionar métodos getter y setter para acceder y modificar los atributos de manera controlada.

**Instrucciones:**

1. **Modifica la clase `ModeloGenerativo`** para hacer que los atributos sean privados y añade métodos getter y setter.

    ```python
    class ModeloGenerativo:
        def __init__(self, nombre, version):
            self._nombre = nombre
            self._version = version
        
        @property
        def nombre(self):
            return self._nombre
        
        @nombre.setter
        def nombre(self, valor):
            self._nombre = valor
        
        @property
        def version(self):
            return self._version
        
        @version.setter
        def version(self, valor):
            self._version = valor
        
        def cargar_modelo(self):
            # Código para cargar el modelo
            pass
        
        def generar_texto(self, prompt):
            # Código para generar texto basado en el prompt
            pass
    ```

2. **Verifica la encapsulación** intentando acceder y modificar los atributos directamente y a través de los métodos getter y setter.

    ```python
    modelo = ModeloGenerativo("BaseModel", "1.0")
    print(modelo.nombre)  # Acceso a través del getter
    modelo.nombre = "BaseModelUpdated"  # Modificación a través del setter
    print(modelo.nombre)
    
    # Intento de acceso directo (debería no ser recomendado)
    print(modelo._nombre)  # Aunque posible, es una mala práctica
    ```

### 2. Gestión de Strings

#### **Ejercicio 3: Limpieza y Formateo de Prompts**

**Objetivo:** Implementar métodos dentro de las clases para limpiar y formatear prompts antes de enviarlos a los modelos generativos.

**Instrucciones:**

1. **Añade un método `limpiar_prompt`** en la clase `ModeloGenerativo` para realizar operaciones de limpieza en el string del prompt.

    ```python
    class ModeloGenerativo:
        # ... (código anterior)
        
        def limpiar_prompt(self, prompt):
            prompt = prompt.strip()  # Eliminar espacios en blanco al inicio y al final
            prompt = prompt.capitalize()  # Capitalizar la primera letra
            # Añadir más operaciones de limpieza si es necesario
            return prompt
    ```

2. **Utiliza el método `limpiar_prompt`** en la subclase `ModeloGPT` antes de generar el texto.

    ```python
    class ModeloGPT(ModeloGenerativo):
        # ... (código anterior)
        
        def generar_texto(self, prompt):
            prompt_limpio = self.limpiar_prompt(prompt)
            # Implementación específica para GPT utilizando prompt_limpio
            texto_generado = f"Texto generado por {self.nombre} versión {self.version} para el prompt: {prompt_limpio}"
            return texto_generado
    ```

3. **Prueba el método de limpieza** con diferentes entradas de prompts.

    ```python
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", "tu_api_key")
    prompt_usuario = "  escribe un poema sobre la inteligencia artificial  "
    prompt_limpio = modelo_gpt.limpiar_prompt(prompt_usuario)
    print(f"Prompt limpio: '{prompt_limpio}'")
    ```

#### **Ejercicio 4: Formateo Dinámico de Prompts**

**Objetivo:** Crear métodos que permitan construir prompts dinámicamente utilizando plantillas y variables.

**Instrucciones:**

1. **Añade un método `formatear_prompt`** en la clase `ModeloGenerativo` que acepte una plantilla y un diccionario de variables para formatear el prompt.

    ```python
    class ModeloGenerativo:
        # ... (código anterior)
        
        def formatear_prompt(self, plantilla, variables):
            try:
                prompt_formateado = plantilla.format(**variables)
                return prompt_formateado
            except KeyError as e:
                print(f"Error: Falta la variable {e} en el diccionario de variables.")
                return plantilla
    ```

2. **Implementa el método en la subclase `ModeloGPT`** y pruébalo con diferentes plantillas y variables.

    ```python
    class ModeloGPT(ModeloGenerativo):
        # ... (código anterior)
        
        def generar_texto(self, plantilla, variables):
            prompt_formateado = self.formatear_prompt(plantilla, variables)
            prompt_limpio = self.limpiar_prompt(prompt_formateado)
            # Implementación específica para GPT utilizando prompt_limpio
            texto_generado = f"Texto generado por {self.nombre} versión {self.version} para el prompt: {prompt_limpio}"
            return texto_generado
    ```

3. **Ejemplo de uso:**

    ```python
    plantilla = "Escribe un artículo sobre {tema} que incluya {punto_clave}."
    variables = {
        "tema": "la inteligencia artificial en la educación",
        "punto_clave": "los beneficios de personalizar el aprendizaje"
    }
    
    texto = modelo_gpt.generar_texto(plantilla, variables)
    print(texto)
    ```

### 3. Patrones de Diseño

#### **Ejercicio 5: Implementación del Patrón Singleton**

**Objetivo:** Asegurar que solo exista una instancia de `ModeloGenerativo` durante la ejecución del programa utilizando el patrón Singleton.

**Instrucciones:**

1. **Define una metaclase `SingletonMeta`** que controle la creación de instancias y asegure que solo una instancia exista.

    ```python
    class SingletonMeta(type):
        _instances = {}
        
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]
    ```

2. **Aplica la metaclase a la clase `ModeloGenerativo`** para convertirla en un Singleton.

    ```python
    class ModeloGenerativo(metaclass=SingletonMeta):
        def __init__(self, nombre, version):
            self._nombre = nombre
            self._version = version
        
        # ... (resto de la clase)
    ```

3. **Verifica el patrón Singleton** creando múltiples instancias y comprobando que todas apuntan a la misma instancia.

    ```python
    modelo1 = ModeloGenerativo("BaseModel", "1.0")
    modelo2 = ModeloGenerativo("BaseModel", "1.0")
    
    print(modelo1 is modelo2)  # Debería imprimir: True
    ```

#### **Ejercicio 6: Implementación del Patrón Factory**

**Objetivo:** Utilizar el patrón Factory para crear instancias de diferentes modelos generativos de manera flexible.

**Instrucciones:**

1. **Define una clase `ModeloFactory`** que tenga un método estático `crear_modelo` para instanciar diferentes tipos de modelos generativos.

    ```python
    class ModeloFactory:
        @staticmethod
        def crear_modelo(tipo, nombre, version, **kwargs):
            if tipo == "GPT":
                return ModeloGPT(nombre, version, kwargs.get("api_key"))
            elif tipo == "OtroModelo":
                # Implementar otras subclases si existen
                pass
            else:
                raise ValueError(f"Tipo de modelo '{tipo}' no reconocido.")
    ```

2. **Utiliza la fábrica para crear instancias de modelos** sin necesidad de conocer las clases específicas.

    ```python
    modelo_gpt = ModeloFactory.crear_modelo(
        tipo="GPT",
        nombre="GPT-4",
        version="v1.0",
        api_key="tu_api_key"
    )
    
    print(modelo_gpt.nombre)  # Debería imprimir: GPT-4
    ```

### 4. Mini-Proyecto: Generador de Textos Personalizado

**Objetivo:** Desarrollar una aplicación sencilla que permita al usuario ingresar un prompt y genere texto utilizando clases avanzadas basadas en OOP. Implementa funcionalidades como limpieza del prompt, generación de texto y manejo de múltiples modelos generativos.

**Instrucciones:**

1. **Define la clase `GeneradorTextos`** que gestionará múltiples modelos generativos.

    ```python
    class GeneradorTextos:
        def __init__(self):
            self.modelos = []
        
        def agregar_modelo(self, modelo):
            if isinstance(modelo, ModeloGenerativo):
                self.modelos.append(modelo)
            else:
                raise TypeError("El modelo debe ser una instancia de ModeloGenerativo.")
        
        def generar(self, plantilla, variables):
            textos = {}
            for modelo in self.modelos:
                texto = modelo.generar_texto(plantilla, variables)
                textos[modelo.nombre] = texto
            return textos
    ```

2. **Implementa la aplicación principal** que interactúa con el usuario para recibir prompts y mostrar textos generados.

    ```python
    def main():
        # Crear instancias de modelos
        modelo_gpt = ModeloGPT("GPT-4", "v1.0", "tu_api_key")
        # Puedes agregar más modelos si los tienes
        # modelo_otro = OtroModelo("OtroModel", "v2.0", "otro_api_key")
        
        # Crear el generador de textos y agregar los modelos
        generador = GeneradorTextos()
        generador.agregar_modelo(modelo_gpt)
        # generador.agregar_modelo(modelo_otro)
        
        # Interacción con el usuario
        while True:
            print("=== Generador de Textos Personalizado ===")
            plantilla = input("Ingresa una plantilla de prompt (o 'salir' para terminar): ")
            if plantilla.lower() == 'salir':
                break
            num_variables = int(input("¿Cuántas variables deseas ingresar? "))
            variables = {}
            for _ in range(num_variables):
                clave = input("Nombre de la variable: ")
                valor = input(f"Valor para '{clave}': ")
                variables[clave] = valor
            
            # Generar textos
            resultados = generador.generar(plantilla, variables)
            
            # Mostrar resultados
            for nombre, texto in resultados.items():
                print(f"\nModelo: {nombre}\nTexto Generado:\n{texto}\n")
    
    if __name__ == "__main__":
        main()
    ```

3. **Ejemplo de uso:**

    - **Plantilla ingresada por el usuario:**
        ```
        Escribe una historia sobre {tema} que incluya {detalle}.
        ```
    - **Variables ingresadas por el usuario:**
        - `tema`: "la exploración espacial"
        - `detalle`: "descubrimientos sorprendentes"
    - **Texto generado:**
        ```
        Texto generado por GPT-4 versión v1.0 para el prompt: Escribe una historia sobre la exploración espacial que incluya descubrimientos sorprendentes.
        ```

## Relación con Generative AI

Estos ejercicios prácticos te permitirán aplicar directamente los conceptos de OOP y gestión de strings en el desarrollo de aplicaciones de Generative AI. Al estructurar tu código de manera orientada a objetos, facilitarás la extensión y mantenimiento de tus proyectos de GenAI. Además, una gestión eficiente de strings es esencial para crear prompts efectivos y procesar las respuestas generadas por los modelos de lenguaje.

## Conclusión

Al finalizar esta sesión práctica, habrás adquirido habilidades clave para implementar soluciones orientadas a objetos en Python, optimizadas para tareas de Generative AI. Estarás preparado para desarrollar aplicaciones más complejas y eficientes, aprovechando al máximo las capacidades de la programación orientada a objetos y la gestión de strings en el contexto de la inteligencia artificial generativa.

---
