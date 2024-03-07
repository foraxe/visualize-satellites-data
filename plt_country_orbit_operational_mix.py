import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset into a pandas DataFrame using ISO-8859-1 encoding
dirname= r"G:\OtherProject\visualize_satellites\ucsusa.org_sites_default_files_2023-06_UCS-Satellite-Database-1-1-2023.txt"
df = pd.read_csv(dirname, sep="\t", encoding='ISO-8859-1')

# 1. Satellites by Country
satellites_by_country = df['Country of Operator/Owner'].value_counts()

# 2. Orbit Types
orbit_types = df['Class of Orbit'].value_counts()

# 3. Operational or Non-operational
df['Launch Year'] = pd.to_datetime(df['Date of Launch'], errors='coerce').dt.year
df['Operational Status'] = (2023 - df['Launch Year'] <= df['Expected Lifetime (yrs.)']).replace({True: 'Operational', False: 'Non-operational'})
operational_status = df['Operational Status'].value_counts()

# Group the data by Launch Year and Country
grouped_by_country = df.groupby(['Launch Year', 'Country of Operator/Owner']).size().unstack().fillna(0)

# Plot the results for the top 5 countries with the most satellites
top_countries = satellites_by_country.head(5).index
grouped_by_country[top_countries].plot(figsize=(15, 7), title="Satellites Launched by Top 5 Countries Over the Years")
plt.ylabel('Number of Satellites Launched')
plt.xlabel('Launch Year')
plt.legend(title="Country")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Group the data by Launch Year and Orbit Type
grouped_by_orbit = df.groupby(['Launch Year', 'Class of Orbit']).size().unstack().fillna(0)

# Plot the results for the different orbit types
grouped_by_orbit.plot(figsize=(15, 7), title="Satellites Launched by Orbit Type Over the Years")
plt.ylabel('Number of Satellites Launched')
plt.xlabel('Launch Year')
plt.legend(title="Orbit Type")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Group the data by Launch Year and Operational Status
grouped_by_status = df.groupby(['Launch Year', 'Operational Status']).size().unstack().fillna(0)

# Plot the results for operational vs. non-operational satellites
grouped_by_status.plot(figsize=(15, 7), title="Operational vs. Non-operational Satellites Over the Years")
plt.ylabel('Number of Satellites Launched')
plt.xlabel('Launch Year')
plt.legend(title="Operational Status")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Convert the Perigee and Apogee columns to numeric, coercing non-numeric values to NaN
df['Perigee (km)'] = pd.to_numeric(df['Perigee (km)'], errors='coerce')
df['Apogee (km)'] = pd.to_numeric(df['Apogee (km)'], errors='coerce')

# Calculate the average altitude again
df['Average Altitude'] = (df['Perigee (km)'] + df['Apogee (km)']) / 2

# Group by Launch Year and Average Altitude, and count the number of satellites
grouped_data = df.groupby(['Launch Year', 'Average Altitude']).size().reset_index(name='Number of Satellites')

# Plotting
plt.figure(figsize=(15, 10))
plt.scatter(grouped_data['Launch Year'], grouped_data['Average Altitude'], 
            s=grouped_data['Number of Satellites']*10, # Multiply by a factor to make it more visually clear
            alpha=0.6, edgecolors="w", linewidth=0.5)

plt.title("Number of Satellites by Year and Altitude")
plt.xlabel("Year")
plt.ylabel("Average Altitude (km)")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Set up the figure and axes
fig, axs = plt.subplots(5, 1, figsize=(15, 25))

# 1. Time Series of Satellite Launches
df['Launch Year'].value_counts().sort_index().plot(ax=axs[0], linestyle='-', marker='o', color='blue')
axs[0].set_title("Number of Satellite Launches Over the Years")
axs[0].set_ylabel("Number of Satellites")
axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)

# 2. Distribution of Satellites by Country (Top 10 countries)
satellites_by_country.head(10).plot(kind='bar', ax=axs[1], color='green')
axs[1].set_title("Top 10 Countries by Number of Satellites Operated")
axs[1].set_ylabel("Number of Satellites")
axs[1].grid(axis='y', which='both', linestyle='--', linewidth=0.5)

# 3. Purpose of Satellites
df['Purpose'].value_counts().head(10).plot(kind='barh', ax=axs[2], color='orange')
axs[2].set_title("Top 10 Purposes of Satellites")
axs[2].set_xlabel("Number of Satellites")
axs[2].grid(axis='x', which='both', linestyle='--', linewidth=0.5)

# 4. Altitude Distribution
df['Average Altitude'].plot(kind='hist', bins=50, ax=axs[3], color='purple')
axs[3].set_title("Distribution of Satellites by Altitude")
axs[3].set_xlabel("Average Altitude (km)")
axs[3].grid(True, which='both', linestyle='--', linewidth=0.5)

# 5. Orbit Type Distribution
orbit_types.plot(kind='bar', ax=axs[4], color='red')
axs[4].set_title("Distribution of Satellites by Orbit Type")
axs[4].set_ylabel("Number of Satellites")
axs[4].grid(axis='y', which='both', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.show()


# Set up the figure and axes
fig, axs = plt.subplots(5, 1, figsize=(15, 30))

# 6. Operational Status over Time
grouped_by_status.unstack().plot(kind='bar', stacked=True, ax=axs[0], colormap="viridis")
axs[0].set_title("Operational vs. Non-operational Satellites Over the Years")
axs[0].set_ylabel("Number of Satellites")
axs[0].grid(axis='y', which='both', linestyle='--', linewidth=0.5)

# 7. Heatmap of Launch Sites (top 10 for visualization clarity)
top_launch_sites = df['Launch Site'].value_counts().head(10).index
launch_sites_data = df[df['Launch Site'].isin(top_launch_sites)]
pivot_launch_sites = launch_sites_data.groupby(['Launch Year', 'Launch Site']).size().unstack().fillna(0)
axs[1].imshow(pivot_launch_sites.T, cmap="YlGnBu", aspect='auto')
axs[1].set_title("Top 10 Launch Sites Activity Over the Years")
axs[1].set_yticks(range(len(top_launch_sites)))
axs[1].set_yticklabels(top_launch_sites)
axs[1].set_xlabel("Year")
axs[1].set_ylabel("Launch Site")

# 8. Satellite Lifetimes
df['Expected Lifetime (yrs.)'].plot(kind='hist', bins=50, ax=axs[2], color='purple')
axs[2].set_title("Distribution of Expected Satellite Lifetimes")
axs[2].set_xlabel("Expected Lifetime (years)")
axs[2].grid(True, which='both', linestyle='--', linewidth=0.5)

# 9. Satellite Launches by Contractor (top 10)
df['Contractor'].value_counts().head(10).plot(kind='barh', ax=axs[3], color='cyan')
axs[3].set_title("Top 10 Satellite Contractors")
axs[3].set_xlabel("Number of Satellites")
axs[3].grid(axis='x', which='both', linestyle='--', linewidth=0.5)

# 10. Correlation Matrix (selecting a subset of numerical columns for clarity)
correlation_columns = ['Perigee (km)', 'Apogee (km)', 'Launch Mass (kg.)', 'Power (watts)', 'Expected Lifetime (yrs.)']
# correlation_data = df[correlation_columns].corr()

# Remove non-numeric characters from the columns and convert them to float
for column in correlation_columns:
    df[column] = df[column].replace('[^\d.]', '', regex=True).astype(float)

# Re-calculate the correlation
correlation_data_fixed = df[correlation_columns].corr()
correlation_data_fixed

cax = axs[4].matshow(correlation_data_fixed, cmap="coolwarm")
fig.colorbar(cax)
axs[4].set_title("Correlation Matrix", pad=20)
axs[4].set_xticks(range(len(correlation_columns)))
axs[4].set_xticklabels(correlation_columns, rotation=45)
axs[4].set_yticks(range(len(correlation_columns)))
axs[4].set_yticklabels(correlation_columns)

plt.tight_layout()
plt.show()