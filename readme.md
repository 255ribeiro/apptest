
# Criação de webapp

Intruções para criação de um webapp

## No computador 

1. Use alguma ferramenta para criação de ambientes virtuais no python. caso não possua nenhuma instale:

    * exemplo: virtualenv

        ```

        pip install virtualenv

        ```

1. Crie uma pasta para seu app 


    ```
    mkdir my_dash_app
    cd my_dash_app
    ```


2. Initialize Git
    
    ```

    git init

    ```

3. Crie e ative um abiente virtual(WINDOWS)
   
   ```
   python -m virtualenv venv

   .\venv\Scripts\activate 

   ```
4. instale as dependências utilizadas pelo web app
   * exemplo:

    ```
    pip install dash, dash-auth, dash-renderer, dash-core-components, dash-html-components, plotly, pandas, numpy, patool

    ```
5. Crie um arquivo requirements.txt

    ```
    pip freeze > requirements.txt

    ```

6. push to github

## Python Anywhere instructions:

[https://www.pythonanywhere.com](https://www.pythonanywhere.com)

1. Iniciar um console bash 
   
<br>

2. Clonar repositório do app:

    ```
    git clone https://github.com/foo/bar.git

    ```

3. criar ambiente virtual no pythonanywhere:
   
    ```
    mkvirtualenv env --python='/usr/bin/python3.8'

    ```
4. Instalar pacotes via pip e arquivo requirements.txt:
   
    ```
    pip install -r requirements.txt
    
    ```
