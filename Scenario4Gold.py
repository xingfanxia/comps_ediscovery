import CompsML
import email_filter
import pandas as pd
import pickle

def scenario_4_Gold():

    relevantTree = pd.read_csv('RelevantLunch.txt', sep = '\n', names = ["ID"])
    relevantTree["Label"] = 1

    notRelevantTree = pd.read_csv('NotRelevantLunch.txt', sep = '\n', names = ["ID"], encoding = 'utf-8')
    notRelevantTree["Label"] = 0

# df = pd.read_csv('./data/parsed/test.csv', dtype=str)
# email_filtered = pd.DataFrame()
# email_filtered = email_filter.full_filter_email(df)
#
# with open("cleaned_test_emails.pickle",'wb') as handle:
#     pickle.dump(email_filtered, handle)

    with open("cleaned_test_emails.pickle", 'rb') as handle:
        email_filtered = pickle.load(handle)

    mask = email_filtered['ID'].isin(relevantTree["ID"])
    relevant = pd.DataFrame(email_filtered.loc[mask])
    relevant["Relevant"] = '1'

    mask1 = email_filtered['ID'].isin(notRelevantTree["ID"])
    notrelevant = pd.DataFrame(email_filtered.loc[mask1])
    notrelevant["Relevant"] = '0'

    full_test_df = pd.concat([relevant,notrelevant])
    full_test_df = full_test_df.reset_index(drop = True)

    full_test_df = CompsML.setup_dataframe('./data/Feb8hhmi/lsa_output_test_Feb8.npy', full_test_df,user_input = True)

    CompsML.test_tree('saved_forest.pickle', full_test_df, user_input = True)
