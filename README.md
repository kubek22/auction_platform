# Auction Platform

This is an academic project for building an online auction system using Django.

## Content
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This is a web application designed for online auctions, allowing users to create, bid on, and manage auctions. 
It provides an environment for buying and selling items through an auction process.

## Features

- **User authentication:** Secure user authentication system for registration, login, and access control.

- **Assigning items:** Users can create items, representing objects to put up on auctions, specifying details such as item description and image.

- **Auction listings:** Users can create auctions of their items, defining entry price and duration.

- **Bidding system:** Real-time bidding functionality allowing users to place bids on active auctions, with automatic bid updates.

- **Watcher list:** Every user can track status of all his auctions and auction he took part in.

- **Winner determination:** The system automatically determines the highest bidder and declares them the winner when an auction ends.

- **Admin panel:** Django admin panel for easy management of users, items and auctions.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/django-auction-platform.git
    cd django-auction-platform
    ```

2. Create a virtual environment:
    ```
    python -m venv venv
    ```

3. Activate the virtual environment:
    ```
    venv\Scripts\activate
    ```

4. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

5. Create a media directory to store uploaded images:
    ```
    mkdir media
    ```

6. Apply migrations:
    ```
    python manage.py migrate
    ```

7. Create a superuser for admin access:
    ```
    python manage.py createsuperuser
    ```

8. Run the development server:
    ```
    python manage.py runserver
    ```
   
9. Run the command for processing finished auctions in a separate local terminal: 
    ```
    python manage.py process_tasks
    ```

10. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage

- Navigate to the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

- Users can register, log in and log out.

- Every visitor has access to the main page and can view auctions listed there.

- Only authenticated users can bid on auctions.

- After logging in, user has access to their items panel and auctions panel.

- In items panel, user can create new items and see all their items added before.

- In auctions panel, user can monitor all their auctions and all auctions they bid on.
