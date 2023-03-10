import numpy as np
import pylab as plt


def errors(err_list):
    plt.plot(err_list)
    plt.xlabel("# Basis elements")
    plt.ylabel("Error")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig("basis_error.png")


def basis(rb_matrix):
    num_elements = len(rb_matrix)
    total_frames = 125
    n_models_per_frame = int(num_elements / total_frames)
    if n_models_per_frame < 1:
        n_models_per_frame = 1
    fig, ax = plt.subplots(total_frames, 1, figsize=(4.5, 2.5 * total_frames))
    for i in range(total_frames):
        start_i = int(i * n_models_per_frame)
        end_i = int(start_i + n_models_per_frame)
        for model_id in range(start_i, end_i):
            if end_i < num_elements:
                h = rb_matrix[model_id]
                ax[i].plot(h, color=f"C{model_id}", alpha=0.7)
        ax[i].set_title(f"Basis element {start_i:003}-{end_i:003}")
    plt.tight_layout()
    fig.savefig("basis.png")


def compare_rom_to_true(ROM, model_params_in):
    """Compare computed ROM to input model"""

    model_params = ROM.model.params_dtype(**model_params_in)

    domain = ROM.model.domain

    model_full = ROM.model.compute(model_params, domain)
    model_nodes = ROM.model.compute(model_params, ROM.empirical_interpolant.nodes)
    model_rom = ROM.evaluate(model_params)

    plt.semilogx(domain, model_rom, label="ROM", alpha=0.5, linestyle="--")
    plt.semilogx(domain, model_full, label="Full model", alpha=0.5)
    plt.scatter(ROM.empirical_interpolant.nodes, model_nodes, s=1)
    plt.legend()

    np.save("ROM_diff", np.subtract(model_rom, model_full))
    plt.savefig("comparison.pdf", bbox_inches="tight")
