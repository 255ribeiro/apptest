
# Criação de *webapp* com o *framework* dash 

Instruções para criação de um *webapp*

## No computador 

1. Use alguma ferramenta para criação de ambientes virtuais no ```Python```.
   <br>

    * Pode-se utilizar o ```virtualenv```. Caso ainda não esteja instalado: 
        <br>

        ```shell

        pip install virtualenv

        ```

2. Crie uma pasta para seu app 
    <br>

    ```shell
    mkdir my_dash_app
    cd my_dash_app
    ```
    <br>


3. Inicialize o ```git```
   <br>
    
    ```shell

    git init

    ```

4. Crie e ative um ambiente virtual (WINDOWS)
   <br>
   
   ```shell
   python -m virtualenv venv

   .\venv\Scripts\activate 

   ```
5. instale as dependências utilizadas pelo web app
   * exemplo:

    ```shell
    pip install dash, dash-auth, dash-renderer, dash-core-components, dash-html-components, plotly, pandas, numpy, patool

    ```
6. Crie um arquivo requirements.txt

    ```shell
    pip freeze > requirements.txt

    ```

7. push to github

## No [Python Anywhere:](https://www.pythonanywhere.com)

1. Iniciar um console bash 
   
<br>

2. Clonar repositório do app:
   <br>

    ```shell
    git clone https://github.com/foo/bar.git

    ```

3. criar ambiente virtual no pythonanywhere:
   <br>
   
    ```shell
    mkvirtualenv env --python='/usr/bin/python3.8'

    ```
4. Instalar pacotes via pip e arquivo requirements.txt:
   
    ```shell
    pip install -r requirements.txt
    
    ```

5. Conteúdo do arquivo  WSGI para dash_app

    ```python

    import sys

    project_home = '/home/user_foo/appfolder_bar'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path

    from appfile_baz import app
    application = app.server

    ```
