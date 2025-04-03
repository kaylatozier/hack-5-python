import streamlit as st
import pandas as pd
import numpy as np
import time

from wf_script import Population

st.title('Simple Wright-Fisher Simulation of Genetic Drift')
# Create a new Population
# As a reminder these are the default values for population size (N)
# and initial derived allele frequency (f).
#   N=10, f=0.2
p = Population()

# Initialize the chart with the initial allele frequency of the derived
# allele. `line_chart` expects a list, so we must wrap `p.f` in square
# brackets to pass a list
chart = st.line_chart([p.f])
N = st.sidebar.slider("# of Generations", 10, 1000, 10, 10)
freq = st.sidebar.slider("Allele Frequency", 0.0, 1.0, 0.2,0.01)
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# Initially we'll run a loop 50 times
for i in range(1, N):
    # Step 1 wf generation
    p.step(ngens=1)
    # Calculate the current derived allele freqsuency
    freq = np.sum(p.pop)/len(p.pop)
    # Update the chart to add the current allele frequency
    chart.add_rows([freq])
    status_text.text(f"{round((i/N)*100)}% complete")
    progress_bar.progress(i/N)
    # sleep for a small amount of time so you can watch the animation
    time.sleep(0.05)

status_text.text(f"{100}% complete")


progress_bar.empty()

# Add a button to rerun the simulation
st.button("Rerun")

