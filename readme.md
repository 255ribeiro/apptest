
# Criação de webapp com o framework dash 

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

1. criar ambiente virtual no pythonanywhere:
   
    ```
    mkvirtualenv env --python='/usr/bin/python3.8'

    ```
1. Instalar pacotes via pip e arquivo requirements.txt:
   
    ```shell
    pip install -r requirements.txt
    
    ```

1. Conteúdo do arquivo  WSGI para dash_app

    ```python

    import sys

    project_home = '/home/user_foo/appfolder_bar'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path

    from appfile_baz import app
    application = app.server

    ```
