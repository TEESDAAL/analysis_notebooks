import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np, altair, pandas as pd
    from ast import literal_eval
    return altair, literal_eval, pd


@app.cell
def _():
    file_path = 'scatter'

    with open(file_path, 'r') as file:
        file_content = file.read()
    return (file_content,)


@app.cell
def _(file_content, literal_eval):
    runs_data = literal_eval(file_content)
    runs_data = [run[0] for run in runs_data]
    return (runs_data,)


@app.cell
def _(mo):
    mo.md(
        """
    # Interactive Prediction Visualiser for each generation
    For seed 0 with a KNN surrogate with a vector length of 70 (10 all 7 decision situations)
    """
    )
    return


@app.cell
def _(mo, runs_data):
    generation = mo.ui.slider(0, len(runs_data) -1, label=f"Generation: ")
    generation
    return (generation,)


@app.cell
def _(generation, pd, runs_data):
    data = pd.DataFrame(runs_data[generation.value], columns=["True Fitness", "Predicted Fitness"])
    return (data,)


@app.cell
def _(altair, data, generation, mo):
    mo.ui.altair_chart(altair.Chart(data).mark_point().encode(
        x='True Fitness',
        y='Predicted Fitness'
        #color='Origin'
    ).properties(
        title=f'Predicted vs True Fitness ({len(data)} points) for generation {generation.value}'
    ))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(""" """)
    return


@app.cell
def _(mo):
    mo.md("""We see some very strange behaviour at generation 0 that is not continued through the other generations""")
    return


@app.cell
def _(mo):
    mo.md(
        """
    Perhaps it is an issue with how I'm evaluating the individuals?
    ```java

    Population oldPopulation = state.population;
    Population intermediatePopulation = breedIntermediatePopulation(state, originalPopulationShape);
    // This feels slightly suspicious but evaluating a population requires it to be part of a state
    state.population = intermediatePopulation; 

    List<GPIndividual> allIntermediateIndividuals = Arrays.stream(state.population.subpops)
        .flatMap(s -> Arrays.stream(s.individuals))
        .map(GPIndividual.class::cast)
        .toList();

    state.evaluator.evaluatePopulation(state); // Is there issues with instance rotation?
    state.population = oldPopulation;
    // Store the data
    scatterPlotRun.add(
            allIntermediateIndividuals.stream()
                    .map(i -> Pair.of(i.fitness.fitness(), cachedSurrogate(i))).toList()
    );
    ```
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
