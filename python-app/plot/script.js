document.addEventListener('DOMContentLoaded', async () => {
    const matchMatrixDiv = document.getElementById('match-matrix');

    // Fetch match data from the server (requires a PHP endpoint)
    const matchData = await fetch('http://127.0.0.1:8888/data').then(response => response.json());

    // Get all neural network engines and non-neural network engines
    const neuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 1);
    const nonNeuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 0);

    console.log(neuralEngines)

    // Set up grid template
    matchMatrixDiv.style.gridTemplateColumns = `repeat(${nonNeuralEngines.length}, 100px)`;

    // Loop through each neural engine and create a row for each
    neuralEngines.forEach(neuralEngine => {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('row');

        // Loop through each non-neural engine to create cells
        nonNeuralEngines.forEach(nonNeuralEngine => {
            const cellDiv = document.createElement('div');
            cellDiv.classList.add('cell');

            // Fetch the results for the two matches between these two engines
            const matches = matchData.matches.filter(match =>
                (match.brancas_id === neuralEngine.id && match.negras_id === nonNeuralEngine.id) ||
                (match.brancas_id === nonNeuralEngine.id && match.negras_id === neuralEngine.id)
            );

            // Create the first cell part for the match where neuralEngine is white
            const firstPart = document.createElement('div');
            firstPart.classList.add('cell-part');
            const firstMatch = matches.find(match => match.brancas_id === neuralEngine.id);
            firstPart.classList.add(getResultClass(firstMatch, neuralEngine.id, nonNeuralEngine.id));

            // Create the second cell part for the match where neuralEngine is black
            const secondPart = document.createElement('div');
            secondPart.classList.add('cell-part');
            const secondMatch = matches.find(match => match.negras_id === neuralEngine.id);
            secondPart.classList.add(getResultClass(secondMatch, neuralEngine.id, nonNeuralEngine.id));

            // Append both parts to the cell and the cell to the row
            cellDiv.appendChild(firstPart);
            cellDiv.appendChild(secondPart);
            rowDiv.appendChild(cellDiv);
        });

        // Append the row to the match matrix
        matchMatrixDiv.appendChild(rowDiv);
    });
});

// Function to determine the result class based on match outcome
function getResultClass(match, neuralEngineId, nonNeuralEngineId) {
    if (!match || !match.vencedor_id) {
        return 'white'; // Draw
    }
    return match.vencedor_id === neuralEngineId ? 'yellow' : 'pink';
}
