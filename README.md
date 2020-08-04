# eco_co2_recrutement

## Installation  

- First of all, you have to create a virtualenv with the command **virtualenv -p /usr/bin/python3 env**
- Then, activate it with the commande **source env/bin/activate**  
- Clone the project with **https://github.com/kmessmer-06/eco_co2_recrutement.git**
- Next, use cd command to go in the eco_co2_recrutement directory **cd eco_co2_recrutement**
- Use **pip install -r requirement.txt** to install all dependencies of the project.
- Setup your database informations in eco_co2/settings.py or create same database as mine.
- Use **python manage.py migrate** to apply all migrations.
- Run **python manage.py loaddata src/co2_consumption/data/seasons.json** to install initial data.

## Part 1 - Django

As first, I decided to create a command management to fetch all the data from the API ECO CO2.  

Run **python manage.py fetch_co2_data_from_api** to create all Consumption objects in your database.

With more time, I would have add loggers instead of a simple print.  

To create a new table with hourly data, I decided to create another command management.  

Run **python manage.py generate_table_hourly_consumption** to create all ConsumptionInterpolate objects in your database.  

Same as the previous CM, loggers should replace the print.  

## Part 2 - Pandas

To be honest, I've never used pandas before. That was a first experience for me. It was interesting. Sorry if some of the code here is hard to understand.  

For this part, I decided to create an url with a template to show you the results I got for every questions.

To interpolate the results of the database ConsumptionInterpolate, I decided to create a pandas Dataframe of the original API calls (Consumption).

Next, I created a Dataframe based on the ConsumptionInterpolate table with a freq of 30 minutes.

Then, I used the method sub() of pandas to create a new Dataframe. I had a problem with this DataFrame, the last informations was empty and I didn't found any clear solution. I decided to use the method ffill() from pandas. I think there is a better way to fill this value.  

To create a graph of this subtract, I used plotly and I found it very easy to use.

To have a better representation, I decided to make a groupby() based on a grouper with a frequence of 15 days.

To the median and the mean, I tried to be DRY. So I created method which take a model_name as parameter. These method works wells to apply the same process on Consumption and ConsumptionInterpolate.  

Then, I started to work on the CSV. I don't really understand why use pandas to do that. It is very easy to do in native python in my point of view.
Anyway, I used pandas for the exercice with a simple method read_consommation_in_csv.

## What's missing

Some things are missing on this project. I didn't write any test because I didn't have time. A test with a mock to fake api return (Part 1) would be a good test.

Like I said earlier, loggers are missing too.

I think some part of the code can be more detailled and documented.

Thanks you for reading/testing and give me some feedback to improve myself !

 
