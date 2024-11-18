document.addEventListener('DOMContentLoaded', async () => {
    // Referências aos contêineres das matrizes para cada cenário
    const whiteMatchMatrixDivs = [
        document.getElementById('white-match-matrix')
    ];
    const blackMatchMatrixDivs = [
        document.getElementById('black-match-matrix')
    ];

    // Buscar dados de partida do servidor
    const matchData = await fetch('http://127.0.0.1:8888/data').then(response => response.json());

    const neuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 1);
    const nonNeuralEngines = matchData.engines.filter(engine => engine.redes_neurais === 0);

    const scenarioId = 6

    // Configuração das colunas em grid para cada cenário
    whiteMatchMatrixDivs.concat(blackMatchMatrixDivs).forEach(matrixDiv => {
        matrixDiv.style.gridTemplateColumns = `repeat(${nonNeuralEngines.length + 1}, 100px)`;
    });

    // Função para criar rótulos de coluna para cada cenário
    const createColumnLabels = (container) => {
        const labelRowDiv = document.createElement('div');
        labelRowDiv.classList.add('row');
        
        const cornerCell = document.createElement('div');
        cornerCell.classList.add('cell');
        labelRowDiv.appendChild(cornerCell);

        nonNeuralEngines.forEach(engine => {
            const labelCell = document.createElement('div');
            labelCell.classList.add('cell');
            labelCell.textContent = `${engine.profundidade}`;
            labelRowDiv.appendChild(labelCell);
        });

        container.appendChild(labelRowDiv);
    };

    // Adicionando rótulos de coluna para todas as matrizes
    whiteMatchMatrixDivs.forEach(createColumnLabels);
    blackMatchMatrixDivs.forEach(createColumnLabels);

    // Função para criar linhas de acordo com o cenário e a cor das peças
    const createRowsByScenario = (matrixDiv, isWhite, scenarioId) => {
        neuralEngines.forEach(neuralEngine => {
            const rowDiv = document.createElement('div');
            rowDiv.classList.add('row');

            const depthLabel = document.createElement('div');
            depthLabel.classList.add('cell');
            depthLabel.textContent = `${neuralEngine.profundidade}`;
            rowDiv.appendChild(depthLabel);

            nonNeuralEngines.forEach(nonNeuralEngine => {
                const cellDiv = document.createElement('div');
                cellDiv.classList.add('cell');

                // Encontrar a partida com base na cor e no cenário
                const match = matchData.matches.find(match =>
                    match.cenario_id === scenarioId &&
                    (isWhite
                        ? match.brancas_id === neuralEngine.id && match.negras_id === nonNeuralEngine.id
                        : match.negras_id === neuralEngine.id && match.brancas_id === nonNeuralEngine.id)
                );

                // Adicionar classe de resultado e id da partida dentro da célula
                cellDiv.classList.add(getResultClass(match, neuralEngine.id, nonNeuralEngine.id));
                //cellDiv.textContent = match ? `${match.id}` : '---'; // Exibe o ID da partida, ou deixa em branco se não houver partida

                rowDiv.appendChild(cellDiv);
            });

            matrixDiv.appendChild(rowDiv);
        });
    };

    // Criando linhas para todas as combinações de cor pro cenário
    createRowsByScenario(whiteMatchMatrixDivs[0], true, scenarioId);
    createRowsByScenario(blackMatchMatrixDivs[0], false, scenarioId);
});

// Função para determinar a classe de resultado com base no resultado da partida
function getResultClass(match, neuralEngineId, nonNeuralEngineId) {
    if (!match || !match.vencedor_id) {
        return 'white'; // Empate
    }
    return match.vencedor_id === neuralEngineId ? 'yellow' : 'pink';
}