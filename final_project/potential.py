# # Install necessary libraries (run once in Colab)
# !pip install pathway bokeh panel --quiet

# # --- Imports ---
# import numpy as np
# import pandas as pd
# import pathway as pw
# import bokeh.plotting
# import panel as pn

# # --- 1. Data Preparation (if needed, adjust file path as per your setup) ---
# # Assume you have a CSV named 'dataset.csv' with required columns.
# # If you already have a cleaned 'parking_stream.csv', you can skip this step.

# df = pd.read_csv('dataset.csv')

# # Combine date and time columns if needed
# if 'LastUpdatedDate' in df.columns and 'LastUpdatedTime' in df.columns:
#     df['Timestamp'] = pd.to_datetime(df['LastUpdatedDate'] + ' ' + df['LastUpdatedTime'],
#                                      format='%d-%m-%Y %H:%M:%S')
# else:
#     df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# # Sort by time
# df = df.sort_values('Timestamp').reset_index(drop=True)

# # If you have multiple lots, ensure a unique lot identifier column (e.g., LotID)
# if 'LotID' not in df.columns:
#     df['LotID'] = df['Latitude'].astype(str) + '_' + df['Longitude'].astype(str)

# # Save a streaming-ready CSV
# df[["Timestamp", "Occupancy", "Capacity", "LotID"]].to_csv("parking_stream.csv", index=False)

# # --- 2. Pathway Schema ---
# class ParkingSchema(pw.Schema):
#     Timestamp: str
#     Occupancy: int
#     Capacity: int
#     LotID: str

# # --- 3. Real-Time Data Ingestion with Pathway ---
# # Simulate real-time streaming at 100 rows/sec
# data = pw.demo.replay_csv(
#     "parking_stream.csv",
#     schema=ParkingSchema,
#     input_rate=100
# )

# # Parse timestamp for plotting
# fmt = "%Y-%m-%d %H:%M:%S"
# data_with_time = data.with_columns(
#     t = data.Timestamp.dt.strptime(fmt)
# )

# # --- 4. Model 1: Baseline Linear Pricing ---
# BASE_PRICE = 10.0
# ALPHA = 2.0  # Sensitivity parameter

# # Stateless price (for each row, price is BASE + ALPHA * (occ/cap))
# data_with_price = data_with_time.with_columns(
#     Price_Model1 = BASE_PRICE + ALPHA * (pw.this.Occupancy / pw.this.Capacity)
# )

# # --- 5. Real-Time Visualization with Bokeh and Panel ---
# pn.extension('bokeh')

# def price_plotter(source):
#     fig = bokeh.plotting.figure(
#         height=400,
#         width=800,
#         title="Model 1: Real-Time Parking Price per Lot",
#         x_axis_type="datetime",
#     )
#     # Plot each lot as a separate line
#     lots = list(set(source.data['LotID']))
#     colors = bokeh.palettes.Category10[10] + bokeh.palettes.Category20[20]
#     for i, lot in enumerate(lots):
#         mask = [l == lot for l in source.data['LotID']]
#         fig.line(
#             [t for t, m in zip(source.data['t'], mask) if m],
#             [p for p, m in zip(source.data['Price_Model1'], mask) if m],
#             line_width=2,
#             color=colors[i % len(colors)],
#             legend_label=f"Lot {lot}"
#         )
#     fig.legend.location = "top_left"
#     fig.xaxis.axis_label = 'Time'
#     fig.yaxis.axis_label = 'Price ($)'
#     return fig

# # Use Pathway's .plot() for real-time updates
# viz = data_with_price.plot(price_plotter, sorting_col="t")
# pn.Column(viz).servable()













# edit 1:














# # --- 1. Install Required Libraries ---
# !pip install pathway bokeh --quiet

# # --- 2. Imports ---
# import numpy as np
# import pandas as pd
# import pathway as pw
# import bokeh.plotting
# from bokeh.io import output_notebook, show

# # --- 3. Data Preparation ---
# # Load the dataset (replace with your actual file if needed)
# df = pd.read_csv('dataset.csv')

# # Combine date and time columns if needed
# if 'LastUpdatedDate' in df.columns and 'LastUpdatedTime' in df.columns:
#     df['Timestamp'] = pd.to_datetime(
#         df['LastUpdatedDate'] + ' ' + df['LastUpdatedTime'],
#         format='%d-%m-%Y %H:%M:%S'
#     )
# else:
#     df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# # Sort by time
# df = df.sort_values('Timestamp').reset_index(drop=True)

# # Ensure a unique lot identifier column (LotID)
# if 'LotID' not in df.columns:
#     df['LotID'] = df['Latitude'].astype(str) + '_' + df['Longitude'].astype(str)

# # Save a streaming-ready CSV for Pathway
# df[["Timestamp", "Occupancy", "Capacity", "LotID"]].to_csv("parking_stream.csv", index=False)

# # --- 4. Pathway Schema ---
# class ParkingSchema(pw.Schema):
#     Timestamp: str
#     Occupancy: int
#     Capacity: int
#     LotID: str

# # --- 5. Real-Time Data Ingestion with Pathway ---
# # Simulate real-time streaming at 100 rows/sec
# data = pw.demo.replay_csv(
#     "parking_stream.csv",
#     schema=ParkingSchema,
#     input_rate=100
# )

# # Parse timestamp for plotting
# fmt = "%Y-%m-%d %H:%M:%S"
# data_with_time = data.with_columns(
#     t = data.Timestamp.dt.strptime(fmt)
# )

# # --- 6. Model 1: Baseline Linear Pricing ---
# BASE_PRICE = 10.0
# ALPHA = 2.0  # Sensitivity parameter

# # Stateless price (for each row, price is BASE + ALPHA * (occ/cap))
# data_with_price = data_with_time.with_columns(
#     Price_Model1 = BASE_PRICE + ALPHA * (pw.this.Occupancy / pw.this.Capacity)
# )

# # --- 7. Collect Results for Visualization ---
# # Convert the Pathway table to a Pandas DataFrame for plotting
# df_price = data_with_price.to_pandas()

# # --- 8. Visualization with Bokeh ---
# output_notebook()

# def plot_all_lots(df):
#     fig = bokeh.plotting.figure(
#         height=400,
#         width=800,
#         title="Model 1: Real-Time Parking Price per Lot",
#         x_axis_type="datetime",
#     )
#     lots = df['LotID'].unique()
#     palette = bokeh.palettes.Category10[10] + bokeh.palettes.Category20[20]
#     for i, lot in enumerate(lots):
#         lot_df = df[df['LotID'] == lot]
#         fig.line(
#             lot_df['t'],
#             lot_df['Price_Model1'],
#             line_width=2,
#             color=palette[i % len(palette)],
#             legend_label=f"Lot {lot}"
#         )
#     fig.legend.location = "top_left"
#     fig.xaxis.axis_label = 'Time'
#     fig.yaxis.axis_label = 'Price ($)'
#     show(fig)

# plot_all_lots(df_price)

# # --- 9. (Optional) Save Results ---
# # df_price.to_csv("model1_price_output.csv", index=False)
