# Schedulit

For this backend, I thought it was going to be interesting and simpler, from a data handling perspective, to share the
same database used by the Django app. That would mean that every bit of information, user accounts, etc., is going to 
be the same in both places, so I can switch backends freely in the frontend and still see the same data but provided by 
either python or django.

This decision forces me to veer a bit out of the standard way of handling objects and their connection with the database 
in Rails, but for the purposes of the demonstration of my ability of work with RoR and ruby, I consider it to be a
acceptable compromise.

```sh
rails new . --api --skip-keeps --skip-action-mailer --skip-action-mailbox --database=postgresql --skip-action-text --skip-active-job  --skip-active-storage  --skip-action-cable  --skip-hotwire --skip-asset-pipeline --skip-javascript
```


# Importing models from django db
https://codeburst.io/how-to-build-a-rails-app-on-top-of-an-existing-database-baa3fe6384a0

```
    rails generate scaffold User password:string last_login:timestamptz is_superuser:boolean email:string is_staff:boolean is_active:boolean date_joined:timestamptz employee_id:string name:string role:string --no-migration
```


```
    rails generate scaffold Shift timestamp:timestamptz start_time:timestamptz end_time:timestamptz status:string employee:references --no-migration
```

```
    rails generate scaffold ShiftNote timestamp:timestamptz note:string shift:references --no-migration
```

```
    rails generate scaffold AuthToken created:timestamptz user:references expiry:timestamptz token_key:string --no-migration --primary-key-type=string
```


## Issues:

### Openssl issue with Ruby 3.0.6 in OSX
Error:

    Could not load OpenSSL.
    You must recompile Ruby with OpenSSL support or change the sources in your Gemfile from 'https' to 'http'. Instructions for
    compiling with OpenSSL using RVM are available at rvm.io/packages/openssl.

Solution: Just use ruby 3.0.0


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
