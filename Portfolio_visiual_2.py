#Bar chart
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import streamlit as st


class Bar_Chart():
    def __init__(self, df):
        self.df = df
        self.fig_width_bar = 16
        self.fig_height_bar = 7
        
        
    def show_data_bar_chart(self, chart_type):
        maximum_lines = st.number_input("Enter the number of lines:", min_value=1, value=1, key=f"{chart_type}1_num_lines_unique")
        self.x_axis = st.selectbox("Select X-axis:", self.df.columns.tolist(), key=f"{chart_type}x_axis_unique_key")
        maximum_num_heads = st.number_input("Enter the number of entities to display:", min_value=1, value=50,  key=f"{chart_type}max_head_unique_key")
        fig_size_bar = st.radio("Change figure size", ["No", "Yes"], key=f"{chart_type} fig_size_bar")
        if fig_size_bar == "Yes":  
            self.fig_width_bar = st.number_input("Enter the figure width:", min_value=4, value = 16 , key=f"{chart_type} figure_width")
            self.fig_height_bar = st.number_input("Enter the figure height:", min_value=4, value = 7, key=f"{chart_type} figure_height")
            self.rotation_inp = st.number_input("Enter degree of rotation:", min_value=0 , value= 45, key=f"{chart_type} rotation_inp") 
            plt.title("Bar Chart")
            plt.figure(figsize=(self.fig_width_bar, self.fig_height_bar))
        else:
            self.fig_width = 16
            self.fig_height = 7
            self.rotation_inp = 45
            plt.figure(figsize=(self.fig_width_bar, self.fig_height_bar))
        width = 0.8 / maximum_lines

        x_values = self.df[self.x_axis].head(maximum_num_heads).values
        
        for i in range(maximum_lines):
            y_axis_bar = st.selectbox(f"Select Y-axis for line {i + 1}:", self.df.columns.tolist() ,key= i)
            color_inp = st.color_picker(f"Choose color for {y_axis_bar}:", value='#FF0000',key=f"color_picker_bar{i}")
            
            bar_positions = np.arange(len(x_values)) + (i - (maximum_lines - 1) / 2) * width
            
            plt.bar(bar_positions, self.df[y_axis_bar].head(maximum_num_heads), width=width, color=color_inp, label= y_axis_bar)
      
        plt.xticks(np.arange(len(x_values)), x_values, rotation=self.rotation_inp)
        
    def download_chart(self, value_key):
        plt.xlabel(self.x_axis)
        
        plt.ylabel('Values')
        
        plt.legend()
        
        # Save the figure to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        st.pyplot(plt)

        st.download_button(
            label="Download Chart",
            data=buf,
            file_name="line_chart.png",
            mime="image/png",
            key= f"{value_key}"
        )
        
    def bar_chart_logic(self):
        chart_type= "bar_chart"
            
        self.show_data_bar_chart(chart_type)
        

        self.download_chart(chart_type)
    
    def main(self):
        self.bar_chart_logic()