# FRUTA
## Elevate your small fruit business with our innovative web application

### Link : http://fruta.therealayman.tech/home
Fruta is a cloud-enabled, mobile-ready, online-storage compatible,
inventory organizer.

- Add Products to your inventory
- Add Your Clients
- Keep Track of your Orders

## Made by: [Ayman Ammar](https://github.com/AymanAegon), [OUSSAMA SEFIANI](https://github.com/ODSEFIANI)
## Features

- Create an account for free
- Add as many products as you want.
- Organize you clients and orders.
- Watch your business Grow

Elevate your small fruit business with our innovative web application, streamlining order management, optimizing inventory tracking, and enhancing client communication. Experience newfound efficiency and organization as our user-friendly tool becomes your go-to solution for effortlessly managing orders, purchases, and client relationships. Join a thriving community of sellers who have transformed their businesses, and revolutionize your fruit business journey today!


## Tech

Fruta uses a number of open source projects to work properly:

- [HTML/CSS] - HTML & CSS enhanced for web apps!
- [jQuery] - Great for some of the functionalities(i.e. backToTop..)
- [Bootstrap] - For EASY and styling.
- [Python] - duh.
- [Flask] - For backend logics.
- [Nginx/Gunicorn] - for handling your http requests.

And of course Fruta itself is open source with a [public repository](https://github.com/AymanAegon/FRUTA)
 on GitHub.

## Installation & Usage

Just clone it bro :)

and run this
```sh
cd FRUTA
python3 main.py
```

oh, and if you using it for production
it's better to create a MySQL Database using this mysql setup file "[setup_mysql_dev.sql](https://github.com/AymanAegon/FRUTA/blob/master/setup_mysql_dev.sql)"
and then run ```main.py``` file with these environment variables:

| Environment variable | Purpose |
| ------ | ------ |
| FRUTA__MYSQL_USER | A database user name |
| FRUTA__MYSQL_PWD | The user's password |
| FRUTA__MYSQL_HOST | The host |
| FRUTA__MYSQL_DB | Database name |
| FRUTA__TYPE_STORAGE | set to ```"db"``` if using database, else ```""```  |
