view here: https://kw-podcat.herokuapp.com

# podcat
Capital One Software Engineering Summit Submission

To solve this challenge, build a web application that provides:

Data Visuals: Display the podcasts returned via search function, as well as key information about each podcast returned. Similarly, display the podcasts a user is subscribed to, as well as information that user might want to know at a glance about the subscriptions.
<br>
**There is a search function both on the home screen and the navigation bar. Once the user types in a search term and clicks 'search', it will return a list of podcasts that fit that search term. There is a subscription page that displays the user's subscriptions. Both of these pages show the podcast objects with their logos, titles, number of subscribers, and descriptions, and the user can click the title to be taken to the podcast website. Both page's results can also be sorted either by the numbers of subscribers or alphabetically.**
<br>
<br>
Smart Searching: Give users the ability to search for podcasts by genre and by popularity.
<br>
**There is a categories page that allows the user to pick a category tag from a variety of options. Once the user clicks a tag, they will be taken to a page that displays podcasts that fit that tag. Both pages can be sorted by popularity or alphabetically. There is also a Top Podcasts page that displays a list of top podcasts by the most subscribers.**
<br>
<br>
Smart Sorting: Based on how frequently each subscribed podcast has new episodes, which subscribed podcasts should the user listen to first in order to avoid falling behind? Assume the user is subscribed to the top 25 podcasts.
<br>
**I wasn't able to find an API function that returned either the number of episodes or the frequency of episode posting. So I assumed the user was subscribed only to the top-25 podcasts and manually found the number of episodes that exist for each podcast, then sorted the top-25 podcasts by their content (number of episodes).**

