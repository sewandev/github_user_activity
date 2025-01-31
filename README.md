# GitHub User Activity CLI

This is a simple command-line tool that fetches and displays recent GitHub activity for a given user. The idea for this project is inspired by the challenge available at [GitHub User Activity Project](https://roadmap.sh/projects/github-user-activity).

## Usage

Run the script with a GitHub username as an argument:

```sh
python script.py <github-username>
```

## Features

- Fetches recent GitHub events for a user.
- Displays up to 5 events with an option to see more.
- Supports event types like `PushEvent`, `IssuesEvent`, and `WatchEvent`.
- Handles invalid usernames and connection errors gracefully.

## Requirements

- Python 3
- No external libraries required

## License

This project is open-source and available for use under the MIT License.