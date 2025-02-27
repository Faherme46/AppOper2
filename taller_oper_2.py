# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

def bayes_theorem(prior, sensitivity, specificity):
    false_positive_rate = 1 - specificity
    p_positive = (sensitivity * prior) + (false_positive_rate * (1 - prior))
    if p_positive == 0:
        return 0  # Evitar división por cero
    posterior = (sensitivity * prior) / p_positive
    return posterior

def update_plot(prior, sensitivity, specificity):
    posterior = bayes_theorem(prior, sensitivity, specificity)
    
    # Mostrar resultados
    print("\nResults:")
    print(f"Given a positive test result, the probability of actually having COVID-19 is: {posterior:.2%}")
    print("\nExplanation:")
    print(f"- Prevalence (Prior Probability): {prior:.2%}")
    print(f"- Test Sensitivity: {sensitivity:.2%}")
    print(f"- Test Specificity: {specificity:.2%}")
    print(f"- False Positive Rate: {(1 - specificity):.2%}")
    
    # Sensitivity analysis
    sensitivities = np.linspace(0, 1, 50)
    specificities = np.linspace(0, 1, 50)
    posteriors = []
    for spec in specificities:
        posteriors.append([bayes_theorem(prior, sens, spec) for sens in sensitivities])
    
    # Plot
    plt.figure(figsize=(8,6))
    for i, spec in enumerate(specificities[::10]):
        plt.plot(sensitivities, posteriors[i*10], label=f"Specificity: {spec:.2f}")
    
    plt.xlabel("Sensitivity")
    plt.ylabel("Posterior Probability P(A | B)")
    plt.title("Effect of Sensitivity and Specificity on Posterior Probability")
    plt.legend()
    plt.grid()
    plt.show()

# Sliders
prior_slider = widgets.FloatSlider(min=0, max=1, step=0.01, value=0.01, description="Prevalence")
sensitivity_slider = widgets.FloatSlider(min=0, max=1, step=0.01, value=0.95, description="Sensitivity")
specificity_slider = widgets.FloatSlider(min=0, max=1, step=0.01, value=0.98, description="Specificity")

# Interactive output
ui = widgets.VBox([prior_slider, sensitivity_slider, specificity_slider])
out = widgets.interactive_output(update_plot, {'prior': prior_slider, 'sensitivity': sensitivity_slider, 'specificity': specificity_slider})

display(ui, out)
