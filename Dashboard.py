import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel data
df = pd.read_excel("cancer_data_2020.xlsx")

# Page Title
st.title("Sri Lanka Cancer Incidence Dashboard (2020)")
st.write("Explore cancer cases by gender and type.")

# Sidebar - Filter by Gender
st.sidebar.header("Filters")
gender_option = st.sidebar.selectbox("Select Gender", ("All", "Male", "Female"))

# Convert wide data to long format
df_long = df.melt(id_vars="Cancer Type", value_vars=["Male", "Female"],
                  var_name="Gender", value_name="Case_Count")

# Apply Gender Filter
if gender_option != "All":
    df_filtered = df_long[df_long["Gender"] == gender_option]
else:
    df_filtered = df_long

# 1. Total Cases (Metric)
st.metric("Total Cancer Cases", int(df_filtered["Case_Count"].sum()))

# 2. Top 10 Cancer Types (Bar Chart)
st.subheader("Top 10 Most Common Cancers")
top10 = df_filtered.groupby("Cancer Type")["Case_Count"].sum().sort_values(ascending=False).head(10).reset_index()
fig_top10 = px.bar(top10, x="Case_Count", y="Cancer Type", orientation="h", color="Case_Count", color_continuous_scale="Blues")
st.plotly_chart(fig_top10)

# 3. Line Chart - Cancer Cases Across Types
st.subheader("Cancer Cases Across Cancer Types (Line Chart)")
fig_line = px.line(df_filtered.groupby("Cancer Type")["Case_Count"].sum().reset_index(),
                   x="Cancer Type", y="Case_Count", title="Cancer Cases by Type")
st.plotly_chart(fig_line)

# 4. Bar Chart - Top 10 Cancer Types
st.subheader("Top 10 Most Common Cancer Types")

# Group by Cancer Type and sum the cases
top_cancers = df_filtered.groupby("Cancer Type")["Case_Count"].sum().sort_values(ascending=False).head(10).reset_index()

# Create a bar chart
fig_bar = px.bar(
    top_cancers,
    x="Case_Count",
    y="Cancer Type",
    orientation="h",
    title="Top 10 Cancer Types by Case Count",
    labels={"Case_Count": "Number of Cases", "Cancer Type": "Type of Cancer"},
    text_auto=True  
)

fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_bar)

# 5. Donut Chart for Gender Distribution
if gender_option == "All":
    st.subheader("Gender-wise Distribution (Donut Chart)")
    gender_counts = df[["Male", "Female"]].sum()
    fig_donut = px.pie(values=gender_counts.values, names=gender_counts.index,
                       hole=0.5, title="Gender-wise Distribution")
    st.plotly_chart(fig_donut)

# 6. Top 5 Male Cancer Types (Bar Chart)
st.subheader("Top 5 Male Cancer Types")
top5_male = df[["Cancer Type", "Male"]].sort_values(by="Male", ascending=False).head(5)
fig_male = px.bar(top5_male, x="Male", y="Cancer Type", orientation="h", title="Top 5 Male Cancers", color="Male")
st.plotly_chart(fig_male)

# 7. Top 5 Female Cancer Types (Bar Chart)
st.subheader("Top 5 Female Cancer Types")
top5_female = df[["Cancer Type", "Female"]].sort_values(by="Female", ascending=False).head(5)
fig_female = px.bar(top5_female, x="Female", y="Cancer Type", orientation="h", title="Top 5 Female Cancers", color="Female")
st.plotly_chart(fig_female)

# 8. Male vs Female Cancer Cases (Grouped Bar Chart)
st.subheader("Male vs Female Cancer Cases (Grouped Bar)")
fig_grouped = px.bar(df, x="Cancer Type", y=["Male", "Female"],
                     title="Male vs Female Cancer Cases",
                     barmode="group")
st.plotly_chart(fig_grouped)

# 9. Cancer Types with Few Cases (<10 cases)
st.subheader("Rare Cancer Types (Less than 10 cases)")
rare_cancers = df[(df["Male"] + df["Female"]) < 10]
fig_rare = px.bar(rare_cancers, x="Cancer Type", y=["Male", "Female"], title="Rare Cancer Types")
st.plotly_chart(fig_rare)

# 10. Average Cases by Cancer Type (Scatter Plot)
st.subheader("Average Cases by Cancer Type (Scatter Plot)")
df["Average"] = (df["Male"] + df["Female"]) / 2
fig_avg = px.scatter(df, x="Cancer Type", y="Average", title="Average Cases by Cancer Type")
st.plotly_chart(fig_avg)

# Footer
st.markdown("---")
st.markdown("Developed for DSPL Coursework | Mohammed Alfar 2025")
