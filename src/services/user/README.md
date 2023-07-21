# User Sub-application

This sub-application is responsible for managing users API.

## Models

### `User`

* **Code:**
  The user model is defined in `services/user/models/user.py` and is used to store user information.
* **Information:**
    * This model overrides the default `django.contrib.auth` model to give more flexibility to the user.
    * It has to be imported in `services/user/models/__init__.py` for migrations to detect it automatically.
* **DB-Signals:**
    * `post_save`: This signal is used to create a **verification-token** for the user when it is created.

## API

### `GET /users`:

* **Authentication:** Required
* **Required Permissions:**
    * `view_user`
* **Description:** This endpoint returns a list of users who are
  in the same organization as the user who is making the request.

### `GET /users/:id`

### `POST /users`

### `PUT /users/:id`

### `DELETE /users/:id`




