from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber, save_fiber_to_csv
from numpy import pi

theta_fluctuations = [(pi / (2 ** i), i) for i in range(8, 4, -1)]
delta_fluctuations = [(pi / (2 ** i), i) for i in range(8, 4, -1)]
max_progress = len(theta_fluctuations) * len(delta_fluctuations) * 220
progress = 0
for theta_fluctuation, i_t in theta_fluctuations:
    for delta_fluctuation, i_d in delta_fluctuations:
        for i in range(100):
            segments = 1000
            fiber = OpticalFiber(
                nr_of_segments=segments,
                temporal_pmd_theta_fluctuation=theta_fluctuation,
                temporal_pmd_delta_fluctuation=delta_fluctuation
            )
            save_fiber_to_csv(fiber, f"Fibers/FibersLength1000/fiber_n{segments}_t{i_t}_d{i_d}_v{i}.csv")
            progress += 1
            print(f"Progress: {progress}/{max_progress}")
        for i in range(100):
            segments = 10000
            fiber = OpticalFiber(
                nr_of_segments=segments,
                temporal_pmd_theta_fluctuation=theta_fluctuation,
                temporal_pmd_delta_fluctuation=delta_fluctuation
            )
            save_fiber_to_csv(fiber, f"Fibers/FibersLength10000/fiber_{segments}_t{i_t}_d{i_d}_v{i}.csv")
            progress += 1
            print(f"Progress: {progress}/{max_progress}")
        for i in range(20):
            segments = 100000
            fiber = OpticalFiber(
                nr_of_segments=segments,
                temporal_pmd_theta_fluctuation=theta_fluctuation,
                temporal_pmd_delta_fluctuation=delta_fluctuation
            )
            save_fiber_to_csv(fiber, f"Fibers/FibersLength100000/fiber_{segments}_t{i_t}_d{i_d}_v{i}.csv")
            progress += 1
            print(f"Progress: {progress}/{max_progress}")
