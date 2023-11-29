# Anime Database

This application operates on an anime database composed of three CSV files, each containing specific tables:

- **Anime table**: Contains information about anime.
- **Rating table**: Contains information about users' rating activities.
- **Userauth table**: Contains information about user roles and credentials.

The application runs an API with five endpoints, all utilizing the GET method. They are divided into two categories:

- Public Tops: Includes endpoints that retrieve publicly available top lists from the anime database.
- User-related Tops: Includes endpoints that retrieve lists about anime rated by specific users.

The User-related Tops category incorporates authentication and authorization for users:

- Users must provide a username and key to authenticate against the API.
- Users have access to resources based on their roles:
  - Admins can access the rating lists of every user.
  - Others can only access rating lists of themselves.

The application also provides a logging mechanism that logs every request with a timestamp,
along with other request and response-related data, to a JSON file.
