import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import BytesIO

class Pie_chart():
    def __init__(self, df):
        self.df = df
        
    def show_data_pie_chart(self, chart_type):
        st.title('Pie Chart')
        labels_pie_chart = st.selectbox('Select the labels:', self.df.columns.tolist(), key=f"{chart_type}labels")
        data_pie_chart_col = st.selectbox('Select data:', self.df.columns.tolist(),key=f"{chart_type}data")

        try:
            if not pd.api.types.is_numeric_dtype(self.df[data_pie_chart_col]):
                self.df[data_pie_chart_col] = pd.to_numeric(self.df[data_pie_chart_col], errors='coerce')
            data_pie_chart = self.df.groupby(labels_pie_chart)[data_pie_chart_col].sum().dropna()

            num_selected_labels = len(data_pie_chart)
            explode_user_inp = st.radio('want to explode the chart:',['No', 'Yes'], key=f"{chart_type}explod_inp")

            # Handle explosion of pie chart segments
            if explode_user_inp == 'Yes':
                explode_pie_chart = [st.number_input(f'Select explode value for section {i + 1}:', min_value=0.0, max_value=1.0, value=0.0, step=0.1, key=f"{i}pie_chart_explode") for i in range(num_selected_labels)]
            else:
                explode_pie_chart = [0] * num_selected_labels

            startangl_pie = st.radio('edit start angle:',['No', 'Yes'],key=f"{chart_type}angle_inp")
            if startangl_pie == 'Yes':
                number_inp_angle = st.number_input("enter angle:", min_value=0, max_value=360, value= 0, key= f"{chart_type}angle")
            else:
                number_inp_angle = 0
                
            # color_inp = st.radio('Change color:', ["No", "Yes"])
            # if color_inp == 'Yes':
            #     for i in range (num_selected_labels):
                    
            #         color_pie_chart = st.color_picker(f"Choose color for {self.df[i]}:",key=f"color_picker_pie{i}")
            # else:
            #     pass
                
            data_column_inp = st.radio('Edit data column:' , ['No', 'Yes'])
            if data_column_inp == 'Yes':
                data_color_inp = st.color_picker('change color:')
            else:
                data_color_inp = 'blue'
                
            fig_size_pie_chart = st.radio("Change figure size", ["No", "Yes"], key=f"{chart_type} fig_size_pie")

            if fig_size_pie_chart == "Yes":
                self.fig_width_pie_chart = st.number_input("Enter the figure width:", min_value=4, value = 16 , key=f"{chart_type} figure_width")
                self.fig_height_pie_chart = st.number_input("Enter the figure height:", min_value=4, value = 7, key=f"{chart_type} figure_height")

                plt.figure(figsize=(self.fig_width_pie_chart, self.fig_height_pie_chart))
            else:
                self.fig_width_pie_chart= 16
                self.fig_height_pie_chart = 7
                plt.figure(figsize=(self.fig_width_pie_chart, self.fig_height_pie_chart))

            
            plt.pie(data_pie_chart, labels= data_pie_chart.index,explode=explode_pie_chart, autopct='%1.1f%%', startangle= number_inp_angle)
            plt.text(1.5, 1.2, f"data column: '{data_pie_chart}'", fontsize=12, color= data_color_inp, ha='left')
            plt.axis('equal')
            plt.title('Pie Chart')
        except ValueError:
            st.error("Please select correct data.")
            
    def download_chart(self, value_key):
       
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
        
    def final_pie_chart(self):
        chart_type = 'pie_chart'
        plt.title("Pie Chart")
        self.show_data_pie_chart(chart_type)
        
        self.download_chart(chart_type)
    
    def main(self):
        self.final_pie_chart()