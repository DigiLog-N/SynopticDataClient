Notes:
Timeseries API is capable of outputting data in CSV format, but only for one
station at a time. 

The plan is to use the timeseries API to build up a year's worth of data. This
should give us the frequency of updates on the fields as well. Then we can use
either the Latest API call or timeseries call either one, two, three times per
day, etc. To get the latest data.

I doubt resolutions greater than once every ten to thirty minutes will be
beneficial, based on part experience with MesoWest, and developing models.
A year's worth of data can be used to model changes with the seasons, day and
night cycles, etc.

We can also use a vehicle's current lat/lon to focus a query on just the
sensors along the vehicle's current position and projected path. We could
potentially do a higher frequency of updates.

MesoWest/SynopticData is relatively inexpensive with free-tier users getting
5,000 requests or 5 million service units per month. After that threshold, the
user needs to pay a $5 dollar service fee + a very small charge per query.

After pulling a year's worth of data for roughly six stations during testing,
I used up all of my free cycles. I subsequently upgraded my account. Depending
on how many stations worth of data that we need, we can pull a year or more
for each relatively inexpensively.

I've added the year's worth of data for the ~14 stations I pulled into
data/yearly. They are all stations within approximately 10-20 miles of UCSD,
as the crow flies. I have station metadata for the states of NH and CA, and
the others are easy enough to get.

Currently each row does not include the station's lat and lon values. Instead
it includes the station's unique identifier (STID). It may be more desireable
to insert the lat/lon values as well.

Data taken from SynopticData's APIs is ostensibly public.

MesoWest/SynopicData's developer site:
https://developers.synopticdata.com/

Getting started page:
https://developers.synopticdata.com/mesonet/v2/getting-started/

IDs for the 14+1 sites used:
'2930P'
'DMHSD'
'MSDSD'
'4160P'
'CI150'
'F1955'
'NMLC1'
'BVDC1'
'KEAC1'
'KCRQ '
'1386P'
'3025P'
'PLMC1'
'CBDSD'
'KSAN'


