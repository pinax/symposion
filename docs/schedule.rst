Schedule App
===========

The ``schedule`` app allows staff members to create the schedule for the 
conference's presentations, breaks, lunches, etc.

The ```schedule``` app has a number of models that facilitate building the
structured schedule:

  * Schedule: A high level container that maps to each Conference Section.
  * Day: A Day associated with a Schedule.
  * Room: A Room associated with a Schedule. 
  * Slot Kind: A type of Slot associated with a Schedule.
  * Slot: A discrete time period for a Schedule.
  * Slot Room: A mapping of a Room and Slot for a given Schedule.
  * Presentation: A mapping of a Slot to an approved Proposal from the ```proposals``` app.

Schedule Builder Form
---------------------

It can be cumbersome to generate a schedule through the admin. With that in mind,
a generic schedule builder is available via a Schedule's edit view. For instance,
if a Conference site has a Talks Section and Schedule, the form would be
available for Staff at::

/schedule/talks/edit

The form consumes a structured CSV file, from which it will build the schedule. 
Sample CSV data is included below::

"date","time_start","time_end","kind"," room "
"12/12/2013","10:00 AM","11:00 AM","plenary","Room2"
"12/12/2013","10:00 AM","11:00 AM","plenary","Room1"
"12/12/2013","11:00 AM","12:00 PM","talk","Room1"
"12/12/2013","11:00 AM","12:00 PM","talk","Room2"
"12/12/2013","12:00 PM","12:45 PM","plenary","Room1"
"12/12/2013","12:00 PM","12:45 PM","plenary","Room2"
"12/13/2013","10:00 AM","11:00 AM","plenary","Room2"
"12/13/2013","10:00 AM","11:00 AM","plenary","Room1"
"12/13/2013","11:00 AM","12:00 PM","talk","Room1"
"12/13/2013","11:00 AM","12:00 PM","talk","Room2"
"12/13/2013","12:00 PM","12:45 PM","plenary","Room1"
"12/13/2013","12:00 PM","12:45 PM","plenary","Room2"

It is worth noting that this generates the **structure** of the schedule. It 
does not create Presentation objects. This will need to be done manually.

One can also **delete** an existing schedule via the delete action. This is
irreversible (save for a database restore).
