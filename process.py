import wget
import os
import numpy as np
import pandas as pd
from functions import empty_directory, make_directorytree_if_not_exists

outputDir = 'output'
dataDir = 'data'
make_directorytree_if_not_exists(outputDir)

# sa1 data
sa1DataPath = f'{dataDir}{os.sep}pp-by-sa1.csv'
sa1Data = pd.read_csv(sa1DataPath)
print(sa1Data)

# normalise with df file names
# note - checked the underlying data and the ccd column (change the name for god sake!) is 2016 SA1s
sa1Data.rename({
    'state_ab': 'StateAb',
    'div_nm': 'DivisionNm',
    'ccd_id': 'sa1_2016',
    'pp_id': 'PollingPlaceID',
    'pp_nm': 'PollingPlace',
    'votes': 'VotesSA1'
}, axis=1, inplace=True)

primaryDataPath = f'{outputDir}{os.sep}aus-p-pc.csv'
primaryData = pd.read_csv(primaryDataPath)
primaryDataCutdown = primaryData[['PollingPlaceID', 'PartyAb', 'OrdinaryVotesPc']]

merge = sa1Data.merge(primaryDataCutdown, how='left', on='PollingPlaceID')
merge.rename({
    'OrdinaryVotesPc': 'VotesPc'
}, axis=1, inplace=True)

otherTypesDataPath = f'{outputDir}{os.sep}aus-type-unpivot-pc.csv'
otherTypesData = pd.read_csv(otherTypesDataPath)
otherTypesDataCutdown = otherTypesData[['DivisionNm', 'type', 'PartyAb', 'VotesPc']]

# fix labels to match sa1 data
otherTypesDataCutdown['type'] = np.where(otherTypesDataCutdown['type']=='AbsentVotes', 'Absent', otherTypesDataCutdown['type'])
otherTypesDataCutdown['type'] = np.where(otherTypesDataCutdown['type']=='ProvisionalVotes', 'Provisional', otherTypesDataCutdown['type'])
otherTypesDataCutdown['type'] = np.where(otherTypesDataCutdown['type']=='PrePollVotes', 'Pre-Poll', otherTypesDataCutdown['type'])
otherTypesDataCutdown['type'] = np.where(otherTypesDataCutdown['type']=='PostalVotes', 'Postal', otherTypesDataCutdown['type'])
otherTypesDataCutdown.rename({
    'type': 'PollingPlace'
}, axis=1, inplace=True)
# remove total rows
otherTypesDataCutdown.drop(otherTypesDataCutdown.index[otherTypesDataCutdown['PartyAb'] == 'Total Formal'], inplace=True)
otherTypesDataCutdown.drop(otherTypesDataCutdown.index[otherTypesDataCutdown['PartyAb'] == 'Total'], inplace=True)

# add data
merge = merge.merge(otherTypesDataCutdown, how='left', on=['DivisionNm','PollingPlace'])

# clean data
merge['PartyAb'] = merge['PartyAb_x'].fillna(merge['PartyAb_y'])
merge['VotesPc'] = merge['VotesPc_x'].fillna(merge['VotesPc_y'])
merge.drop(['PartyAb_x', 'PartyAb_y', 'VotesPc_x', 'VotesPc_y'], axis=1, inplace=True)

# create sum var
merge['weight'] = merge['VotesSA1'] * merge['VotesPc']

# from initial throw, delete informal
merge=merge.dropna(subset=['PartyAb'])

total = merge.groupby('sa1_2016').sum()['weight'].reset_index()
total.rename({'weight': 'primary_total_votes'}, axis=1, inplace=True)

groups = merge.groupby(['sa1_2016','PartyAb']).sum()['weight'].reset_index()
groups.rename({'weight': 'primary_votes'}, axis=1, inplace=True)

sa1Votes = groups.merge(total, on='sa1_2016')
sa1Votes['primary_pc'] = sa1Votes['primary_votes'] / sa1Votes['primary_total_votes']

# clean
sa1Votes.primary_votes = sa1Votes.primary_votes.round(0)
sa1Votes.primary_total_votes = sa1Votes.primary_total_votes.round(0)
sa1Votes.primary_pc = sa1Votes.primary_pc.round(4)

# unpivoted data
sa1VotesPathUnpivot = f'{outputDir}{os.sep}f2022_fp_by_sa1_2016_aus_unpivot.csv'
sa1Votes.to_csv(sa1VotesPathUnpivot, index=False)

# pivot
sa1VotesPivoted = pd.pivot_table(sa1Votes, values='primary_pc', index='sa1_2016', columns=['PartyAb']).reset_index().fillna(0)

sa1VotesPathPivoted = f'{outputDir}{os.sep}f2022_fp_by_sa1_2016_aus.csv'
sa1VotesPivoted.to_csv(sa1VotesPathPivoted, index=False)