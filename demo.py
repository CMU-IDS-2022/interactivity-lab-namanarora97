import streamlit as st
import pandas as pd
import altair as alt

st.header('My first streamlit application here')

st.write('Hello World')

# Cache the return for each URL. If URL is same, don't execute function, return previous value
@st.cache
def load(url):
    return pd.read_json(url)

# Read old penguin data
df = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")


if st.checkbox('Show data'):
    st.write(df)

# with st.echo():    
#     scatter = alt.Chart(df).mark_point(tooltip=True).encode(
#         alt.X("Flipper Length (mm)", scale = alt.Scale(zero = False)),
#         alt.Y('Body Mass (g)', scale = alt.Scale(zero = False)),
#         alt.Color('Species'),
#     )

# scatter = alt.Chart(df).mark_point(tooltip=True).encode(
#     alt.X("Flipper Length (mm)", scale = alt.Scale(zero = False)),
#     alt.Y('Body Mass (g)', scale = alt.Scale(zero = False)),
#     alt.Color('Species'),
# )

# st.write(scatter)

# min_weight = st.slider(
#     "Minimum Body Mass",
#     2500, 
#     6500
# )

# st.write(min_weight)

# scatter_filtered = scatter.transform_filter(f"datum['Body Mass (g)'] >= {min_weight}")

# st.write(scatter_filtered)


# picked = alt.selection_single(on = 'mouseover')

# picked = alt.selection_multi()

# picked = alt.selection_interval()

# picked = alt.selection_interval(encodings = ['x'])

# picked = alt.selection_single(on = 'mouseover', fields = ['Species'])

# picked = alt.selection_single(on = 'mouseover', fields = ['Species', 'Island'])


# input_dropdown = alt.binding_select(
#     options = ['Adelie', 'Chinstrap', 'Gentoo'],
#     name = 'Species'    
# )

# picked = alt.selection_single(encodings = 'color', bind = input_dropdown)

# scatter = alt.Chart(df).mark_circle(tooltip=True, size = 100).encode(
#     alt.X("Flipper Length (mm)", scale = alt.Scale(zero = False)),
#     alt.Y('Body Mass (g)', scale = alt.Scale(zero = False)),
#     alt.Color('Species'),
#     # color = alt.condition(picked, "Species", alt.value('lightgray'))
# ).add_selection(picked)


# scatter = alt.Chart(df).mark_circle(tooltip=True, size = 100).encode(
#     alt.X("Flipper Length (mm)", scale = alt.Scale(zero = False)),
#     alt.Y('Body Mass (g)', scale = alt.Scale(zero = False)),
#     alt.Color('Species'),
#     # color = alt.condition(picked, "Species", alt.value('lightgray'))
# )

# scales = alt.selection_interval(bind = "scales")
# st.write(scatter.add_selection(scales))

# SHORTCUT!

brush = alt.selection_interval(
    encodings = ["x"]
)

scatter = alt.Chart(df).mark_circle(tooltip=True, size = 100).encode(
    alt.X("Flipper Length (mm)", scale = alt.Scale(zero = False)),
    alt.Y('Body Mass (g)', scale = alt.Scale(zero = False)),
    alt.Color('Species'),
    # color = alt.condition(picked, "Species", alt.value('lightgray'))
).interactive().add_selection(brush)

hist =  alt.Chart(df).mark_bar().encode(
    alt.X('Body Mass (g)', bin = True),
    alt.Y('count()'),
    alt.Color('Species')
).transform_filter(
    brush
)

st.write(scatter & hist)