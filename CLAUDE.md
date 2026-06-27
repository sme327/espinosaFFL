CLAUDE.md

Project Identity

This project is a kid-friendly Fantasy Football Museum / Clubhouse for our family league.

It is not a serious analytics dashboard first. It is a playful, colorful, Saturday-morning-cartoon fantasy football world that preserves family history, celebrates winners, tracks rivalries, and gives the kids fun things to explore over time.

Think:

* Saturday morning cartoons
* Backyard Football
* ESPN for Kids
* Pixar energy
* Family scrapbook
* Fantasy football clubhouse
* Museum, but with confetti

The app should feel approachable for kids, funny for adults, and meaningful as a long-term family memory project.

League Context

This is a family fantasy football league.

Current players:

* Shawn
* Jennifer
* Daphne
* Elliot

Future player:

* Wyatt, once he is old enough to understand the game better

League format:

* Redraft
* Snake draft
* Simplified rosters
* Simplified scoring
* Built for kids and family fun, not hardcore fantasy optimization

Core Purpose

The project should do four things well:

1. Preserve league history over time
2. Celebrate each season’s winner
3. Make the league fun for kids to revisit
4. Build toward family rivalries, jokes, achievements, and traditions

The site should help us eventually say things like:

* “Daphne always beats Dad in Week 3.”
* “Elliot has the best team names.”
* “Jennifer is the quiet dynasty.”
* “Wyatt joined late but caused chaos.”
* “Shawn talks the most and loses anyway.”

Product Philosophy

Every page should answer a fun question.

Examples:

* Who won this year?
* Who has the most championships?
* Who had the funniest team name?
* Who drafted the best player?
* Who had the worst luck?
* Who is Dad’s biggest rival?
* Who has the best playoff record?
* Which kid has the most trophies?
* What silly thing happened this season?
* What achievements did each person unlock?

Avoid pages that feel like plain databases. Stats are welcome, but they should support stories.

Design Principles

1. Kid-Friendly First

Use bright, warm, playful design. Avoid dense tables when possible. Prefer cards, badges, trophies, helmets, mascots, stickers, football fields, comic-style panels, and visual summaries.

2. Celebrate Everyone

Even the last-place team should have something fun to celebrate.

Examples:

* Best Team Name
* Chaos Champion
* Biggest Upset
* Best Draft Pick
* Most Loyal Fan
* Rivalry Troublemaker
* Comeback Kid
* Almost Had It Award

3. History Should Feel Like a Scrapbook

The site should feel like a family memory book that happens to use fantasy football data.

Use season recaps, funny notes, champion cards, rivalry blurbs, and “remember when?” moments.

4. Unlocks and Achievements Matter

Achievements should be playful and collectible.

Examples:

* First Win
* Beat Dad
* Beat Mom
* Sibling Showdown Winner
* Draft Day Genius
* Upset Alert
* Playoff Bound
* Champion
* Rivalry Starter
* Mascot Collector
* Trash Talk Apprentice

5. Smack Talk, But Sweet

The tone can be funny and competitive, but never mean.

Use playful rivalry language:

* “Daphne has officially entered her villain era.”
* “Dad is requesting a recount.”
* “Jennifer quietly built a monster.”
* “Elliot’s team name remains undefeated.”
* “Wyatt is scouting from the sidelines.”

Suggested App Sections

Home / Clubhouse

The landing page should feel like the family league headquarters.

Possible sections:

* Current champion
* League scoreboard
* This year’s teams
* Trophy case preview
* Latest achievement unlocks
* Rivalry spotlight
* Fun family quote or joke
* Season countdown / current week status

Champions Hall

A kid-friendly Hall of Champions.

Each champion should get:

* Big trophy card
* Team name
* Manager
* Record
* Championship matchup
* Fun season tagline
* Optional photo/avatar/mascot
* “How they won” story

Season Archive

Each season gets its own scrapbook page.

Include:

* Final standings
* Champion
* Runner-up
* Team names
* Draft highlights
* Best players
* Biggest upset
* Funny notes
* Awards
* Rivalry moments

Team Pages

Each family member should have a manager profile.

Include:

* Avatar
* Team name history
* Championships
* Best season
* Funniest season
* Rivalries
* Achievements
* Favorite players
* Signature style

Rivalries

This should become one of the most fun pages.

Track:

* Shawn vs Daphne
* Shawn vs Elliot
* Shawn vs Jennifer
* Daphne vs Elliot
* Daphne vs Jennifer
* Elliot vs Jennifer
* Eventually Wyatt vs everyone

Each rivalry page/card should include:

* Head-to-head record
* Biggest win
* Closest game
* Playoff meetings
* Current bragging rights
* Funny rivalry tagline

Trophy Case

A visual awards room.

Include serious and silly awards:

* League Champion
* Regular Season Champion
* Best Draft
* Biggest Upset
* Best Team Name
* Most Chaotic Team
* Comeback Kid
* Rivalry Winner
* Dad Slayer
* Mom Magic
* Sibling Champion
* Almost Champion

Achievement Book

A collectible sticker-book style page.

Achievements should look like badges/stickers. Locked achievements can appear greyed out or hidden.

Draft Day

Since this is a snake draft, focus on stories instead of advanced draft analytics.

Track:

* Draft order
* First-round picks
* Best pick
* Funniest pick
* “Oops” pick
* Kid-favorite players
* Draft steals
* Draft regrets

Player Card Gallery

Create football-card style visuals for notable players.

Possible card types:

* Family Favorite
* Championship Hero
* Draft Steal
* Heartbreaker
* Rivalry Villain
* Playoff Legend

League Timeline

A simple visual timeline of major family league moments.

Examples:

* League founded
* First champion
* First kid win over parent
* First sibling rivalry
* First undefeated week
* Wyatt joins
* First repeat champion

Data Philosophy

Start simple. Do not over-engineer.

Core data should probably include:

* seasons
* managers
* teams
* matchups
* standings
* champions
* draft picks
* achievements
* rivalry records
* season notes
* awards

Prefer CSV or simple JSON files early unless the app clearly needs a database.

Data should be easy for Shawn to update manually at first.

Tone and Copy Style

Use playful, warm, family-friendly writing.

Good examples:

* “The trophy has a new home.”
* “Dad is already making excuses.”
* “Sibling rivalry loading…”
* “A new challenger enters the clubhouse.”
* “This matchup had big cartoon villain energy.”
* “The championship confetti has fallen.”
* “The standings are getting spicy.”
* “Somehow, Mom did it again.”

Avoid:

* Overly corporate language
* Dense analytics jargon
* Gambling-style language
* Mean insults
* Pages that feel like ESPN stat tables only

Technical Guidance

Build iteratively.

Prioritize:

1. Clear navigation
2. Reusable components
3. Easy data updates
4. Fun visual design
5. Mobile-friendly layout
6. Kid-readable pages
7. Simple storytelling over complex analytics

Use Streamlit unless otherwise specified.

Recommended structure:

family_ffl_clubhouse/
  app.py
  data/
    seasons.csv
    managers.csv
    teams.csv
    matchups.csv
    standings.csv
    draft_picks.csv
    achievements.csv
    awards.csv
    rivalries.csv
    notes.csv
  components/
    cards.py
    trophies.py
    badges.py
    navigation.py
    charts.py
  pages/
    home.py
    champions.py
    seasons.py
    managers.py
    rivalries.py
    trophy_case.py
    achievements.py
    draft_day.py
  assets/
    avatars/
    mascots/
    trophies/
    backgrounds/
  README.md
  CLAUDE.md

Visual Direction

The visual language should be playful and bold.

Suggested motifs:

* Football field backgrounds
* Trophy cards
* Sticker badges
* Cartoon avatars
* Helmet icons
* Confetti
* Scoreboard panels
* Trading cards
* Comic-book bursts
* Locker-room signs
* Backyard football field vibes

Use rounded cards, large headers, emoji where appropriate, and simple visual hierarchy.

Important Product Rule

Whenever adding a feature, ask:

Would one of the kids understand this?
Would this be fun to look back on in five years?
Does this create a family story?

If not, simplify it or make it more playful.