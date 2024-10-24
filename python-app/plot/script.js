document.addEventListener('DOMContentLoaded', async () => {
    const whiteMatchMatrixDiv = document.getElementById('white-match-matrix');
    const blackMatchMatrixDiv = document.getElementById('black-match-matrix');

    // Fetch match data from the server
    const matchData = await fetch('http://127.0.0.1:8888/data').then(response => response.json());

    // Get all neural network engines and non-neural network engines
    const neuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 1);
    const nonNeuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 0);

    // Set up grid templates for both matrices
    whiteMatchMatrixDiv.style.gridTemplateColumns = `repeat(${nonNeuralEngines.length}, 100px)`;
    blackMatchMatrixDiv.style.gridTemplateColumns = `repeat(${nonNeuralEngines.length}, 100px)`;

    // Loop through each neural engine to create rows for both matrices
    neuralEngines.forEach(neuralEngine => {
        const whiteRowDiv = document.createElement('div');
        whiteRowDiv.classList.add('row');
        
        const blackRowDiv = document.createElement('div');
        blackRowDiv.classList.add('row');

        // Loop through each non-neural engine to create cells for both matrices
        nonNeuralEngines.forEach(nonNeuralEngine => {
            // Cell for the white matrix (neural engine as white)
            const whiteCellDiv = document.createElement('div');
            whiteCellDiv.classList.add('cell');
            const whiteMatch = matchData.matches.find(match => 
                match.brancas_id === neuralEngine.id && match.negras_id === nonNeuralEngine.id);
            whiteCellDiv.classList.add(getResultClass(whiteMatch, neuralEngine.id, nonNeuralEngine.id));

            // Cell for the black matrix (neural engine as black)
            const blackCellDiv = document.createElement('div');
            blackCellDiv.classList.add('cell');
            const blackMatch = matchData.matches.find(match => 
                match.negras_id === neuralEngine.id && match.brancas_id === nonNeuralEngine.id);
            blackCellDiv.classList.add(getResultClass(blackMatch, neuralEngine.id, nonNeuralEngine.id));

            // Append cells to respective rows
            whiteRowDiv.appendChild(whiteCellDiv);
            blackRowDiv.appendChild(blackCellDiv);
        });

        // Append the rows to the corresponding match matrices
        whiteMatchMatrixDiv.appendChild(whiteRowDiv);
        blackMatchMatrixDiv.appendChild(blackRowDiv);
    });
});

// Function to determine the result class based on match outcome
function getResultClass(match, neuralEngineId, nonNeuralEngineId) {
    if (!match || !match.vencedor_id) {
        return 'white'; // Draw
    }
    return match.vencedor_id === neuralEngineId ? 'yellow' : 'pink';
}
