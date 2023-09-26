import pandas as pd
import numpy as np
import streamlit as st
import scipy as sp
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import chart_studio
from plotly.subplots import make_subplots

# Is College Worth it?

st.title('Is College Worth it?')
st.header('Data suggests that recent high school graduates don\'t think it is.')
st.write('This work is based on the following article: https://freopp.org/is-college-worth-it-a-comprehensive-return-on-investment-analysis-1b2ad17f84c8')

st.header('2.7M students graduated high school in 2021. Only 1.7M joined college the next fall.' ,divider='violet')



# Enrollment data for males, females, and total from 1960 till 2021

# Load the College Enrollment Data
#enrollment = pd.read_csv('/Users/hassancoudsi/Documents/AUB/MSBA/325Visualization/Streamlit_Assignment/CollegeEnrollment.csv')

# Load the College Enrollment Data (github)
file1 = './CollegeEnrollment.csv'
enrollment = pd.read_csv(file1)

# Create Streamlit checkboxes to choose columns
labels = ['Total', 'Male', 'Female']

selected_columns = [label for label in labels if st.checkbox(label, True)]

# Create a line plot for % of recent high school graduates who enroll in college
title = '% of Recent High School Graduates who Enrolled in Colleges'
colors = ['#6371E0', '#EC516E', '#F8CD5B']

mode_size = [12, 8, 8]
line_size = [4, 2, 2]

x_data = enrollment['Year']
y_data = enrollment[['Total_Percent_Recent_HighSchool_Completers_Enrolled_in_College', 'Total_Males', 'Total_Females']]

fig = go.Figure()

for i in range(0, 3):
    if labels[i] in selected_columns:
        fig.add_trace(go.Scatter(x=x_data, y=y_data.iloc[:, i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))
        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data.iloc[0], x_data.iloc[-1]],
            y=[y_data.iloc[0, i], y_data.iloc[-1, i]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))
    else:
        # If the column is not selected, remove it from the figure
        fig.data = [trace for trace in fig.data if trace.name != labels[i]]

fig.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False,
    plot_bgcolor='white'
)

annotations = []

# Adding labels for selected columns
for label, color in zip(labels, colors):
    if label in selected_columns:
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_data.iloc[0, labels.index(label)],
                                xanchor='right', yanchor='middle',
                                text=label + ' {}%'.format(y_data.iloc[0, labels.index(label)]),
                                font=dict(family='Saraburn',
                                          size=16,
                                          color=color),
                                showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_data.iloc[-1, labels.index(label)],
                                xanchor='left', yanchor='middle',
                                text='{}%'.format(y_data.iloc[-1, labels.index(label)]),
                                font=dict(family='Saraburn',
                                          size=16,
                                          color=color),
                                showarrow=False))

# Title
annotations.append(dict(xref='paper', yref='paper', x=0.48, y=1.05,
                        xanchor='center', yanchor='bottom',
                        text=title,
                        font=dict(family='Poppins',
                                  size=24,
                                  color='#696C71'),
                        showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.2,
                        xanchor='center', yanchor='top',
                        text='Source: National Center of Education Statistics<br>https://nces.ed.gov/programs/digest/d22/tables/dt22_302.10.asp',
                        font=dict(family='Saraburn',
                                  size=12,
                                  color='rgb(150,150,150)'),
                        showarrow=False))

fig.update_layout(annotations=annotations)

# Customize the figure layout
fig.update_layout()

# Display the Plotly figure using st.plotly_chart
st.plotly_chart(fig)

st.markdown('<span style="color: #EC516E; font-size: 24px;">1M students finished high school but chose not to join college in 2021.</span>', unsafe_allow_html=True)
st.markdown('<span style="color: #EC516E; font-size: 24px;">62% of high school graduates enrolled in college the next fall in 2021. We are back to 1992 level.</span>', unsafe_allow_html=True)
st.markdown('<span style="color: #EC516E; font-size: 24px;">Only 55% of male high school graudates enrolled in college the following fall in 2021. We are back to the 1960 level..</span>', unsafe_allow_html=True)


st.write("")
st.write("")
st.write("")

# ROI Charts

# ROI by Program Category

st.title('Is College Worth it? It Depends!')
st.header('What Does ROI Analysis Say?')
st.markdown('<span style="color: #6371E0; font-size: 32px;">Return on Investment (ROI) of a college degree is the increase in lifetime earnings a student can expect from that degree, minus the direct and indirect costs of college.</span>', unsafe_allow_html=True)
st.write('The graphs below are based on the analysis of 30,000 bachelor’s degree programs at 1,775 colleges and universities across the United States reveals new insights.')

st.subheader('Let us group all college programs (majors) under 17 categories and examine the ROI for each program category.')


# Load the ROI Data
#roi = pd.read_csv('/Users/hassancoudsi/Documents/AUB/MSBA/325Visualization/Streamlit_Assignment/ROI.csv')

# Load the ROI Data (Github)
file2 = './ROI.csv'
roi = pd.read_csv(file2)

roi['Age at which ROI turns positive'] = roi['Age at which ROI turns positive'].replace(999, 70)

# Group by 'Program category' and calculate the mean ROI and the mean Age at which ROI turns positive for each program
roi_by_program = roi.groupby('Program category').agg({
    'Lifetime return on investment (ROI)': 'mean',
    'Age at which ROI turns positive': 'mean'
}).reset_index()

roi_by_program.columns = ['Program Type', 'Lifetime return on investment (ROI)', 'Age at which ROI turns positive']

columns_to_round = ['Lifetime return on investment (ROI)', 'Age at which ROI turns positive']
roi_by_program[columns_to_round] = roi_by_program[columns_to_round].apply(lambda x: round(x))


roi_by_program = roi_by_program.sort_values(by=['Lifetime return on investment (ROI)', 'Age at which ROI turns positive'], ascending=[False, True])

# Create the Plotly Express figure
fig1 = px.bar(roi_by_program, x='Program Type', y='Lifetime return on investment (ROI)')

# Conditionally color bars below 0 (e.g., in red)
fig1.update_traces(marker_color=['red' if val < 0 else 'blue' for val in roi_by_program['Lifetime return on investment (ROI)']])

# Display the figure in Streamlit
st.plotly_chart(fig1)


st.markdown('<span style="color: #EC516E; font-size: 24px;">The lifetime return on investment is very high for engineering and computer science.</span>', unsafe_allow_html=True)
st.markdown('<span style="color: #EC516E; font-size: 24px;">The lifetime return on investment is nearly zero or negative for Psychology, Philosophy and Religious Studies, and Visual Arts and Music.</span>', unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

# How long does it take to recover the investment

st.subheader('So, how quickly can the investment in a degree be recovered? It also depends on the major.')

# Create the Plotly Express figure
fig2 = px.bar(roi_by_program, x='Program Type', y='Age at which ROI turns positive')

# Display the figure in Streamlit
st.plotly_chart(fig2)

st.markdown('<span style="color: #EC516E; font-size: 24px;">Engineering and computer science students can recover their investment by the time they reach 30.</span>', unsafe_allow_html=True)
st.markdown('<span style="color: #EC516E; font-size: 24px;">Philosophy and Religious Studies, and Visual Arts and Music majors will NOT recover their investments before retirement.</span>', unsafe_allow_html=True)


# The ranking of the top 10 programs by ROI

st.subheader('Curious to know the top 10 programs in terms of ROI?')

roi_sorted = roi.sort_values(by='Lifetime return on investment (ROI)', ascending=False)
top10_programs = roi_sorted[['Institution name', 'Program name', 'Lifetime return on investment (ROI)']].head(10)

fig3 = go.Figure(go.Bar(
    x=top10_programs['Lifetime return on investment (ROI)'][::-1],  # Reverse the order of ROI data
    y=top10_programs['Institution name'][::-1],  # Reverse the order of institution names
    text=top10_programs['Program name'][::-1],
    textposition='inside',  # Set textposition to 'inside'
    insidetextanchor='start',  # Align text to the right inside the bars
    orientation='h'
))

fig3.update_layout(
    title="The to 10 Programs in Life Time Return on Investment",
    xaxis_title="ROI",
)

st.plotly_chart(fig3)

st.markdown('<span style="color: #EC516E; font-size: 24px;">The brand name is important, but the program type is even more important.</span>', unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

# The top 10 universities by ROI 

st.subheader('Let us rank based on institution name across majors and look at the top 10 institutions in terms of ROI.')
st.markdown('<span style="color: #6371E0; font-size: 32px;">Does the list look like anything you have seen in the rankings?</span>', unsafe_allow_html=True)

#unique_institutions = roi['Institution name'].unique()
earnings_by_institution = roi.groupby('Institution name')['Lifetime return on investment (ROI)'].mean().reset_index()
earnings_by_institution_sorted = earnings_by_institution.sort_values(by='Lifetime return on investment (ROI)', ascending=False)
top10_institutions = earnings_by_institution_sorted[['Institution name','Lifetime return on investment (ROI)']].head(10)

fig4 = go.Figure(go.Bar(
    x=top10_institutions['Institution name'],  # Reverse the order of ROI data
    y=top10_institutions['Lifetime return on investment (ROI)'],  # Reverse the order of institution names
))

fig4.update_layout(
    title="The to 10 Institutions in Life Time Return on Investment",
    yaxis_title="ROI",
    )
st.plotly_chart(fig4)

st.markdown('<span style="color: #EC516E; font-size: 24px;">Where is Harvard, Princeton, or most of the Ivy Leagues?</span>', unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")


# ROI correlation with cost and admissions 

st.subheader('Is ROI correlated with cost or admissions rate?')

st.markdown('<span style="color: #6371E0; font-size: 32px;">Are more expensive schools worth it?</span>', unsafe_allow_html=True)
st.markdown('<span style="color: #6371E0; font-size: 32px;">We will use the average net price all students pay after financial aid, not the sticker price published on the school\'s website.</span>', unsafe_allow_html=True)


roi_cleaned = roi.dropna(subset=['Admissions rate', 'Annual net tuition cost']).query('`Admissions rate` != 0 and `Annual net tuition cost` != 0')


roi_by_institution = roi_cleaned.groupby('Institution name').agg({
    'Lifetime return on investment (ROI)': lambda x: round(x.mean()),
    'Admissions rate': lambda x: round(x.mean()),
    'Annual net tuition cost': lambda x: round(x.mean()),
}).reset_index()


fig5 = px.scatter(
    roi_by_institution,
    x='Annual net tuition cost',
    y='Lifetime return on investment (ROI)',
    title='Lifetime ROI vs Annual Net Tuition Cost'
)
st.plotly_chart(fig5)

st.markdown('<span style="color: #EC516E; font-size: 24px;">When the annual net tuition cost goes up the ROI does NOT go up.</span>', unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

st.markdown('<span style="color: #6371E0; font-size: 32px;">Are more selective schools worth it?</span>', unsafe_allow_html=True)


fig6 = px.scatter(
    roi_by_institution,
    x='Admissions rate',
    y='Lifetime return on investment (ROI)',
    title='Lifetime ROI vs Admissions rate'
)
st.plotly_chart(fig6)

st.markdown('<span style="color: #EC516E; font-size: 24px;">Unless you go to a highly slective school (less than 15% admissions rate), there seems to be no correlation between school selectivity and ROI.</span>', unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

# Compare earnings with and without a degree for different programs

st.title('So, college is worth it but NOT for all majors.')
st.subheader('How much more money could you expect to earn if you pursue a degree?')
st.subheader('Choose a program type and an age category and find out for yourself.')

st.write('Keep in mind that if somone does not enroll in colege, s/he can start making money earlier.')


unique_programs = roi['Program category'].unique()

age_brackets = ['26-28','29-31','32-34','35-37','38-40','41-43','44-46','47-49','50-52','53-55','56-58','59-61','62-64']

degree_status = ['Degree', 'No Degree']

# Create a DataFrame with the desired order: 'Program Type', 'Age', 'Degree Status'
data = []

for program in unique_programs:
    for age in age_brackets:
        for degree in degree_status:
            data.append([program, age, degree])

degree_effect = pd.DataFrame(data, columns=['Program Type', 'Age', 'Degree Status'])

earnings_cols = ['Estimated earnings, ages 23-25', 'Estimated earnings, ages 26-28', 'Estimated earnings, ages 29-31',
                  'Estimated earnings, ages 32-34', 'Estimated earnings, ages 35-37', 'Estimated earnings, ages 38-40',
                  'Estimated earnings, ages 41-43', 'Estimated earnings, ages 44-46', 'Estimated earnings, ages 47-49',
                  'Estimated earnings, ages 50-52', 'Estimated earnings, ages 53-55', 'Estimated earnings, ages 56-58',
                  'Estimated earnings, ages 59-61', 'Estimated earnings, ages 62-64',
                  'Estimated counterfactual earnings, ages 19-20', 'Estimated counterfactual earnings, ages 21-22',
                  'Estimated counterfactual earnings, ages 23-24', 'Estimated counterfactual earnings, ages 26-28',
                  'Estimated counterfactual earnings, ages 29-31', 'Estimated counterfactual earnings, ages 32-34',
                  'Estimated counterfactual earnings, ages 35-37', 'Estimated counterfactual earnings, ages 38-40',
                  'Estimated counterfactual earnings, ages 41-43', 'Estimated counterfactual earnings, ages 44-46',
                  'Estimated counterfactual earnings, ages 47-49', 'Estimated counterfactual earnings, ages 50-52',
                  'Estimated counterfactual earnings, ages 53-55', 'Estimated counterfactual earnings, ages 56-58',
                  'Estimated counterfactual earnings, ages 59-61', 'Estimated counterfactual earnings, ages 62-64']

earnings_by_program = roi.groupby('Program category')[earnings_cols].mean().reset_index()

earnings_by_program[earnings_cols] = earnings_by_program[earnings_cols].astype(int)

# Create a Streamlit multiselect widget for selecting program types
select_all_option = "Select All"
clear_all_option = "Clear All"
selected_programs = st.multiselect('Select Program Type(s)', [select_all_option] + list(unique_programs), default=[select_all_option])

# Create a Streamlit selectbox for selecting age brackets
selected_age = st.selectbox('Select Age Bracket', age_brackets)

# Filter the degree_effect DataFrame based on the selected program types and age bracket
if select_all_option in selected_programs:
    filtered_degree_effect = degree_effect
    # Remove the "Select All" option if it's selected, so it doesn't interfere with the filtering
    selected_programs.remove(select_all_option)
else:
    filtered_degree_effect = degree_effect[degree_effect['Program Type'].isin(selected_programs)]

# Filter data for the selected age bracket
filtered_data = filtered_degree_effect[filtered_degree_effect['Age'] == selected_age]

# Filter earnings data for the selected age bracket
earnings_data = earnings_by_program[earnings_by_program['Program category'].isin(filtered_data['Program Type'])]

# Merge the filtered data with earnings data
filtered_data = pd.merge(filtered_data, earnings_data, left_on='Program Type', right_on='Program category')

# Create a bar chart using Plotly Express
fig = px.bar(filtered_data, x='Program Type', y=f'Estimated earnings, ages {selected_age}', color='Degree Status',
             barmode='group', title=f'Earnings by Program Type and Degree Status for Age Bracket {selected_age}')

# Show the plot
st.plotly_chart(fig)

st.write('Would you like to hear more perspectives about this? Check this episode of the Daily podcast from the New York Times: https://www.nytimes.com/2023/09/20/podcasts/the-daily/is-college-worth-it.html')
