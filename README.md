# [AuctionApp](https://django-auction-app.herokuapp.com/)

### Challenges that I have faced.

-   Step1: In the first step main challenge was authenticating the use with their email address. Firstly, I did a query with the given email address. If any user exists with this email, log in to the user. If not, create a new user. And the email address is unique in the Database.

-   Step2: Step two was pretty easy for me. For the auction gallery, I did a query for all the products. Then loop through the query for displaying all the items. Added a form for creating a new auction item. And did some conditional rendering for My posted items and logout menu.

-   Step3: In this step, the challenge was auction expiration. Here, I compared the end date with today's date and I got the expiration status.

-   Step4: Here, the challenge was declared the winner. So I did an aggregation on the total bid for the auction and, I got the winner with max bid price.

-   Step5: The most challenging step in the whole project was this step. I created an admin dashboard for all the statistics. For the first chart, I did a query for counting the auction item by created date. I used chart.js for displaying the chart. I was not 100% clear about what to do and for me, this was quite complex. But, if I get some hint, I believe I'll do that.

-   Step6: Designing is always a challenging part for me. I was focused on functionality. But I did the minimum design.

-   Step7: I am familiar with Heroku and this step was not challenging at all for me.
