# SI_507_Final_Project

Hello there!

I created this job searching scraper python program as my final project deliverable. Thank you for viewing my code. I hope you enjoy. 



### Base structure

This is an Indeed job posting web scraper. Its base URL is: 

https://www.indeed.com/

Users can search job title and location. Then the URL will generate something like this:

https://www.indeed.com/jobs?q=data+analyst&l=Charlotte%2C+NC  (Search term: data analyst | Charlotte,NC)

https://www.indeed.com/jobs?q=research+assistant&l=Ann+Arbor%2C+MI (Search term: research assistant | Ann Arbor, MI)

By looking it closely, you can see that the base URL structure for building the search URL is pretty similar, which is:

https://www.indeed.com/jobs?q={}&l={}



 Now, we are ready to build this web scraper. 



### Program Run

The program will ask user whether they want to search for a job, user needs to type 'Y' or 'N' as their answer. If yes, the program will ask the user to input position and the location that user wants to search. Once the web scraping is finished, the program will ask if the user want to view it in an Excel sheet. (I wrote the code on windows system, so the excel open code work for me perfectly, but if you are using mac, you might want to change couple of my code line to make this step works).  

![image-20201216121201978](C:\Users\panyu\Desktop\MHI\SI_507\Final\image-20201216121201978.png)

![image-20201216121704420](C:\Users\panyu\Desktop\MHI\SI_507\Final\image-20201216121704420.png)



The program will not open the Excel if the user chose no. But it will display a list of search results in the terminal.  

![image-20201216121857704](C:\Users\panyu\Desktop\MHI\SI_507\Final\image-20201216121857704.png)



Then the program will ask user if they want to review the job detail in a browser or not. Users can view the job details by type in the job list number to open the URL link in their browser. (The example here is the No.5 in the list)

![image-20201216122146115](C:\Users\panyu\Desktop\MHI\SI_507\Final\image-20201216122146115.png)

 

This is the basic program run. Users can search as many jobs/different locations as you want. However, if user want to view a position in big city such as New York, NY, it will take a long time for the program to generate its first 'Fetching'. But if user search the exact same term the second time, the program will use its cache and that will speed up the searching time. 



### Demo Link

Youtube URL: https://youtu.be/__n_ks7mq60

