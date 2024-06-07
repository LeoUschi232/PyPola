from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber, save_fiber_to_csv
from numpy import pi

theta_fluctuations = [(pi / (2 ** i), i) for i in range(8, 4, -1)]
delta_fluctuations = [(pi / (2 ** i), i) for i in range(8, 4, -1)]
segment_counts = [(1000, 100), (10000, 100), (100000, 20), (1000000, 5)]
max_progress = len(theta_fluctuations) * len(delta_fluctuations) * sum([i for _, i in segment_counts])
progress = 0
for theta_fluctuation, i_t in theta_fluctuations:
    for delta_fluctuation, i_d in delta_fluctuations:
        for segments, versions in segment_counts:
            for v in range(versions):
                fiber = OpticalFiber(
                    nr_of_segments=segments,
                    temporal_pmd_theta_fluctuation=theta_fluctuation,
                    temporal_pmd_delta_fluctuation=delta_fluctuation
                )
                save_fiber_to_csv(fiber, f"Fibers/FibersLength{segments}/fiber_{segments}_t{i_t}_d{i_d}_v{v}.csv")
                progress += 1
                print(f"Progress: {progress}/{max_progress}")
