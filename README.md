<h1 align="center">daily-diary-backend ⚙️</h1>
<p align="center">
    <img src="https://i.imgur.com/2UulD71.png" alt="daily-diary-web">
</p>

<h4 align="center">
Backend code for Daily Diary built with Flask, OAuthLib, Supabase, 
PyCryptodome and Flask-JWT-Extended</h4>

<div style="text-align:center;">
  <a href="https://github.com/aditya76-git">aditya76-git</a> /
  <a href="https://github.com/aditya76-git/daily-diary-backend">daily-diary-backend</a>
</div>

<br />

## Description

This repository contains the backend code for a journaling web app called Daily Diary. It serves as the API that facilitates communication between the client and the server, handling various operations such as user authentication, diary entry management, category handling, and streak tracking.

## Auth Routes

| **Route**                     | **Request Type** | **Description**                                                                                                                                                                                            | **Token Required**  |
| ----------------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `/auth/signup`                | POST             | Registers a new user. Validates required fields and email format. Returns a success message if the user is added, or an error message if fields are missing, email is invalid, or username already exists. | No                  |
| `/auth/login`                 | POST             | Authenticates a user using their username and password. Returns access and refresh tokens if successful, or an error message if the credentials are invalid.                                               | No                  |
| `/auth/login/google`          | GET              | Initiates Google OAuth login by generating and returning a redirect URL.                                                                                                                                   | No                  |
| `/auth/login/google/callback` | GET              | Handles the callback from Google OAuth. Retrieves user info from Google, logs the user in, or registers them if they don’t already exist. Returns tokens and redirects to the client.                      | No                  |
| `/refresh`                    | GET              | Refreshes the user's access token using the refresh token. Returns a new access token.                                                                                                                     | Yes (Refresh Token) |

## User Routes

| **Route**            | **Request Type** | **Description**                                                                                                                                                                        | **Token Required** |
| -------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `/user/info`         | GET              | Retrieves the current user's details, including username, email, profile picture, categories, user ID, and account creation date.                                                      | Yes                |
| `/user/add-category` | POST             | Adds a new category to the user's account. Requires the category name in the request body.                                                                                             | Yes                |
| `/user/add-entry`    | POST             | Adds a new journal entry. Requires title, description, emoji, category, sharing settings, and slug. Encrypts the title and description, generates search tokens, and stores the entry. | Yes                |
| `/user/edit-entry`   | POST             | Edits an existing journal entry. Allows updating the title, description, emoji, category, sharing settings, and slug. Encrypts fields if they are provided.                            | Yes                |
| `/user/list-entries` | GET              | Lists all journal entries for the current user, optionally filtered by a query parameter.                                                                                              | Yes                |

## Streak Routes

| **Route** | **Request Type** | **Description**                                                                          | **Token Required** |
| --------- | ---------------- | ---------------------------------------------------------------------------------------- | ------------------ |
| `/check`  | GET              | Checks the current streak status for the logged-in user. Returns the streak information. | Yes                |
| `/add`    | GET              | Adds a day to the user's streak, effectively updating the streak status.                 | Yes                |

## 🌟 Show Your Support

- If you find this project useful or interesting, please consider giving it a star on GitHub. It's a simple way to show your support and help others discover the project.

## 💻Authors

- Copyright © 2024 - [aditya76-git](https://github.com/aditya76-git) / [daily-diary-backend](https://github.com/aditya76-git/daily-diary-backend)
