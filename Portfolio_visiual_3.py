import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import streamlit as st

class HeatMap():
    def __init__(self, df):
        self.df = df
        
    def show_data_heatmp(self, chart_type):
        colormaps = [
            'PuBuGn','coolwarm','YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'PuBu', 'viridis', 'OrRd', 
    'PuRd', 'RdPu', 'GnBu', 'Spectral', 'cool', 'warm', 'bwr', 'seismic',
    'cubehelix', 'afmhot', 'gist_heat', 'copper', 'autumn', 'spring', 
    'summer', 'winter', 'bone', 'pink', 'ocean', 'gist_earth', 'terrain', 
    'CMRmap', 'gnuplot', 'gnuplot2', 'brg', 'jet', 'rainbow', 
    'nipy_spectral', 'gist_ncar', 'plasma', 'inferno', 'magma', 'cividis',
            'Blues', 'BuGn', 'BuPu', 'GnBu', 'Oranges', 'Greens',
            'Purples', 'Reds', 'Greys', 'PiYG', 'PRGn', 'BrBG',
            'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
            'twilight', 'twilight_shifted', 'hsv'
        ]


        num_columns_heatmap = st.multiselect(f"Select columns for line :", self.df.columns.tolist() ,key= f"{chart_type}columns")
        values_heatmap = st.selectbox("enter y axis value:",  self.df.columns.tolist() ,key= f"{chart_type}values")
        colormaps_heatmap = st.selectbox('select colormaps:', colormaps)
        fig_size_heatmap = st.radio("Change figure size", ["No", "Yes"], key=f"{chart_type} fig_size_bar")
        annot_heatmap = st.radio("Display numbers:", ['No', 'Yes'], key=f"{chart_type}annot")
        if annot_heatmap == 'Yes':
            annot_display = True
        else:
            annot_display = False
            
        if fig_size_heatmap == "Yes":
            self.fig_width_heat = st.number_input("Enter the figure width:", min_value=4, value = 16 , key=f"{chart_type} figure_width")
            self.fig_height_heat = st.number_input("Enter the figure height:", min_value=4, value = 7, key=f"{chart_type} figure_height")
            
            plt.figure(figsize=(self.fig_width_heat, self.fig_height_heat))
        else:
            self.fig_width_heat = 16
            self.fig_height_heat = 7
            plt.figure(figsize=(self.fig_width_heat, self.fig_height_heat))
        
        df_heatmap = self.df[num_columns_heatmap]
        if chart_type == 'heatmap':
                
            try:
                sns.heatmap(df_heatmap, cmap = colormaps_heatmap, annot= annot_display )
            except ValueError:
                st.error("Invalid input")
            plt.title("Heatmap")
            
        elif chart_type == 'clustered_heatmap':
            
            try:
                sns.clustermap(df_heatmap, cmap = colormaps_heatmap, annot= annot_display )
            except ValueError:
                st.error("Invalid input")
            plt.title("Clusterd Heatmap")

            
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
    
    def final_heatmap_logic(self):
        chart_type = 'heatmap'
        st.title("Heatmap")
        
        self.show_data_heatmp(chart_type)
        
        self.download_chart(chart_type)
    
    def clustered_heatmap_logic(self):
        chart_type = 'clustered_heatmap'
        st.title('Clustered Heatmap')
        
        self.show_data_heatmp(chart_type)
        
        self.download_chart(chart_type)
    def pivot_heatmap(self):
        colormaps_pivot_list = [
            'coolwarm','viridis', 'plasma', 'inferno', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'PuBu', 'PuBuGn', 'OrRd', 
    'PuRd', 'RdPu', 'GnBu', 'Spectral', 'cool', 'warm', 'bwr', 'seismic',
    'cubehelix', 'afmhot', 'gist_heat', 'copper', 'autumn', 'spring', 
    'summer', 'winter', 'bone', 'pink', 'ocean', 'gist_earth', 'terrain', 
    'CMRmap', 'gnuplot', 'gnuplot2', 'brg', 'jet', 'rainbow', 
    'nipy_spectral', 'gist_ncar','magma', 'cividis',
            'Blues', 'BuGn', 'BuPu', 'GnBu', 'Oranges', 'Greens',
            'Purples', 'Reds', 'Greys', 'PiYG', 'PRGn', 'BrBG',
            'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
            'twilight', 'twilight_shifted', 'hsv'
        ]
        chart_type = 'pivot'
        
        st.title('Heatmap with Pivot')
        index_pivot = st.selectbox('select index of heatmap:', self.df.columns.tolist() ,key= f"{chart_type}index")   
        column_pivot = st.selectbox('Select columns of heatmap:', self.df.columns.tolist(), key=f"{chart_type}columns")
        values_pivot = st.selectbox('Select valuse of heatmap:', self.df.columns.tolist(), key= f"{chart_type}values")
        colormaps_pivot = st.selectbox('select colormaps:', colormaps_pivot_list)
        aggfun_pivot = st.selectbox('Select aggregate function of heatmap:', ['None','mean','sum','count','min','max'], key= f"{chart_type}aggfun")
        try:
            if aggfun_pivot == 'None':
                
                pivot_df = self.df.pivot_table(index = index_pivot, columns = column_pivot, values= values_pivot)
            else:
                pivot_df = self.df.pivot_table(index = index_pivot, columns = column_pivot, values= values_pivot, aggfunc = aggfun_pivot)
                
            
            annot_pivot = st.radio('display numbers:', ['No','Yes'])
            linewidth_pivot = st.radio('Select Linewidth:', ['No','Yes'])
            if linewidth_pivot == "Yes":
                values_of_line = st.number_input("Enter the line Width:", min_value=0.1, value = 0.5 , key=f"{chart_type} figure_line_width")
            else:
                values_of_line = 0.5

            if annot_pivot == "Yes":
                annot_value = True
            else:
                annot_value = False

            fig_size_pivot = st.radio("Change figure size", ["No", "Yes"], key=f"{chart_type} fig_size_bar")

            if fig_size_pivot == "Yes":
                self.fig_width_heat = st.number_input("Enter the figure width:", min_value=4, value = 16 , key=f"{chart_type} figure_width")
                self.fig_height_heat = st.number_input("Enter the figure height:", min_value=4, value = 7, key=f"{chart_type} figure_height")

                plt.figure(figsize=(self.fig_width_heat, self.fig_height_heat))
            else:
                self.fig_width_heat = 16
                self.fig_height_heat = 7
                plt.figure(figsize=(self.fig_width_heat, self.fig_height_heat))



            sns.heatmap(pivot_df, annot= annot_value,cmap= colormaps_pivot, linewidths = values_of_line )
            plt.text(0, -0.5, f"Values column: '{values_pivot}'", fontsize=12, color='blue', ha='center')


            self.download_chart(chart_type)
        except ValueError:
            st.error("Pivot table creation failed. Check selected inputs.")
            
            
    def main(self, data_visulization_op3):
        if data_visulization_op3 == 'Heatmap':
            self.final_heatmap_logic()
        elif data_visulization_op3 == 'Clustered  Heatmap':
            self.clustered_heatmap_logic()
        elif data_visulization_op3 == 'Heatmap with pivot':
            self.pivot_heatmap()

    
