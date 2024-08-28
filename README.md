# Tracking-films
Tracking-Films is a Telegram bot designed to help you keep track of movies you want to watch. This project is a pet project and allows users to easily manage their list of unwatched films.

## Features
- **Add Unwatched Films**: Add new movies to your unwatched list. Simply provide the movie title and genre, and the bot will store it for future tracking.
- **Delete Films**: Remove movies from your unwatched list. Specify the title of the movie you want to delete, and the bot will take care of it.
- **List All Movies**: Retrieve and view the complete list of unwatched movies. The bot will display all movies currently in your list in alphabetical order.

## Installation
1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Angelika2707/Tracking-films.git
    cd tracking-films
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables. Create a `.env` file in the project's root directory and add the following variables:

    ```env
    TOKEN=<your_telegram_bot_token>
    SQL_ALCHEMY_DATABASE_URI=<your_database_uri>
    ```
## Usage

To start the bot, run:

```bash
python main.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.