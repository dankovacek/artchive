# The Artchive Project

A platform for documenting, archiving, and studying street art.

## 1.0 Running the application in local a development envioronment

#### Install Dependencies for Python (2.7) Development Environment

Follow the setup portion of this [DigitalOcean tutorial.](https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications).

See `requirements.txt`

Start the development server from the root directory (/artchive):
`$ python run.py`

A few notes on how this is is set up:

<ul>
<li>For my webhost, Nearlyfreespeech.net, an 'index' file of some
sort must be included in the /public folder.</li>
<li>There are a few ways to accomplish the above point, and
my approach is to create the shell script run.sh, which calls
only one function, run.py.</li>
<li>In calling the 'app' module in run.py  (from protected import app),
__init__.py is called.  '__init__.py' sets the app configuration file,
sets 'secret key', registers module blueprints, and initializes the Flask app instance, creates the database, sets template and static resource folders, and contains a 404 error handler.
</li>
<li>Registering the default_module blueprint imports the main
functions of the controller code, where routing occurs, where
models are called, and where the views are executed.</li>
</ul>


## 2.0 Background and Inspiration
Photographing street art has been an interest of mine for years.  I have photos from Europe, West Africa, and across North, Central, and South America.

While still working full time as a mechanical engineer, I completed a Frontend web development program through Udacity.com. My favourite project in the program was the "Neighbourhood Map" Project, where I made a tool for myself to create my own street art walking tour wherever I went.  My project reviewers gave excellent feedback and it was cool to see screen captures of how my UI looked in Riga, Latvia, and in Brooklyn, NY.

I integrated the Flickr and Google Maps APIs to populate a local map view of where street art could be seen.  Photos were all posted publicly by Flickr users.

After quitting my job and taking on programming studies full-time, I finally got around to figuring out the backend and putting my app live on the web.  I tried walking around and visiting some of the street art my app pulled in.  The first time I toured around my neighbourhood, downtown Vancouver, I was amazed to be unable to find a single piece that still existed.  Some were painted over, some were removed entirely, and many were on walls that no longer existed, or had been obscured by new construction.  The pieces I was most familiar with from my walks around town were no longer there.  Beautiful, building-scale murals depicting traditional First Nation styles were no longer a part of the visual fabric of the city.

Street art is meant to be ephemeral, but art is an important way to describe a time and place, and a unique perspective and voice speaking about urban life.

The Artchive Project is intended to capture the stories about city life told by locals for the purpose of pure creative expression or protest.  It creates a timeline for the story of urban transformation.

### 2.1 Pictograph

Around the world, prehistoric nomads drew pictographs to communicate migratory routes, sources of food, water, etc.  Today, the rare surviving pictographs are prized artifacts of great academic importance for understanding the function of ancient peoples, their customs, development, interactions, etc. prior to the development of written language.

### 2.2 Hoboglyph

With the emergence of a national railway in the latter half of the 19th century, a combination of social and environmental factors produced a growing population of impoverished transient workers who used the railways as transit.  The great depression saw a sharp rise in the population of hobos in North America, and transient populations today are estimated at 20K.  The inherent danger in this lifestyle necessitated a complex and cryptic symbology for navigating life in the fringes of society.  (Illiteracy among the working classes and a necessity to evade interpretation of authorities).  Today, these symbols are rare and important artifacts for archiving a history of a relatively poorly documented portion of society.

### 2.3 Totem

(Totem poles have been stolen from native communities.  Totems are sculpture stories, so Project Graffiki includes in its scope the documentation of sculpture and installation.

(Ketchikan story, visiting totem museum.  Who was that Hollwood-type that stole a prominent Coastal totem for his livingroom?)

(It is understood that some art is ephemeral, but what issues exist with
non-destructive, (non-invasive?  minimally invasive?) photo (& video-graphic?!)
documentation of street art and not-for-profit installation.

### 2.4 Graffiti

From vandalism to high art, urbanization, globalization, mass migration, conflict, and explosive population growth, intermingling of language, music, art, etc. have created an incredibly diverse and constantly changing and evolving body of street art.  The incredible volume and transient nature of this massive body of self-expresson is perfectly suited to modern tools of crowd-sourcing and digital archiving.

-Culture and public perception of street art


## 3.0 Executive Summary

The Artchive Project is archiving tool for documenting street art of various forms.  It's also a tool to study the diversity of artistic styles in local and regional contexts, a means of tracking the evolution of artistic styles over time, a system of documentation for modern uses of symbology (protest, artistic expression, contemporary urban life).

## 4.0 UI/UX, Not Yet Organized Thoughts

Database population:
* crowdsourcing the documentation process,
* encouraging participation by gamifying the documentation and validation
processes <a href="https://www.reddit.com/wiki/faq#wiki_how_is_a_submission.27s_score_determined.3F">(think Reddit 'upvotes')</a>,
* include supporting documentation by crowd-crafted 'wiki'-style articles

_User Aquisition_
This is a tough one.
* outreach for documenting first nations art.

Try out the <a href="https://github.com/dankovacek/P5-1-hoodmap">Graffoto prototype</a>.  Visit any city on the globe and witness the sheer
volume of street art documented by users of Flickr.

<div class="flex">
<img src="/public/graffikiapp/static/images/UIlandscape.jpg"><img src="/public/graffikiapp/static/images/UImobileprofile.jpg">

</div>
## Thoughts on UI, Database Design, Archiving Art

**Map View**
Colour encoding map pins to convey time:
* Pins should be colour coded to indicate the age of verification
* 'red' means hasn't been verified in ~>1 year **or** unverified
* 'orange' means hasn't been verified in ~>6 months
* 'yellow' means hasn't been verified in ~>3 months
* 'green' means verified 1 > and < 3 months
* 'blue' means 'new', added < 1 month ago

**User**
A User database will track:
* contributions of photography (flicks),
* comments, i.e. information related to the piece, the artist,
a movement, etc.
* 'like' or verification (see Quality Assurance below)
* **must not track** personal information
* Following initial registration with Oauth process, users can
voluntarily provide additional information and customize their
own profile
* can follow and be followed

**Piece**
A Piece is a single work of art,
* track when photos were taken
* track verifications of location
* track status of piece, i.e. unaltered from most current photo

**Archiving**
Quality standards should be applied to the documentation of a work.  For example:
* if contained, the name of the artist should be visible
* minimum resolution
* the entire work in one frame (what about fine details?)
* the date the photo was taken
* the piece 'type' (installation, graffiti, etc.)
* **geolocation** (lat/long) is required.  App should check if location services
is on, and have a backup methodology for archiving photos taken with other equipment and edited later (to allow for higher caliber photography equipment and software to be used)
* as the intent is to represent the piece as it exists in situ, filters might
skew the original intent of the artist.  More research is required on maintaining
the integrity of the work in its environment.

_Quality Assurance_
The 'quality assurance' aspect of photo documentation can employ
a Reddit-style 'rating'or 'approval' system.  By publishing
carefully crafted quality standards,the PG community will self-
filter the best images.  A Reddit-style points system
can encourage participation, similar to the 'treasure hunt'
spirit of the Geocaching
community.

**UI/UX**
(insert example graphic from Graffoto)
A mobile-first application will primarily display a map of locations and a
list-view of results returned by the bounds described by the map window.

_Menu_
A menu 'burger will slide to reveal standard links:
* profile,
* messaging, and
* an extra large camera icon to bring up camera for documenting a piece

**Messaging**
Users should be able to communicate and receive notifications when:
-a piece or location they have documented or verified is commented on
-a piece or location they have documented is verified or 'liked'
-new photos are submitted documenting the location ID

## 5.0 License

I don't expect government or academia to fund such a thing, especially as a tool created by some goon Canadian engineer who knows not his ass from his anthropology nor his art, but as the original idea is to create a useful tool for archiving a visual history and language, input from art historians and anthropologists is invaluable and should be sought.


## 6.0 Budget

Prepare a project schedule detailing:
* phasing of application features
* budget breakdown
(who to consult for budget?)

**Register Project Graffiki as a not-for-profit?**

_________

## N.0 Tangents

This framework could be carried over for the documentation of oral histories, traditional songs, etc.

* Think crowd-sourced Lomax Project
* Obstacles include a reluctance to be recorded, data access?
*
