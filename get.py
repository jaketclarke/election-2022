# imports
import wget
import os

# result data from https://results.aec.gov.au/27966/Website/HouseDownloadsMenu-27966-Csv.htm

files = [
    {'label':'nsw-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-NSW.csv'},
    {'label':'vic-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-VIC.csv'},
    {'label':'qld-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-QLD.csv'},
    {'label':'sa-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-SA.csv'},
    {'label':'wa-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-WA.csv'},
    {'label':'tas-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-TAS.csv'},
    {'label':'act-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-ACT.csv'},
    {'label':'nt-p','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-27966-NT.csv'},
    {'label':'aus-tcp','url':'https://results.aec.gov.au/27966/Website/Downloads/HouseTcpByCandidateByPollingPlaceDownload-27966.csv'},
    {'label':'aus-tpp','url':' https://results.aec.gov.au/27966/Website/Downloads/HouseTppByPollingPlaceDownload-27966.csv'}
]

dataDir = 'data'

for file in files:
    url = file['url']
    file=file['label']
    filepath=f'{dataDir}{os.sep}{file}.csv'

    wget.download(url, out=filepath)