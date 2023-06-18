# Integrated Healthcare System

The Integrated Healthcare System (IHS) is a Django-based web application aimed at streamlining and improving the communication between healthcare providers (doctors and nurses) and patients. It facilitates scheduling appointments, managing prescriptions, and maintaining a real-time chat system for direct communication.

This documentation covers the `chat` module of the system. The chat module is built on Django Channels, providing real-time WebSocket communication. 

## Chat Module

The `chat` module is responsible for the chat functionality between the users of the system, which could be patients or health practitioners. The real-time communication feature is facilitated by WebSockets and Django Channels. 

The two main classes in this module are `ChatConsumer` and `NotifConsumer`.

### `ChatConsumer`

This class handles the connections, disconnections, message reception, and message sending in the chat. Here's a brief overview of its main methods:

- `connect()`: This method handles the connection process when a client connects to the WebSocket. It identifies the user and the chat room they are connecting to.

- `disconnect()`: This method handles the disconnection process. It ensures the client is removed from the group chat when they disconnect.

- `receive()`: This method is triggered when a message is received from the WebSocket. It takes the incoming message and sends it to the group chat.

- `chat_message()`: This method handles the process of sending a message to the client.

- `post_message()`: This is a helper method that creates a new message in the database.

### `NotifConsumer`

This class handles the real-time delivery of notifications to users.

- `connect()`: This method handles the connection process. It identifies the user and adds them to a notification group.

- `receive()`: This method is triggered when a notification is received from the WebSocket.

- `notification()`: This method handles the process of sending a notification to the client.

- `get_notif()`: This is a helper method that retrieves all unseen notifications for a user from the database.

The core of these classes is the use of Django Channels for managing WebSockets, enabling real-time, bidirectional communication between the server and the client.

## Core Module

The core part of this Django-based healthcare system is responsible for handling main functionalities such as user authentication, managing user profiles, and implementing different REST APIs to ensure smooth communication between frontend and backend. 

It manages various healthcare related models including `Insurance`, `Patient`, `Doctor`, `Treatment`, `Message`, `Follower`, `Clinic`, `Appointment`, `Review`, `Disease`, `Speciality`, `Medicine`, and `Notification`. Corresponding serializers for these models are also provided.

### API Viewsets:

- `InsuranceViewSet`: This viewset handles CRUD operations for Insurance data, and allows searching insurances by their organization names.
- `PatientViewSet` and `DoctorViewSet`: These viewsets deal with CRUD operations for Patients and Doctors. It supports searching patients/doctors by name.
- `UserViewSet`: It handles user-related operations, including creating, updating, and deleting users.
- `TreatmentViewSet`: This viewset manages CRUD operations for Treatments.
- `MessageViewSet`: This viewset handles operations related to Messages between users. It supports filtering messages by sender and receiver.
- `FollowerViewSet`: It handles operations for Follower model. It allows filtering followers by follower and followee.
- `CustomObtainAuthToken`: This custom view handles user authentication and token generation. It also fetches and responds with related user information upon successful authentication.
- `ClinicViewSet` and `ClinicDoctorViewSet`: These viewsets manage operations for Clinics and ClinicDoctor data respectively.
- `AppointmentViewSet`: This viewset handles CRUD operations for Appointments. It allows filtering appointments by doctor, specialty, start time, and end time.
- `ReviewViewSet`: This viewset is responsible for CRUD operations related to Reviews.
- `DiseaseViewSet`, `SpecialityViewSet`, and `MedicineViewSet`: These viewsets manage CRUD operations for Diseases, Specialties, and Medicines respectively.
- `NotificationViewSet`: It manages CRUD operations for Notifications and allows filtering notifications by user.

Please refer to the code for a more detailed understanding of how these viewsets operate. Each viewset is defined by extending Django's `ModelViewSet` and implementing necessary methods to perform CRUD operations.

**Note:** In this code, `DefaultsMixin` is used to provide additional default behaviors to the viewsets such as pagination, filtering, and ordering, while `OwnerMixin` is used to enforce object-level permissions, where users can only modify their own data. Please ensure these mixins are implemented correctly in your application.

## Getting Started

Sure, here's a step-by-step guide to get this Django REST application up and running:

1. **Ensure you have Python installed**: This project requires Python 3, which can be checked using the command `python --version` in your terminal. If you don't have Python installed, you can download it from [the official Python website](https://www.python.org/downloads/).

2. **Setup a virtual environment (optional, but recommended)**: A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated Python environments for them. This can be setup using the venv module that comes with Python 3. 

   - To create a virtual environment, run: `python3 -m venv env`
   - To activate the environment, run: `source env/bin/activate` (on Windows use: `env\Scripts\activate`)

3. **Install Django and Django REST Framework**: After setting up the virtual environment, you can install Django and Django REST Framework using pip, the Python package installer.

   - `pip install django djangorestframework`

4. **Install the project dependencies**: In the project directory, there should be a file named `requirements.txt` that lists the dependencies for this project. You can install these using pip.

   - `pip install -r requirements.txt`

5. **Set up the database**: Django comes with a built-in database abstraction layer that supports a wide range of databases. By default, Django uses SQLite. You can configure your database in `settings.py` file located in the project directory.

   - Apply the database migrations using following command: `python manage.py migrate`

6. **Running the server**: You can start the development server using Django's command-line utility.

   - `python manage.py runserver`

7. **Access the application**: Open your web browser and visit http://127.0.0.1:8000/ to see the application running.

8. **Create an admin user (optional)**: Django's admin is a powerful, production-ready administration interface. To access it, you first need to create a superuser account.

   - `python manage.py createsuperuser`, then follow the prompts.

Please note that the exact steps may vary based on your operating system and the configuration of your Django project.

For the **Procfile** and **runtime.txt**, they are used when deploying the Django application on platforms like Heroku. The `Procfile` is used to declare what commands are run by your application's dynos on the Heroku platform, while `runtime.txt` is used to specify the python version to be used. You don't need them for local development. 

This guide should get you started with running the Django REST project. However, based on the specific needs of your application, you might need to perform additional setup tasks such as configuring the settings for third-party apps or setting up environment variables.
