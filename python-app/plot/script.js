document.addEventListener('DOMContentLoaded', async () => {
    const whiteMatchMatrixDiv = document.getElementById('white-match-matrix');
    const blackMatchMatrixDiv = document.getElementById('black-match-matrix');

    // Fetch match data from the server
    const matchData = await fetch('http://127.0.0.1:8888/data').then(response => response.json());

    // Get all neural network engines and non-neural network engines
    const neuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 1);
    const nonNeuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 0);

    // Set up grid templates for both matrices
    whiteMatchMatrixDiv.style.gridTemplateColumns = `repeat(${nonNeuralEngines.length + 1}, 100px)`; // +1 for depth labels
    blackMatchMatrixDiv.style.gridTemplateColumns = `repeat(${nonNeuralEngines.length + 1}, 100px)`; // +1 for depth labels

    // Create column labels for the non-neural engines' depths (X-axis)
    const createColumnLabels = (container, matrixName) => {
        const labelRowDiv = document.createElement('div');
        labelRowDiv.classList.add('row');

        // Add a corner cell
        const cornerCell = document.createElement('div');
        cornerCell.classList.add('cell');
        labelRowDiv.appendChild(cornerCell);

        // Depth labels for non-neural engines (X-axis)
        nonNeuralEngines.forEach(engine => {
            const labelCell = document.createElement('div');
            labelCell.classList.add('cell');
            labelCell.textContent = `${engine.profundidade}`;
            labelRowDiv.appendChild(labelCell);
        });

        // Append the label row to the matrix container
        container.appendChild(labelRowDiv);

        // Add a title to indicate which matrix it is
        const title = document.createElement('h3');
        title.textContent = `${matrixName}: Neural Engines vs. Non-Neural Engines`;
        container.prepend(title);
    };

    // Add row labels for both matrices
    createColumnLabels(whiteMatchMatrixDiv, "White Pieces");
    createColumnLabels(blackMatchMatrixDiv, "Black Pieces");

    // Function to create rows with depth labels for neural engines (Y-axis)
    const createRows = (matrixDiv, isWhite) => {
        neuralEngines.forEach(neuralEngine => {
            const rowDiv = document.createElement('div');
            rowDiv.classList.add('row');

            // Add depth label for neural engine on the Y-axis
            const depthLabel = document.createElement('div');
            depthLabel.classList.add('cell');
            depthLabel.textContent = `${neuralEngine.profundidade}`;
            rowDiv.appendChild(depthLabel);

            // Loop through each non-neural engine to create cells
            nonNeuralEngines.forEach(nonNeuralEngine => {
                const cellDiv = document.createElement('div');
                cellDiv.classList.add('cell');

                // Find the match based on the color of the neural engine
                const match = matchData.matches.find(match => 
                    isWhite
                        ? match.brancas_id === neuralEngine.id && match.negras_id === nonNeuralEngine.id
                        : match.negras_id === neuralEngine.id && match.brancas_id === nonNeuralEngine.id
                );

                cellDiv.classList.add(getResultClass(match, neuralEngine.id, nonNeuralEngine.id));

                // Append the cell to the row
                rowDiv.appendChild(cellDiv);
            });

            // Append the row to the matrix
            matrixDiv.appendChild(rowDiv);
        });
    };

    // Create rows for both white and black matrices
    createRows(whiteMatchMatrixDiv, true);  // For matches where neural engine is white
    createRows(blackMatchMatrixDiv, false); // For matches where neural engine is black

    // Add axis labels (e.g., classic graph-style labels)
    const addAxisLabels = () => {
        // X-axis label: "Profundidade motores sem redes neurais"
        const xAxisLabelWhite = document.createElement('div');
        xAxisLabelWhite.classList.add('x-axis-label');
        xAxisLabelWhite.textContent = 'Profundidade motores sem redes neurais';
        whiteMatchMatrixDiv.appendChild(xAxisLabelWhite);

        const xAxisLabelBlack = document.createElement('div');
        xAxisLabelBlack.classList.add('x-axis-label');
        xAxisLabelBlack.textContent = 'Profundidade motores sem redes neurais';
        blackMatchMatrixDiv.appendChild(xAxisLabelBlack);

        // Y-axis label: "Profundidade motores com redes neurais" (rotated 90 degrees)
        const yAxisLabelWhite = document.createElement('div');
        yAxisLabelWhite.classList.add('y-axis-label');
        yAxisLabelWhite.textContent = 'Profundidade motores com redes neurais';
        whiteMatchMatrixDiv.prepend(yAxisLabelWhite);

        const yAxisLabelBlack = document.createElement('div');
        yAxisLabelBlack.classList.add('y-axis-label');
        yAxisLabelBlack.textContent = 'Profundidade motores com redes neurais';
        blackMatchMatrixDiv.prepend(yAxisLabelBlack);
    };

    // Call the function to add axis labels
    addAxisLabels();
});

// Function to determine the result class based on match outcome
function getResultClass(match, neuralEngineId, nonNeuralEngineId) {
    if (!match || !match.vencedor_id) {
        return 'white'; // Draw
    }
    return match.vencedor_id === neuralEngineId ? 'yellow' : 'pink';
}
