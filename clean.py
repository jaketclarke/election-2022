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

# calculate totals for the division
voteTypeTotals = voteTypeData.groupby(['DivisionNm']).sum().reset_index()
voteTypeTotals = voteTypeTotals[['DivisionNm','OrdinaryVotes','AbsentVotes','ProvisionalVotes','PrePollVotes','PostalVotes','TotalVotes']]
voteTypeTotals['PartyAb'] = 'Total'

# calculate formal totals for the division
voteTypeDataFormal = voteTypeData[voteTypeData.PartyNm != 'Informal']
voteTypeTotalsFormal = voteTypeDataFormal.groupby(['DivisionNm']).sum().reset_index()
voteTypeTotalsFormal = voteTypeTotalsFormal[['DivisionNm','OrdinaryVotes','AbsentVotes','ProvisionalVotes','PrePollVotes','PostalVotes','TotalVotes']]
voteTypeTotalsFormal['PartyAb'] = 'Total Formal'

# add to series
voteTypeData = pd.concat([voteTypeData,voteTypeTotals])
voteTypeData = pd.concat([voteTypeData,voteTypeTotalsFormal])
voteTypeData.sort_values(by=['DivisionNm','PartyAb'], inplace=True)

# unpivot
voteTypeDataUnpivot = pd.melt(
    voteTypeData,
    id_vars=['StateAb','DivisionID','DivisionNm','CandidateID','Surname','GivenNm','BallotPosition','Elected','HistoricElected','PartyAb','PartyNm'],
    value_vars=['OrdinaryVotes','AbsentVotes','ProvisionalVotes','PrePollVotes','PostalVotes','TotalVotes'], # excluding swing
    var_name='type',
    value_name='votes'
)

# pull out formal votes
voteTypeDataUnpivotTotalFormal = voteTypeDataUnpivot[voteTypeDataUnpivot['PartyAb'] == 'Total Formal']
voteTypeDataUnpivotTotalFormal = voteTypeDataUnpivotTotalFormal[['DivisionNm','type','votes']]
voteTypeDataUnpivotTotalFormal.rename({'votes':'Total Formal Primary Votes'}, axis=1, inplace=True)

# pull out all votes
voteTypeDataUnpivotTotal = voteTypeDataUnpivot[voteTypeDataUnpivot['PartyAb'] == 'Total']
voteTypeDataUnpivotTotal = voteTypeDataUnpivotTotal[['DivisionNm','type','votes']]
voteTypeDataUnpivotTotal.rename({'votes':'Total Primary Votes'}, axis=1, inplace=True)

# merge in for totals
voteTypeDataUnpivot = voteTypeDataUnpivot.merge(voteTypeDataUnpivotTotalFormal, on=['type','DivisionNm'])
voteTypeDataUnpivot = voteTypeDataUnpivot.merge(voteTypeDataUnpivotTotal, on=['type','DivisionNm'])

# Proportions calc
voteTypeDataUnpivot['VotesPcTotal'] = voteTypeDataUnpivot["votes"].div(voteTypeDataUnpivot["Total Primary Votes"].values)
voteTypeDataUnpivot['VotesPcFormalTotal'] = voteTypeDataUnpivot['votes'].div(voteTypeDataUnpivot['Total Formal Primary Votes'].values)

# What we want is informal as % total, votes % total formal 
voteTypeDataUnpivot["VotesPc"] = np.where(
    voteTypeDataUnpivot["PartyNm"] == "Informal",
    voteTypeDataUnpivot["votes"]/voteTypeDataUnpivot["Total Primary Votes"],
    voteTypeDataUnpivot["votes"]/voteTypeDataUnpivot["Total Formal Primary Votes"]
) 

# save
voteTypeDataUnpivotFileName = 'aus-type-unpivot-pc'
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

