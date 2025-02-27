import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

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
    st.subheader("Results:")
    st.write(f"Given a positive test result, the probability of actually having COVID-19 is: {posterior:.2%}")
    st.subheader("Explanation:")
    st.write(f"- Prevalence (Prior Probability): {prior:.2%}")
    st.write(f"- Test Sensitivity: {sensitivity:.2%}")
    st.write(f"- Test Specificity: {specificity:.2%}")
    st.write(f"- False Positive Rate: {(1 - specificity):.2%}")
    
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
    st.pyplot(plt)

# Streamlit UI
st.title("COVID-19 Test Probability Calculator")
prior = st.slider("Prevalence (Prior Probability)", 0.0, 1.0, 0.01, 0.01)
sensitivity = st.slider("Test Sensitivity", 0.0, 1.0, 0.95, 0.01)
specificity = st.slider("Test Specificity", 0.0, 1.0, 0.98, 0.01)

update_plot(prior, sensitivity, specificity)