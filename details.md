
## The Details

Nothing is 100% required. The only true requirement is that something, in some form, be delivered to the team for consideration. Below we have a simple spec for the type of application we expect to work towards.

- Create new Rails application. Use the newest version (or use another version if you have a reason to do so. Be prepared to explain why in this case)

  - Ruby MRI would be standard but feel free to impress with the use of another runtime.

  - Postgres would match common Rails idioms and what we work with. It’s Ok to choose another database and we’d love to hear why.

- You will be creating a very simple version of our product. So, come up with a fun name. Pick whatever you want; be creative!

- This application can be a classic Rails web app. There’s no need to create an API or a single page application unless that’s your strong suit and you would like demonstrate that.

- The first step will likely be some level of authentication. Choose your own path here. Some ideas:

  - Use Devise and make a real local authentication/user system

    - Use OmniAuth and allow a Google/Facebook login

    - Implement auth yourself

    - Keep it simple and have the login simply check a hard-coded username/password. This is totally fine if you’d rather flex your muscles in other parts of the application.

- However you choose to implement authentication there should be the concept of “logging in” and “having a role”. The two roles we would like to see are “employee” and “scheduler”. These can be represented however you see fit. The only importance is the ability to have this distinction.

- When a user of role “scheduler” logs in they should be able to create, edit, update and destroy objects of type “User” and “Shift”.

  - Make a simple form to create a user. A user should have a name, an email and employee ID. Validate the email if you like. Validate further if you think you should. The “scheduler” should be able to create “employees”.

  - Make an “index” (list) of all users in the system. Only the “scheduler” should be able to see this list.

  - A “scheduler” should be able to choose an employee and create a “shift” for them. This can be a crude form that accepts a “start time” and “end time” and attaches it to the user. Things to consider:

    - How will these “shifts” be stored in the database?

    - What happens when multiple “shifts” overlap in date/time?

    - Is there a way to spruce up the form UX (think: datepicker UI, inline validation) using simple techniques?

- When a user of role “employee” logs in they should be able to read.

  - The default employee view should be a simple index listing of their shifts, with date and times.

  - It should be possible to click a shift within this listing to view a detailed page. At this time the “detailed” page may not have much additional information but the distinction between the “index” and “individual” views would be appreciated.

  - Bonus: allow the employee to “write” back in some way. Example: The employee can “acknowledge” the shift by clicking a button which flips a flag in the database; or maybe they can add “notes” to a shift.


### Additional Guidelines

- Feel free to grab a UI library like Bootstrap or SemanticUI for a quick way to make the project look and feel modern.

- No Javascript is required but any enhancements via Javascript are welcome. Interesting and advanced usage of Javascript may provide a real edge and will be evaluated if you choose to put some time/focus in this area. However, it is not expected or required.

- If any part of this task becomes a blocker or is taking longer than expected, feel free to make a quick note about the situation and move on. We’d rather see something incomplete with thoughts attached than nothing at all.

- We’re big on tests! We know asking for complete test coverage is over the top but an example of at least one interesting test can go a long way.


### Deployment/Delivery

- Please use your own private github repository. 

- A small effort to provide a few commits with well thought-out messages will go a long way to demonstrate basic source control and documentation hygiene.

- A deployed and running version of this application would be considered a bonus. If you have familiarity with Heroku then it shouldn’t take more than 5% of the total assignment time to have a version of this running on their free tier (please provide a link). If deployments and infrastructure is something you're passionate about feel free use another service and take this as far as you like.

## Summary

This assignment is designed with the intention of ensuring that candidates can comfortably pick up (or learn) the tools we use here at our company. Communication holds above-all-else for us and failure to achieve the a significant outcome will not be considered a failure if your thought process is documented and communicated back to us. This communication can live in your response email, code comments, git commit messages, a project “readme”, all of the above or otherwise; this is up to you. The more we can get a sense of how you approach issues and the thought processes involved, the better.

This assignment is also designed purposely to be somewhat vague. Creativity and a self-starting is important and needed within our team. There are certainly details missing within the specs for this assignment. Use your best judgement! That being said, please communicate these thoughts back to us; just don’t let anything completely block you.
