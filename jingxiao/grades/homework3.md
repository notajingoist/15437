homework3 Feedback
==================

Commit graded: `2314d5bc8a23b6bbe0962e19b22859a938b38374`

### Version control - Git (6/10)
  * -4, Commit messages should adequately describe what occurs in your commits. For example, definitely avoid messages like "asdflkjsadf" and "blah some user profile stuff".

### Iterative design (10/10)

### Implementation and functionality (69/85)

##### Routing and configuration (urls.py/settings.py)

##### Models (models.py)

##### Views (views.py)
  * -10, There is no search feature
  * -0, Be careful not to make needless queries. Your `views.py` queries `TextPosts` on line 43, and then re-queries on line 44. 
  * -1, You should only be calling `.save()` once; your `save_profile_changes` method, for example, should only call `user.save` right before rendering, rather than every time a field is updated. 
  * -0, Don't use `get_or_create` for things that need to find something. If you're trying to edit the logged in user, for example, you shouldn't create the user if it doesn't exist. 
  * -5 No use of the query API (e.g. `text_contains`)
  
##### Authentication

##### Templates

### Additional feedback
  * There is no way to navigate from a user's profile page away to another page. 
  * You may want to consider adding consistent navigation between pages. 
  * Your site looks really, really nice. If you'd like help setting up live-reload for things like less precompiling, let me know. 

---

#### Total score (85/105)

---

Graded by: Salem Hilal (salem@cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/jingxiao/blob/master/grades/homework3.md
