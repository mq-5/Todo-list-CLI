# Features 🎯🥇🏆

- [x] The user can run your program from the command line.
- [x] The user can see all todos from the command line by passing a list command, sorted with the ones due first.
- [x] The user can add a todo from the command line by passing an add argument. The fields specified should be body,due_date, and project_id. The fields due_date and project_id are optional. Only body is required.
- [x] By default todos are incomplete.
- [x] The user should see a message giving information about the todo that was added.
- [x] User can mark a todo as complete by passing a command and an id.
- [x] User can mark a todo as incomplete by passing a command and an id.
- [x] If the user does not supply the correct arguments, or supplies a --help flag, the user sees a usage message.
- [x] The user can supply arguments to the list command to only see todos that are complete.

## Optional Requirements

- [x] The user can supply arguments to the list command to only see todos of a particular project_id.
- [x] The user can supply arguments to the list command to reverse the default sort, to now see the todos by due_date - descending.
- [x] The user can supply arguments to the list command to combine the above options.
- [x] The user can add a user_id to each todo.
- [x] The user can add a user to the system by passing add_user. Each user should have a name, email_address, and id.
- [x] The user can call a list_users command that shows all the users in the system.
- [x] The user can call a staff command that shows each project, combined with each of the users working on that project.
- [ ] The user can call a who_to_fire command that lists all users who are not currently assigned a todo.
- [x] The user can add a project by calling add_project. Each project must have a name.
- [ ] The user can see all projects from the command line.
