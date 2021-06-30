# middleman
## Installation

### Clone the repository

``` git clone https://github.com/middleman-api/middleman.git ```

### Setup project

Create the virtual env

``` python3 -m venv env ```

``` source env/bin/activate ```


Install the packages

``` pip install -r requirements.txt ```

#### Configure postgres

Assuming postgres in installed in the system

```

$ sudo su - postgres
postgres@server:~$ createuser --interactive -P
Enter name of role to add: middleman
Enter password for new role: middlemanpassword
Enter it again: middlemanpassword
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n
postgres@server:~$ createdb --owner middleman middleman
```

### Running the project

```

uvicorn middleman.main:app --reload --host 0.0.0.0

```

### View api doc

Visit http://127.0.0.1:8000/docs#/ once the project is running
