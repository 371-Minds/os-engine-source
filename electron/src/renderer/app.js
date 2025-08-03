// Monaco Editor setup
require.config({ paths: { vs: '../node_modules/monaco-editor/min/vs' } });

require(['vs/editor/editor.main'], function () {
    const editor = monaco.editor.create(document.getElementById('editor-container'), {
        value: '// Place your code here and click "Analyze Code"\n',
        language: 'javascript',
        theme: 'vs-dark'
    });

    const executeBtn = document.getElementById('execute-btn');
    const resultOutput = document.getElementById('result-output');

    executeBtn.addEventListener('click', async () => {
        const code = editor.getValue();
        resultOutput.textContent = 'Analyzing...';

        try {
            const response = await fetch('http://127.0.0.1:5000/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ submission: code }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            resultOutput.textContent = JSON.stringify(data.result, null, 2);

        } catch (error) {
            console.error('Error:', error);
            resultOutput.textContent = 'Error: ' + error.message;
        }
    });
});
