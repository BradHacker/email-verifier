# Email Verifier

Email verifier written in Python that utilizes SMTP to connect to a mail server and test if an email is valid.

## Setup

Run the following command to install the necessary dependencies.

`pip3 install -r requirements.txt`

## Getting started

Create an `input.txt` file containing **one email per line**

**Be sure to add a blank line at the end of the file**

Then, just run the program and wait:

```bash
$ python3 verifyemails.py
```

## Example `input.txt`

```
example@mail.example.com
randomemail123@gmail.com

```

## Example `output.csv`

```csv
example@mail.example.com,exists
randomemail123@gmail.com,doesn't exist
```