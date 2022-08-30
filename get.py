# imports
import wget
import os
from functions import empty_directory, make_directorytree_if_not_exists

# settings
dataDir = 'data'
make_directorytree_if_not_exists(dataDir)

# result data from https://results.aec.gov.au/27966/Website/HouseDownloadsMenu-27966-Csv.htm
# sa1 data from https://www.aec.gov.au/Elections/federal_elections/2022/downloads.htm

files = [
    {'label':'nsw-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-NSW.csv'},
    {'label':'vic-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-VIC.csv'},
    {'label':'qld-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-QLD.csv'},
    {'label':'sa-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-SA.csv'},
    {'label':'wa-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-WA.csv'},
    {'label':'tas-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-TAS.csv'},
    {'label':'act-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-ACT.csv'},
    {'label':'nt-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-NT.csv'},
    {'label':'aus-type','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseFirstPrefsByCandidateByVoteTypeDownload-27966.csv'},
    {'label':'aus-tcp','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseTcpByCandidateByPollingPlaceDownload-27966.csv'},
    {'label':'aus-tpp','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseTppByPollingPlaceDownload-27966.csv'},
    {'label':'pp-by-sa1','url':'https://www.aec.gov.au/Elections/federal_elections/2022/files/downloads/2022-federal-election-votes-sa1.csv'}
]

# empty and populate
empty_directory(dataDir)

for file in files:
    url = file['url']
    file=file['label']
    filepath=f'{dataDir}{os.sep}{file}.csv'

    wget.download(url, out=filepath)