# Problem: Predicting House Prices in Pakistan from Zameen.com

## Background
Zameen.com is the premier online destination for buying, selling and renting real estate in Pakistan. According to its website, it boasts 550,000 new listings every month for an average monthly audience of 5.5 million users and has with more than 15,000 active real estate agencies. 

In 2016, Zameen.com started publishing a Real Estate Price Index that estimates the prices for houses, plots and residential property for 9 different cities. For each listing, Zameen.com estimates its current value by using the Real Estate Price Index (similar to Zillow Zestimate). However, it is unclear how they calculate the index, or how accurate its estimates are.

My goal is to a build a more transparent and accurate pricing model than Zameen's.


## Dataset
I collected the data by scrapping Zameen.com from 12/1/2020 to 12/31/2020. I extracted listings from the three largest real markets markets in Pakistan (Lahore, Karachi and Islamabad) for all types of listings (e.g. plots, houses, farmhouses, agricultural land) for sale or rent. The total dataset size is about 450K listings.

To simplify my model, I filtered the dataset to include houses for sale in Lahore. In addition, I only considered listings scrapped on a single day, 12/8/2020. This reduced the dataset to 14K unique listings.


## Model
My final model is a Random Forest with an accuracy of 83% with 8 features (`Area`, `Beds`, `Baths`, `Age`, `DHA Defence`, `Parking Spaces`, `Servant Quarters`, `Park`). It has a MSE of 1.5 crores and a RMSE of 1.2 crores ([see modelling](modelling.ipynb)).


## Findings
* DHA Lahore is most common location for listings ([see eda-one day](eda-one-day.ipynb))
* Home buyers are willing to pay a premium for a Jacuzzi ([see eda-one day](eda-one-day.ipynb))
* Houses more than 5 years old perform well compared to new houses ([see eda-one-day](eda-one-day.ipynb))
* About a quarter of listings on Zameen.com are duplicate ([see data-preprocessing](data-preprocessing.ipynb))
* Commerical plots in Islamabad moved quite a bit in December 2020 ([see eda-month-duplicates-and-price-changes](eda-month-duplicates-and-price-changes.ipynb))


## Discussion
To improve predictions, I want to test a time series model that is able to use scraped listings over multiple days. However, lagging house price will be tricky since it stays fairly consistent.

I also want to add plot prices to my model. However, it is a challenge since plot availability and house availability do not overlap on Zameen.com. Hence, most houses are not near plots for sale which makes it difficult to estimate their plot prices (perhaps a plot pricing model could help). One way to solve this is to match plots to houses using gelocation, so plots closest to a house determine a house's underlying plot price. On the other hand, geomapping is not consistent and up-to-date across Pakistan so it requires a non-trivial amount of manual work (e.g. breaking DHA Lahore into Phases and blocks, and matching plots to each block).

I also want to incorporate macroeconomic variables, such as expected taxes and inflation, to make the model responsive to the economy.