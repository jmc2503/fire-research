import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fps_data = np.loadtxt("FrameRateData.txt")
path_find_latency = np.loadtxt("PathFindTimes.txt")
render_scale_data = pd.read_csv("ovr_data.csv", usecols=["render_scale"])

render_scale_data = render_scale_data['render_scale'].values


# Step 1: Sort data
sorted_data = np.sort(fps_data)
sorted_data_path = np.sort(path_find_latency)
sorted_render_scale = np.sort(render_scale_data)

# Step 2: Compute ECDF values
n = len(sorted_data)
ecdf = np.arange(1, n+1) / n  # Cumulative probabilities

n_path = len(sorted_data_path)
ecdf_path = np.arange(1, n_path+1) / n_path  # Cumulative probabilities

n_scale = len(sorted_render_scale)
ecdf_scale = np.arange(1, n_scale+1) / n_scale

# Step 3: Plot ECDF
plt.figure(1)
plt.step(sorted_data, ecdf, where="post")
plt.xlim([40, 100])
plt.xlabel("Frame Rate (fps)")
plt.ylabel("Cumulative Probability")
plt.grid()
plt.title("Frame Rate Empirical CDF")

plt.figure(2)
plt.step(sorted_data_path, ecdf_path, where="post")
plt.xlim([40, 500])
plt.xlabel("Time to Find Path (μs)")
plt.ylabel("Cumulative Probability")
plt.title("Latency Empirical CDF")
plt.grid()

plt.figure(3)
plt.step(sorted_render_scale, ecdf_scale, where="post")
plt.xlim([80, 150])
plt.xlabel("Render Scaling (%)")
plt.ylabel("Cumulative Probability")
plt.title("Render Scaling Empirical CDF")
plt.grid()
plt.show()

print(np.mean(fps_data))
print(np.mean(path_find_latency))
print(np.mean(render_scale_data))