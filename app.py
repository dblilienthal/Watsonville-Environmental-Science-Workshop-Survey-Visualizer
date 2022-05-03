from re import S
from numpy import size
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
 
STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""
 
 
class FileUpload(object):
 
    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Upload file", type=['csv'])
        show_file = st.empty()
        if not file:
            show_file.info("Please upload a file of type: csv")
            return pd.DataFrame() # Returns a blank dataframe to avoid error. Might want to fix later 
        else:
            data = pd.read_csv(file)
            file.close()

            return data


 
if __name__ ==  "__main__":

    # Logo
    st.image('./WESW Logo.png')
    
    # Title
    st.header("Watsonville Environmental Workshop Survey Visualizer")

    helper = FileUpload()
    data = helper.run()
    # If the data has been populated
    if data.shape != (0,0):

        ### Snapshot of the dataset
        st.caption('Snapshot of uploaded dataset')
        st.dataframe(data.head(10))

        ### Sidebar code
        st.sidebar.header('Features to graph')
        st.sidebar.subheader('Timestamp column')
        timeseries_column = st.sidebar.selectbox("Time Column (The column that has the time the survey was taken)", data.columns.tolist())
        st.sidebar.subheader('Target Column')
        column = st.sidebar.selectbox("The column you want to graph", data.columns.tolist())
        
        st.sidebar.subheader('Date Input')
        start_date = st.sidebar.date_input('Start date')
        end_date = st.sidebar.date_input('End date')

        # Check to make sure the dates are okay
        if (start_date > end_date):
            st.sidebar.header('Please fix the dates. Start date is greater than end date.')

        print(start_date)

        st.sidebar.subheader('Number of results')
        top_num_freq = st.sidebar.slider(f'Top number of results', 1, 30)

        st.sidebar.subheader('Graphing Options')
        width = st.sidebar.slider("plot width", 1, 25, 5)
        height = st.sidebar.slider("plot height", 1, 25, 5)
        title_font_size = st.sidebar.slider("Title Size", 1, 50, 10)
        axis_label_size = st.sidebar.slider("X/Y Label Size", 1, 30, 10)
        
        # Click for button 
        clicked = st.sidebar.button('Make Graph')
        if clicked:
            print("Selected columns:", column)
            print('Time column:', timeseries_column)

            data[timeseries_column] = pd.to_datetime(data[timeseries_column]) # Convert the timecolumn to datetime
            data = data[(data[timeseries_column] >= str(start_date)) & (data[timeseries_column] <= str(end_date))] # Filter by dates

            # Getting the data
            result_dict = {}
            for row in data[column].astype(str):
                try:
                    items = row.split(', ')
                    for item in items:
                        result_dict[item] = result_dict.get(item, 0) + 1 
                except:
                    pass
                
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=False))
            print(result_dict)
            val_count_df = pd.DataFrame.from_dict(result_dict, orient='index')[:top_num_freq]
            # val_count_df = data[column].astype(str).value_counts()[:top_num_freq]  # Geting value counts by selected column
            # val_count_df.sort_values(ascending=True, inplace=True)
            st.dataframe(val_count_df)

            y_values = val_count_df.index.tolist()
            x_values = val_count_df.values.flatten()

            fig, ax = plt.subplots(figsize=(width, height))
            ax.barh(y_values, x_values)
            ax.set_title(f'{column}', size=title_font_size)
            ax.set_xticks(range(max(x_values)+1), fontsize=axis_label_size)
            ax.set_yticks(y_values, fontsize=axis_label_size)
            print(axis_label_size)

            st.pyplot(fig)







