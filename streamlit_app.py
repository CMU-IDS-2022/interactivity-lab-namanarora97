from re import U
from prompt_toolkit import print_formatted_text
import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def load_data():
    """
    Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
    and return it.
    """
    return pd.read_csv('pulse39.csv')
    pass

@st.cache
def get_slice_membership(df, genders, races, educations, age_range):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice.
    
    In the example provided, we assume genders is a list of selected strings
    (e.g. ['Male', 'Transgender']). We then filter the labels based on which
    rows have a value for gender that is contained in this list. You can extend
    this approach to the other variables based on how they are returned from
    their respective Streamlit components.
    """
    labels = pd.Series([1] * len(df), index=df.index)
    if genders:
        labels &= df['gender'].isin(genders)
    
    # ... complete this function for the other demographic variables

    labels &= df['race'].isin(races)
    labels &= df['education'].isin(educations)

    age_min, age_max = age_range
    labels &= (df['age'].between(age_min, age_max, inclusive = 'both'))
    print(labels)
    print(len(labels))
    print(labels.sum())
    return labels

def make_long_reason_dataframe(df, reason_prefix):
    """
    ======== You don't need to edit this =========
    
    Utility function that converts a dataframe containing multiple columns to
    a long-style dataframe that can be plotted using Altair. For example, say
    the input is something like:
    
         | why_no_vaccine_Reason 1 | why_no_vaccine_Reason 2 | ...
    -----+-------------------------+-------------------------+------
    1    | 0                       | 1                       | 
    2    | 1                       | 1                       |
    
    This function, if called with the reason_prefix 'why_no_vaccine_', will
    return a long dataframe:
    
         | id | reason      | agree
    -----+----+-------------+---------
    1    | 1  | Reason 2    | 1
    2    | 2  | Reason 1    | 1
    3    | 2  | Reason 2    | 1
    
    For every person (in the returned id column), there may be one or more
    rows for each reason listed. The agree column will always contain 1s, so you
    can easily sum that column for visualization.
    """
    reasons = df[[c for c in df.columns if c.startswith(reason_prefix)]].copy()
    reasons['id'] = reasons.index
    reasons = pd.wide_to_long(reasons, reason_prefix, i='id', j='reason', suffix='.+')
    reasons = reasons[~pd.isna(reasons[reason_prefix])].reset_index().rename({reason_prefix: 'agree'}, axis=1)
    return reasons


# MAIN CODE


st.title("Household Pulse Explorable")
with st.spinner(text="Loading data..."):
    df = load_data()
st.write(df)    
st.text("Visualize the overall dataset and some distributions here...")

# race_hist = alt.Chart(df).mark_bar().encode(
#     alt.Y('race', sort = 'x'),
#     alt.X('count()')
# ).interactive()

# edu_hist = alt.Chart(df).mark_bar().encode(
#     alt.Y('education', sort = 'x'),
#     alt.X('count()')
# ).interactive()

# st.altair_chart(race_hist, use_container_width=True)
# st.altair_chart(edu_hist)

# st.write(race_hist)

st.header("Custom slicing")
st.text("Implement your interactive slicing tool here...")

slice_gender = st.multiselect(
    'Genders', 
    list(df.gender.unique()), 
    default = 'Male'
)
slice_race = st.multiselect(
    'Race', 
    list(df.race.unique()), 
    default = 'White'
)
slice_education = st.multiselect(
    'Education', 
    list(df.education.unique()), 
    default = 'Bachelors degree'
)
slice_age = st.slider(
    'Select a range of age', 
    0, 100, 
    (19, 89)
)

labels = get_slice_membership(
    df,
    slice_gender,
    slice_race,
    slice_education,
    slice_age
)

st.write(str(round((len(df[labels])/len(df)) * 100, 2)) + \
    '% rows sliced')

st.write('Received Vaccine')

receieved_vaccine_chart_in = alt.Chart(df[labels], title='In Slice').mark_bar().encode(
    alt.X('received_vaccine'),
    alt.Y('count()')
)

receieved_vaccine_chart_out = alt.Chart(df[~labels], title='Out of Slice').mark_bar().encode(
    alt.X('received_vaccine'),
    alt.Y('count()')
)

st.write(receieved_vaccine_chart_in | receieved_vaccine_chart_out)

st.write('Vaccine Intention')

intention_chart_in = alt.Chart(df[labels], title='In Slice').mark_bar(bandSize=30).encode(
    alt.X('vaccine_intention'),
    alt.Y('count()')
)

intention_chart_out = alt.Chart(df[~labels], title='Out of Slice').mark_bar(bandSize=30).encode(
    alt.X('vaccine_intention'),
    alt.Y('count()')
)

st.write(intention_chart_in | intention_chart_out)


st.write('Vaccine Reasons')

vaccine_reasons_in = make_long_reason_dataframe(
    df[labels], 
    'why_no_vaccine_'
)

vaccine_reasons_in_chart = alt.Chart(vaccine_reasons_in, title='In Slice').mark_bar().encode(
    alt.X('sum(agree)'),
    alt.Y('reason:O', sort = '-x'),
).interactive()

vaccine_reasons_out = make_long_reason_dataframe(
    df[~labels], 
    'why_no_vaccine_'
)

vaccine_reasons_out_chart = alt.Chart(vaccine_reasons_out, title='Out of Slice').mark_bar().encode(
    alt.X('sum(agree)'),
    alt.Y('reason:O', sort = '-x'),
).interactive()


st.write(vaccine_reasons_in_chart | vaccine_reasons_out_chart)


st.header("Person sampling")
st.text("Implement a button to sample and describe a random person here...")

import random

i = random.randint(0, len(df)-1)

age = df.loc[i, 'age']
orient = df.loc[i, 'sexual_orientation']
marital = df.loc[i, 'marital_status']
gender = df.loc[i, 'gender']
race = df.loc[i, 'race']
vaxxed = df.loc[i, 'received_vaccine']

out = '''
This person is a {} year old {}, {}, {} {}. 
They {} received the vaccine. 
'''

out2 = '''
Their reasons for not getting vaxxed include: 
{}
'''

vaccine_reasons = make_long_reason_dataframe(
    df, 
    'why_no_vaccine_'
)

if st.button('Get Random Person'):
    if vaxxed:
        st.write(
            out.format(age, orient, race, marital, gender, 'have')
        )
    else:
        reasons_ = [reason for reason in vaccine_reasons[vaccine_reasons.id == i]]
        print(
            out.format(age, orient, race, marital, gender, 'have not')
        )
        st.write(
            out2.format(reasons_)
        )