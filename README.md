# Fine Furnishings
![Fine Furnishings - Am I Responsive](static/readme_images/am-i-responsive.png)

Fine Furnishings is a B2C focused online furniture store that will provide it's users a relaxing and trustworthy experience when purchasing new home furnishings. The goal of Fine Furnishings is to provide quality furniture to our customers as well as a seamless online experience that will provide them with peace of mind when purchasing from our company.

So many online experiences leave the user hesitating to make a purchase or stumbling through a website that is not user friendly. As we know how significant our surroundings and atmosphere are, our goal here, is to ensure that the user has easy accessibility to all the answers of any questions they may be asking when purchasing new furniture. If their question is not easily answered, we will provide an easy system of contact for the user to ask their specific question. 

Our goal is to provide simple navigation of the website so that our customers can purchase quality furniture from a trustworthy business.

# User Experience (UX)

## Project Planning

<details>

<summary> User Stories</summary>

- Planning of user stories completed in Google sheets:
[Google sheet](https://docs.google.com/spreadsheets/d/1xrrFyjqHdzZsPyJ-DnGmsfV3z4rvsZ0ZD8F23ye3utk/edit#gid=0)
- Link to my [GitHub Project](https://github.com/users/morganoleary/projects/5)

</details>

<details>

<summary>ERD Diagram - Lucidchart</summary>

![LucidChart ERD](static/readme_images/erd-diagram-min.png)

</details>

<details>

<summary>Wireframes - Justinmind</summary>

- The wireframes for this project were created on the Justinmind local development environment for MacOS. Due to the time constraints for completing this project, I did not have the time to implement all device sizes for each page's wireframes. The mockups for these pages were used as a guide for the project as I continued to style more and adjust the project during project creation and coding.

![Home Page Mobile](static/readme_images/wf-home-page-mobile.png)
![Home Page Tablet](static/readme_images/wf-home-page-tablet.png)
![Home Page Desktop](static/readme_images/wf-home-page-desktop.png)
![Product Options Mobile](static/readme_images/wf-product-options-mobile.png)
![Product Options Tablet](static/readme_images/wf-product-options-tablet.png)
![Product Options Desktop](static/readme_images/wf-product-options-desktop.png)
![Product Page Mobile](static/readme_images/wf-product-page-mobile.png)
![Product Page Tablet](static/readme_images/wf-product-page-tablet.png)
![Product Page Desktop](static/readme_images/wf-product-page-desktop.png)
![User Wishlist Mobile](static/readme_images/wf-user-wishlist-mobile.png)
![User Personal Details Mobile](static/readme_images/wf-user-personal-details-mobile.png)
![Shopping Cart Mobile](static/readme_images/wf-shopping-cart-mobile.png)
![Checkout Page Mobile](static/readme_images/wf-checkout-page-mobile.png)

</details>

<details>

<summary>Design</summary>

- Using the color Red - psychology of color
I used the color Red as it has been proven to boost online sales. While the site has a red overall color, I created a more muted version to keep the site classy and more elegant for a more peaceful shopping experience. More information on this was found at [Crazy Egg](https://www.crazyegg.com/blog/colors-proven-to-boost-sales/).
- The content of the project was created by myself. I found the images and created the descriptions, pricing, etc. on all products. The content from the FAQs page is also created by me as an example of what I would like to see from a furniture store if I were the consumer.

</details>

## Marketing:

<details>

<summary>E-Commerce Business Model</summary>

- Fine Furnishings uses a business to consumer (B2C) business model. This is a furniture company that provides quality furniture to customers throughout the island of Ireland. The value of the company's services is huge as it provides a better well-being to everyone's day-to-day living within their homes. The business supplies furniture for consumers, customers are able to make purchases of the furniture on the Fine Furnishings website and the company is able to process orders via the website to complete each order placed.

</details>

<details>

<summary>SEO Implementations</summary>

- Descriptive meta tags & keywords were used throughout the site. In particular, the product descriptions and image file names.
- sitemap.xml
- robots.txt

</details>

<details>

<summary>Facebook Screenshots</summary>

![Facebook Screenshot #1](static/readme_images/facebook-1-min.png)
![Facebook Screenshot #2](static/readme_images/facebook-2-min.png)
![Facebook Screenshot #3](static/readme_images/facebook-3-min.png)
![Facebook Screenshot #4](static/readme_images/facebook-4-min.png)
![Facebook Screenshot #5](static/readme_images/facebook-5-min.png)

</details>

# Features

<details>

<summary>Existing Features</summary>

- Home page
- Navbar
- User login/registration
- User Wishlist
- User Personal Details
- Product Search Bar
- Product Categories & Filtered pages
- Home page product category blocks
- Product Detail page for each product
- Shopping Cart page to view before purchasing
- Secure Checkout page for the user to checkout with Stripe
- Footer links
- Mailchimp Subscription form working to store contact emails on Mailchimp:
![Mailchimp - successful emails added](static/readme_images/mailchimp-success.png)
- Custom 404 page

#### External Links in Footer

- A link to [kollect.ie](https://kollect.ie/) can be found in the footer as many customers looking for new furniture will be in need of a service to dispose of their old furniture. Since Fine Furnishings does not offer these services, this provides our users with a simple solution to their disposal needs.
- A link can be found in the footer to the [Psychology of Design blog](https://blog.zeelproject.com/64-psychology-in-interior-design.html). Many consumers, looking to purchase furniture, would like help and assistance in making a decision for what suits their home and needs best. The customer can always contact the business with any questions, but this blog provides a simple read to give the customer some ideas of what they may be looking for.

</details>

## Future Implementations

<details>

<summary>Future Features</summary>

- In future features, the site's home page will contain a Google Map for the company's location. 
- In future features, an About Us page will be implemented to give the user more information about the company.
- In future developments, the user's order confirmation will be stored in the user's 'Order History' on their individual profile, and they will have access to this from the navbar when logged in. This was not implemented due to time constraints on project submission.
- In future developments of this project, I will implement Stripe Webhook handlers and email confirmations to give the user better feedback on their checkout system. This was not implemented due to time constraints.
- In future features, the site will have a section for company reviews to help showcase the company's reputation and drive new users to the site. This would be implemented with a link to a Trustpilot review page in the footer as well. 

</details>

# Testing
<details>

<summary>Validator Testing</summary>

</details>

<details>

<summary>Manual Testing</summary>

</details>

<details>

<summary>Bugs/Unfixed Bugs</summary>

- Success messages are showing after the user navigates to a new page on the site. The message should be appearing on the page the user remains on or is redirected to, if called for. This will be fixed/updated in future features and was unfixed due to time constraints.
- I wanted the user to be able to save multiple addresses to their user profile and select a specific address when placing an order. Maybe they save a 'Home' address, 'Office' address, etc. Unfortunately, I implemented the model correctly with the Address name and the form allows for a second address to be added, however in future fixes, this will work correctly as any added addresses are not saved to the profile or admin panel. This was not fixed due to time constraints with submission.

</details>

# Deployment
<details>

<summary>Steps taken to deploy on Heroku</summary>

Set up the workspace:
1. Install gunicorn in workspace for Heroku deployment
2. Add to requirements.txt and create Procfile
3. In settings.py set DEBUG = False 
4. Reconfigured Default file & Static file storage in settings.py to allow Cloudinary deployment with Heroku
5. Added the Heroku app to the 'Allowed Hosts' in settings.py
6. Ensured all secret keys were added to the env.py file & stored in the gitignore file
7. Git add, commit and push changes to GitHub
Deploy on Heroku:
8. Create the app on Heroku and connect to GitHub project
9. Set the Config Vars in the "Settings" Tab - this includes: CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME, DATABASE_URL, SECRET_KEY, STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
10. Navigate to the "Deploy" tab and scroll down to click on "Deploy Branch" in the "Manual deploy" section

</details>

<details>

<summary>Fork Repository</summary>

Forking a repository allows you to create a copy to GitHub, and any changes made will not affect the original repository:

- Within GitHub, navigate to the repository page you are going to fork
- Click "Fork" on the top right corner of the page
- Wait for the copy to be created and you are then redirected to the forked repository

</details>

<details>

<summary>Clone Repository</summary>

Cloning a repository allows you to create a local copy of a repository on your machine:

- Within GitHub, navigate to the repository you are wanting to clone
- Click the green "<>Code" button
- Within the "Local" tab, copy the HTTPS url
- In your IDE, open Git Bash and type in 'git clone' followed by the pasted url just copied from GitHub. Ex: git clone https://example.com/repository/project
- The clone has been created on your local machine

</details>

# Credits

<details>

<summary>Content</summary>

- The Boutique Ado Walkthrough was referenced when setting up Django, Allauth and the base template.
- The [Boutique Ado Walkthrough](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2/courseware/eb05f06e62c64ac89823cc956fcd8191/0fb892bc636a44cf94b69d9f2aa9166a/?child=first) was referenced when creating product pages & search bar functionality.
- [Django documention](https://docs.djangoproject.com/en/dev/ref/models/querysets/#iexact) was referenced when utilizing iexact in creating the product category links.
- [Stack Overflow](https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request) helped me redirect users to the previous page without using the 'back' button on the browser.
- The contact app, was largely taken from my previous project [Sould Base Studio Booking Site](https://github.com/morganoleary/studio-booking-site)
- [Bootstrap Collapse Documentation](https://getbootstrap.com/docs/4.6/components/collapse/) was used to implement the dropdown answers on the FAQs page.
- [FreePik.com](https://www.freepik.com/free-photos-vectors/ff-logo) was used to create a mockup of a logo for the company for the Facebook page.
- Updating the shopping cart with quantity functionality & size options for the bedframes was implemented with a great help from the [Boutique Ado Walkthrough - Adding Products](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2/courseware/eb05f06e62c64ac89823cc956fcd8191/f324de58c90e47bd9497bf5839cf1859/)
- [Stack Overflow](https://stackoverflow.com/questions/47258289/differences-between-stacked-inline-and-tabular-inline) was referenced when creating the admin user profile and address fields.
- [Django Docs - forloop.counter](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#for) & [Django Docs - modelformset_factory¶](https://docs.djangoproject.com/en/5.0/ref/forms/models/#:~:text=modelformset_factory%20%C2%B6&text=Returns%20a%20FormSet%20class%20for,passed%20through%20to%20modelform_factory()%20.) were utilized when implementing the functionality of the users addresses and being able to add multiple to the same account. 
- [w3things.com](https://w3things.com/blog/rel-noopener-noreferrer/) was referenced when implementing the rel attributes on external site links in my project.
- Implementing Mailchimp as a newsletter signup in the footer of the site was implemented by following along with Code Institute's [Web Marketing Video - Newsletter Marking with Mailchimp](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+DRWM101+2021_T1/courseware/2b2a6057abf44272955637c09687ab43/acc4b7d56e3a400ebe110e5d734ce767/).

</details>

<details>

<summary>Technologies Used</summary>

- LucidChart = ERD
- Justinmind = wireframes
- [Pexels.com](https://www.pexels.com/) = product images 
- [Unsplash.com](https://unsplash.com/) = product images
- [Adobe Express Converter](https://www.adobe.com/express/feature/image/convert/jpg-to-png) = convert all jpg images to png
- [Compress PNG](https://compresspng.com/#google_vignette) = compress all png images
- [Fonticon](https://gauger.io/fonticon/) = generate site icons
- Django = Framework
- HTML = mark up language
- CSS = styling
- Bootstrap = styling
- Python = functionality
- VS Code = IDE
- Stripe = payment system
- Cloudinary = web hosting of product images
- Heroku = Deployment
- GitHub = Used to store the project
- Git = version control
- [PostgreSQL from CI](https://dbs.ci-dbs.net/) = database
- [Am I Responsive](https://ui.dev/amiresponsive) = multiple screen size views

</details>

<details>

<summary>Acknowledgements</summary>

- I would like to give a huge shout out to the tutor support team. Roman, Oisin & Roo were a great help while I ran into issues with implementing Cloudinary, git actions between GitPod & VS Code and issues deploying on Heroku with static files and Cloudinary.
- I would like to thank my mentor, Narender, for his time and support on this project. As we were limited in meetings on my part, he continued to stay supportive and helped keep me positive through the stress! Thank you.
- I would like to extend a huge thank you to Code Institute for this course. This has been an amazing opportunity that I never thought would be a part of my future and I am excited to continue my coding journey and begin my new career as a software developer! You have provided great resources throughout the last year and it has completely changed my life. Thank you so much for this opportunity.

</details>