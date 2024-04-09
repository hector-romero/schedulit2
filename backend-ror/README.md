# Schedulit

For this backend, I though it was going to be interesting and simpler, from a data handling perspective, to share the
same database used by the Django app. That would mean that every bit of information, user accounts, etc is going to 
be the same in both places, so I can switch backends freely in the frontend and still see the same data but provided by 
either python or django.

This decision forces me to veer a bit out of the standard way of handling objects and their conection with the database 
in Rails, but for the purposes of the demonstration of my ability of work with RoR and ruby, I consider it to be a
good compromise.

```sh
rails new . --api --skip-keeps --skip-action-mailer --skip-action-mailbox --database=postgresql --skip-action-text --skip-active-job  --skip-active-storage  --skip-action-cable  --skip-hotwire --skip-asset-pipeline --skip-javascript
```


# Importing models from django db
https://codeburst.io/how-to-build-a-rails-app-on-top-of-an-existing-database-baa3fe6384a0

```
    rails generate scaffold User password:string last_login:timestamptz is_superuser:boolean email:string is_staff:boolean is_active:boolean date_joined:timestamptz employee_id:string name:string role:string --no-migration
```



# README

This README would normally document whatever steps are necessary to get the
application up and running.

Things you may want to cover:

* Ruby version

* System dependencies

* Configuration

* Database creation

* Database initialization

* How to run the test suite

* Services (job queues, cache servers, search engines, etc.)

* Deployment instructions

* ...
