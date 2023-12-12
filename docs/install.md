For typical usage, a simple pip install will do the trick.

```bash
pip install settus
```

The main dependencies are:

* [`pydantic`](https://pypi.org/project/pydantic/): All laktory models derived from Pydantic `BaseModel`.
* [`pydantic-settings`](https://pypi.org/project/settus/): Cloud-based settings management system.

If you've got Python 3.8+ and `pip` installed, you're good to go. 
It is generally recommended to use a virtual environment for the installation. 


## Cloud-specific installation
To benefit from all features, we recommend also installing your cloud provider-specific dependencies:

* Microsoft Azure: 
    ```bash
    pip install settus[azure]
    ```

* Amazon Web Services (AWS)
    ```bash
    pip install settus[aws]
    ```

* Google Cloud Platform (GCP)
    ```bash
    pip install settus[gcp]
    ```

* Databricks
    ```bash
    pip install settus[databricks]
    ```
  
## Git-based installation
If you need or prefer installing Settus from git, you can use:
```bash
pip install git+https://github.com/okube-ai/settus.git@main
```
