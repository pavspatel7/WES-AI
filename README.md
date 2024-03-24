# Devpot Link: https://devpost.com/software/wesai

# Project Setup Instructions

This guide will walk you through setting up the project environment, installing necessary dependencies, and running the project.

## Setting Up the Virtual Environment

We recommend using `conda` to manage your virtual environments. If you haven't already, [install Anaconda or Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) on your system.

1. **Create the Virtual Environment:**

    Run the following command to create a new virtual environment named `myenv` with Python 3.12.0:

    ```
    conda create -n myenv python=3.12.0
    ```

2. **Activate the Virtual Environment:**

    Once the environment is created, activate it using:

    ```
    conda activate myenv
    ```

## Installing Dependencies

With your virtual environment activated, install the project dependencies using `pip`. 

Run the following commands to install each required package:

```
pip install flask
pip install Django
pip install sentence_transformers
pip install django-cors-headers
```


## Running the Project

Before running the project for the first time, you'll need to apply migrations to your database. Then, you can start the development server.

1. **Apply Migrations:**

    ```
    python manage.py migrate
    ```

2. **Start the Development Server:**

    Run the following command to start the Django development server:

    ```
    python manage.py runserver
    ```

    The server will start on `http://127.0.0.1:8000/` by default. Open your web browser and navigate to this URL to view the application.

## Troubleshooting

- If you encounter any issues with package versions, consider adjusting the version numbers in the installation commands based on your specific requirements or compatibility concerns.
- Ensure that the `conda` environment is activated whenever you're working on the project to keep dependencies isolated and manageable.

---

Thank you for setting up the project! If you have any questions or encounter any issues, please feel free to reach out for support.

![Alt text](Images/p1.png "What is Chat Bot name?")
![Alt text](Images/p2.png "Asking Location")
![Alt text](Images/p3.png "General Information")
