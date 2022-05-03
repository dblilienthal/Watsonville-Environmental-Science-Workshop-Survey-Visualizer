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

    helper = FileUpload() # Loading in the CSV file
    data = helper.run()
    # If the data has been populated
    if data.shape != (0,0):

        ### Snapshot of the dataset
        st.subheader('Snapshot of uploaded dataset')
        st.caption('Last 10 results')
        st.dataframe(data.tail(10)) # Shows last 10 results

        ### Sidebar code
        st.sidebar.header('Features to graph')
        st.sidebar.subheader('Timestamp column')
        timeseries_column = st.sidebar.selectbox("The column that has the time the survey was taken", data.columns.tolist()) # Shows all the columns in the dataset
        st.sidebar.subheader('Target Column')
        column = st.sidebar.selectbox("The column you want to graph", data.columns.tolist()) # Shows all the columns in the dataset
        st.sidebar.subheader('Date Range')
        start_date = st.sidebar.date_input('Start date') # Start date
        end_date = st.sidebar.date_input('End date') # End Date

        # Check to make sure the dates are okay
        if (start_date > end_date):
            st.sidebar.header('Please fix the dates. Start date is greater than end date.')

        # Showing the top n results (5 is default)
        st.sidebar.subheader('Number of results')
        top_num_freq = st.sidebar.slider(f'Top number of results', 1, 50, 5)

        # Graphing options
        st.sidebar.subheader('Graphing Options')
        width = st.sidebar.slider("plot width", 1, 25, 5) # Width
        height = st.sidebar.slider("plot height", 1, 25, 5)  # Height
        title_font_size = st.sidebar.slider("Title Size", 1, 50, 10) # Font size
        axis_label_size = st.sidebar.slider("X/Y Label Size", 1, 30, 10) # Axis label size
        
        # Click for button 
        clicked = st.sidebar.button('Make Graph')
        ### If the button has been clicked
        if clicked: 
            print("Selected columns:", column)
            print('Time column:', timeseries_column)

            data[timeseries_column] = pd.to_datetime(data[timeseries_column]) # Convert the timecolumn to datetime
            data = data[(data[timeseries_column] >= str(start_date)) & (data[timeseries_column] <= str(end_date))] # Filter by dates

            # Putting the data into a dictionary by times it appears.
            # This also accounts for values seperated by commas
            result_dict = {}
            for row in data[column].astype(str):
                try:
                    items = row.split(', ')
                    for item in items:
                        result_dict[item] = result_dict.get(item, 0) + 1 
                except:
                    pass
                
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=False)) # Reversing the dictionary to start with higher counts first
            val_count_df = pd.DataFrame.from_dict(result_dict, orient='index')[:top_num_freq] # Getting the top N results
            y_values = val_count_df.index.tolist() # Converting the y-values to list 
            x_values = val_count_df.values.flatten() # Converting the x-values to list
            print(result_dict, y_values, x_values, sep='\n')

            ### Graph code
            st.subheader('Graph')
            fig, ax = plt.subplots(figsize=(width, height)) # Creating the subplot
            ax.barh(y_values, x_values) # Adding the values to the plot
            ax.set_title(f'{column}', size=title_font_size) # Creating the title
            ax.set_xticks(range(max(x_values)+1)) # Setting the x-labels
            ax.set_xticklabels(range(max(x_values)+1), size=axis_label_size) # Setting the x-label size
            ax.set_yticklabels(y_values, size=axis_label_size) # Setting the y-label size
            st.pyplot(fig) # Pasting the plot to streamlit

            # Showing the actual data below
            st.subheader('Actual Data')
            st.dataframe(val_count_df.rename(columns={0:column})[::-1]) # Showing the dataframe







