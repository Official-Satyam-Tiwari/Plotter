import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score

st.set_option('deprecation.showPyplotGlobalUse', False)
nav = st.sidebar.radio("Navigation",["Single Plotter","Multiple Plotter","Conversion to CSV","Coming Soon","About Us"],index=0)

if nav=="Single Plotter":
	st.title("Plotter - Just upload it")
	try:
		name = st.file_uploader('Upload a CSV',type=["csv"])
		df = pd.read_csv(name)
		st.write(df)
	except ValueError:
		pass
	x_name = st.selectbox("Select column for x-axis:",df.columns.tolist())
	y_name = st.selectbox("Select column for y-axis:",df.columns.tolist()) #its a dictionary
	
	x_label = st.text_input("Enter x-label:")
	y_label = st.text_input("Enter y-label:")
	title = st.text_input("Enter title of the plot:")

	plt.figure(figsize=(8,6))
	try:
		plt.scatter(df[x_name],df[y_name])
		plt.xlabel(x_label)
		plt.ylabel(y_label)
		plt.title(title)
		st.pyplot()
	except:
		pass
	if st.checkbox("Apply LSF:",value=False):
		try:
			x = np.array(df[x_name])
			y = np.array(df[y_name])
			A = np.vstack([x, np.ones(len(x))]).T
			m, c = np.linalg.lstsq(A, y, rcond=None)[0]
			y_pred = m*x + c
			r_squared = r2_score(y, y_pred)
			plt.plot(x,y,"o",label="Original Data",markersize=10)
			plt.plot(x,y_pred,"r",label="Fitted Line")
			plt.xlabel(x_label)
			plt.ylabel(y_label)
			plt.title(title)
			plt.legend()
			st.success(f"Slope = {m} & Intercept = {c}")
			plt.show()
			st.pyplot()
			st.info(f"\nEquation of Fitted Line : y = {m:.2f} x + {c:.2f}\n\nR-Squared Error = {r_squared}")
			plt.savefig("myplot.png",bbox_inches="tight")
			with open("myplot.png", "rb") as file:
				btn = st.download_button(label="Download Plot",data=file,file_name="myplot.png",mime="image/png")
				st.warning("Currently Download Button not working...")
		except:
			st.write("First upload the data and input the names of columns to plot.")
if nav=="Conversion to CSV":
	st.title("Conversion to CSV file")
	st.write("### How to Convert Table Data to CSV")
	st.write("To convert a table kind of data into a CSV file, follow these steps:")
	st.write("""
1. Open the table in a spreadsheet software like Microsoft Excel, Google Sheets, or LibreOffice Calc.

2. Select all the data you want to convert to CSV. You can do this by clicking and dragging your mouse over the cells, or by using keyboard shortcuts like Ctrl+A (Windows) or Command+A (Mac) to select all.

3. Once you have selected all the data, go to the File menu and choose the "Save As" option.

4. In the "Save As" dialog box, choose "CSV (Comma delimited)" as the file format.

5. Choose a location on your computer to save the file, and give it a name.

6. Click the "Save" button to save the file as a CSV.

7. If your spreadsheet software prompts you to confirm any formatting issues, review them and ensure they align with your expectations.

Your table data should now be saved in CSV format, which can be opened in a wide range of applications and tools.""")
	st.write("Thanks for reading! If you have any questions or feedback, please feel free to reach out to us at 22n0292@iitb.ac.in .")
	st.info("You may also use any free online converter such as : https://cloudconvert.com/csv-converter")

if nav == "Multiple Plotter":
	st.title("Plotter - Just upload it")
	try:
		name = st.file_uploader('Upload a CSV',type=["csv"])
		df = pd.read_csv(name)
		st.write(df)
	except ValueError:
		pass
	x_name = st.selectbox("Select column for x-axis:",df.columns.tolist())
	y_name = st.multiselect("Select columns for y-axis:",df.columns.tolist()) #its a dictionary
	x_label = st.text_input("Enter x-label:")
	y_label = st.text_input("Enter y-label:")
	st.write(x_label,y_label)
	title = st.text_input("Enter title of the plot:")
#	sns.scatterplot(x = x_name,y = y_name,data=df)
	#st.write(x_name,y_name,df[x_name],df[y_name],sns.scatterplot(x = x_name,y = y_name,data=df))
	#st.pyplot()

	#plt.figure(figsize=(8,6))
	try:	
		fig, ax = plt.subplots()
		for i in range(len(y_name)):
			ax.scatter(df[x_name],df[y_name[i]],label=y_name[i])
		if len(x_label)==0:
			ax.set_xlabel(x_name)
		else:
			ax.set_xlabel(x_label)
		if len(y_label)==0:
			ax.set_ylabel(y_name)
		else:
			ax.set_ylabel(y_label)
		if len(title)==0:
			ax.set_title(name.name[:-len(".csv")])
		else:
			ax.set_title(title)
		ax.legend()
		st.pyplot(fig)
	except ValueError:
		pass
	if st.checkbox("Apply LSF:",value=False):
		try:
			x = np.array(df[x_name])
			y = np.array(df[y_name])
			m = []
			c = []
			r_s = []
			for i in range(len(y_name)):
				A = np.vstack([x, np.ones(len(x))]).T
				m.append(np.linalg.lstsq(A, y, rcond=None)[0][0][0])
				c.append(np.linalg.lstsq(A, y, rcond=None)[0][1][0])
				m = np.array(m)
				c = np.array(c)
				#st.write(np.linalg.lstsq(A, y, rcond=None)[0][1][0])
				y_pred = m*x + c
				#st.write(y_pred)
				r_s.append(r2_score(y, y_pred[i]))
				ax.plot(x,y[i],label=y_name[i]+"Original Line",markersize=10)
				ax.plot(x,y_pred[i],"r",label=y_name[i]+"Fitted Line")
				ax.set_xlabel(x_label)
				ax.set_ylabel(y_label[i])
				ax.set_title(title)
				st.success(f"For {y_name[i]}, Slope = {m[i]} & Intercept = {c[i]}")
				st.info(f"\nEquation of Fitted Line : y = {m[i]:.2f} x + {c[i]:.2f}\n\nR-Squared Error = {r_s[i]}")
			ax.legend()
			st.pyplot(fig)
		except:
			st.write("(LSF, not working yet) First upload the data and input the names of columns to plot.")

if nav == "About Us":
	st.title("About Us")
	#st.image("aboutus.jpg	")
	st.write("Welcome to my web app!\n\nI'm SATYAM TIWARI a data enthusiast from India, passionate about helping people explore and visualize data in new and meaningful ways.\n\nMy goal is to create a user-friendly platform that makes data analysis accessible to everyone. \n\nThanks for using our app and supporting our mission to make data more approachable! \n\n #### Made with :heart: in Bharat :flag-in:")

if nav=="Coming Soon":
	st.title("Features that are coming soon...")
	st.write("""
    1. _Interactive plot_: Add interactivity to your plot, such as zooming, panning, or hover effects.

    2. _Custom themes_: Create custom themes for your plot that match your brand or your user's preferences.

    3. _Export options_: Allow users to export the plot in various formats, such as PNG, SVG, or PDF.

    4. _Data filtering_: Allow users to filter the data before plotting, such as selecting specific columns or rows.

    5. _Machine learning_: Using machine learning algorithms to analyze the data and provide insights.

    6. _Integration_: Integrating our plotter with other tools and platforms, such as Jupyter notebooks, GitHub, or Slack.
		""")
