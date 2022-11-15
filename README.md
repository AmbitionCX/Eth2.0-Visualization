# Eth-Visualization

## Server

The server employs Flask to provide web services. 
All codes below should be run under the "server" folder.
The data folder is ignored due to data confidentiality. 
Please create a "data" folder by yourself (./server/data/).

### Server Setup

This project is created using Python 3.8.5. It is recommended to use virtualenv to build the project. 
For example, 

``` 
$ apt install python3.8-venv

# Create a new virtualenv named "venv"
$ python -m venv venv

# Activate the virtualenv (OS X & Linux)
$ source venv/bin/activate

# Activate the virtualenv (Windows)
$ venv\Scripts\activate

# Deactivate the virtualenv
$ deactivate
```

For this project, we will be installing flask and jupyter lab to facilitate development. Install the dependencies using:

```
# Install the specified dependencies
$ pip install -r requirements.txt

# Export your own dependencies
$ pip freeze > requirements.txt
```

### Server activation

The default address for the server is http://127.0.0.1:5000/

```
$ python run.py
```


## Client

The client services are provided by Vue 3 and Vite. 
All codes below should be run under the "client" folder.

### Client Setup

The packages are handled by npm, and specified in the package.json.

```
$ npm install
```

### Client activation

The client is served at http://localhost:3000/.
Notice that the framework supports hot-reloads, so that the changes on DOM are applied automatically and do not require reloads.

```
# Compiles and hot-reloads for development
$ npm run dev

# Compiles and minifies for production
$ npm run build
```
