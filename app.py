# Import necessary libraries
import plotly.express as px
from shiny import reactive, render, ui, App
from shinywidgets import render_plotly
import palmerpenguins
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Palmer Penguins dataset
penguinsdata_df = palmerpenguins.load_penguins()

# --- Define Reactive Functions ---

# This function lets us filter data based on user selections
@reactive.Calc
def filtered_data():
    return penguinsdata_df[
        penguinsdata_df['species'].isin(input.selected_species()) &
        penguinsdata_df['island'].isin(input.selected_islands())
    ]

# --- UI Definition ---

app_ui = ui.page_fluid(
    ui.h1("Penguins Dataset Exploration"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.h3("Filter Options"),
            # Slider for selecting sample size
            ui.input_slider("n", "Sample Size", 0, 100, 20),
            # Slider for setting bin count in the Seaborn histogram
            ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 50, 500, 200),
            # Checkbox group for filtering by penguin species
            ui.input_checkbox_group(
                "selected_species", 
                "Penguin Species", 
                {"Chinstrap": "Chinstrap", "Gentoo": "Gentoo", "Adelie": "Adelie"},
                selected=["Chinstrap", "Gentoo", "Adelie"]
            ),
            # Checkbox group for filtering by island
            ui.input_checkbox_group(
                "selected_islands", 
                "Select Islands", 
                {"Biscoe": "Biscoe", "Dream": "Dream", "Torgersen": "Torgersen"},
                selected=["Biscoe", "Dream", "Torgersen"]
            )
        ),
        # Main panel to display visualizations
        ui.panel_main(
            ui.h4("Body Mass Distribution (Seaborn)"),
            ui.output_plot("seaborn_histogram")
        )
    )
)

# --- Server Logic ---

def server(input, output, session):
    
    # Render Seaborn histogram for body mass distribution
    @output.seaborn_histogram
    @render.plot
    def seaborn_histogram():
        # Create a plot area
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create a histogram using Seaborn to show body mass distribution
        sns.histplot(
            data=filtered_data(),
            x="body_mass_g",           # Data for x-axis: body mass
            hue="species",             # Color by species
            multiple="stack",          # Stack the histogram for clarity
            bins=input.seaborn_bin_count(),  # Set bin count based on user input
            ax=ax
        )
        
        # Customize the plot with title and labels
        ax.set_title("Body Mass Distribution by Species")
        ax.set_xlabel("Body Mass (g)")
        ax.set_ylabel("Count")
        
        # Ensure plot layout is adjusted properly
        fig.tight_layout()
        
        # Return the figure to be displayed
        return fig

# --- Run the App ---
app = App(app_ui, server)
