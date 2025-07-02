# Running the Python Flask Application

To start the Flask backend server on port **5000** (default):

```bash
cd scripts
flask --app flasker run --debug
```

This will launch the Python API at [http://localhost:5000](http://localhost:5000).

---

## Running on a Different Port

To start the Flask server on a different port (e.g., **5050**):

```bash
cd scripts
flask --app flasker run --debug --port 5050
```

This will launch the API at [http://localhost:5050](http://localhost:5050).