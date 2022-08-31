import wget
import os
import pandas as pd
from functions import empty_directory, make_directorytree_if_not_exists
import numpy as np

outputDir = 'output'
dataDir = 'data'
make_directorytree_if_not_exists(outputDir)

# initial job - read and unpivot the votetype data
voteTypeDataPath = f'{dataDir}{os.sep}aus-type.csv'
voteTypeData = pd.read_csv(voteTypeDataPath, skiprows=1)
# print(voteTypeData)

voteTypeDataUnpivot = pd.melt(
    voteTypeData,
    id_vars=['StateAb','DivisionID','DivisionNm','CandidateID','Surname','GivenNm','BallotPosition','Elected','HistoricElected','PartyAb','PartyNm'],
    value_vars=['OrdinaryVotes','AbsentVotes','ProvisionalVotes','PrePollVotes','PostalVotes','TotalVotes','Swing'],
    var_name='type',
    value_name='value'
)

voteTypeDataUnpivotFileName = 'aus-type-unpivot'
voteTypeDataUnpivotFilePath = f'{outputDir}{os.sep}{voteTypeDataUnpivotFileName}.csv'

voteTypeDataUnpivot.to_csv(voteTypeDataUnpivotFilePath, index=False)

# merge primary data

states = [
    'vic',
    'qld',
    'sa',
    'wa',
    'tas',
    'act',
    'nt'
]

state = 'nsw'
primaryVoteDataPath = f'{dataDir}{os.sep}{state}-p.csv'
primaryData = pd.read_csv(primaryVoteDataPath, skiprows=1)

for state in states:
    primaryVoteDataPath = f'{dataDir}{os.sep}{state}-p.csv'
    newData = pd.read_csv(primaryVoteDataPath, skiprows=1)
    primaryData = pd.concat([primaryData, newData])

primaryDataUnpivotFileName = 'aus-p'
primaryDataUnpivotFilePath = f'{outputDir}{os.sep}{primaryDataUnpivotFileName}.csv'

primaryData.to_csv(primaryDataUnpivotFilePath, index=False)

# add proportions to primary data
primaryDataPath = f'{outputDir}{os.sep}aus-p.csv'
primaryData = pd.read_csv(primaryDataPath)
print(primaryData)

# work out total column
# joint booths have different PollingPlaceIDs
primaryTotal = primaryData.groupby(['PollingPlaceID']).sum()['OrdinaryVotes'].reset_index('PollingPlaceID')
primaryTotal.rename({'OrdinaryVotes':'Total Primary Votes'}, axis=1, inplace=True)

primaryData = primaryData.merge(primaryTotal, on='PollingPlaceID')

# work out total formal
primaryDataFormal = primaryData[primaryData.PartyNm != 'Informal']
primaryTotalFormal = primaryDataFormal.groupby(['PollingPlaceID']).sum()['OrdinaryVotes'].reset_index('PollingPlaceID')
primaryTotalFormal.rename({'OrdinaryVotes':'Total Formal Primary Votes'}, axis=1, inplace=True)

primaryData = primaryData.merge(primaryTotalFormal, on='PollingPlaceID')


# Proportions calc
primaryData['OrdinaryVotesPcTotal'] = primaryData["OrdinaryVotes"].div(primaryData["Total Primary Votes"].values)
primaryData['OrdinaryVotesPcFormalTotal'] = primaryData['OrdinaryVotes'].div(primaryData['Total Formal Primary Votes'].values)

# What we want is informal as % total, votes % total formal 
primaryData["OrdinaryVotesPc"] = np.where(
    primaryData["PartyNm"] == "Informal",
    primaryData["OrdinaryVotes"]/primaryData["Total Primary Votes"],
    primaryData["OrdinaryVotes"]/primaryData["Total Formal Primary Votes"]
) 

# output this file
primaryOutputDataPath = f'{outputDir}{os.sep}aus-p-pc.csv'
primaryData.to_csv(primaryOutputDataPath, index=False)

