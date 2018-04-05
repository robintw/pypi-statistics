import json

import pandas as pd

def convert_to_df_with_github_url():
    """Converts the raw metadata JSON files to a pandas dataframe containing the metadata
    from the 'info' dict in the JSON, and adds a Github URL if found anywhere in the JSON"""
    files = os.listdir('all_metadata')

    s = []

    for filename in tqdm(files):
        # Read JSON file for package
        with open('all_metadata/' + filename) as f:
            json_string = f.read()
        # Search in the string for a github URL
        regex_result = re.search('github.com/([^\s;\(){}#]+?/[^\s`_.;\'\\\[\]\{\\}/\","><#!$\%&*)(]+)', json_string)
        # Try loading the JSON and skip if it fails
        try:
            j = json.loads(json_string)
        except:
            continue
        # Convert to a pandas Series
        json_series = pd.io.json.json_normalize(j['info'])
        # Add the github URL if one was found
        if regex_result:
            json_series['github_url'] = regex_result.group(1)
        
        # Add to a list
        s.append(json_series)

    # Concatenate the list of Series to create a DataFrame
    df = pd.concat(s)

    return df