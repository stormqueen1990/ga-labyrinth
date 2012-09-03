Um labirinto auto-solucionável, implementado utilizando técnicas de algoritmos genéticos.
Requer <a href="http://www.pyside.org/" target="_blank">PySide</a> para rodar.

Parâmetros:
<ul>
<li><b>População inicial:</b> a quantidade de indivíduos na geração da primeira população</li>
<li><b>Tipo de parada:</b> critério para a parada da geração de indivíduos. Pode ser Aptidão, onde se deverá informar um valor de aptidão, e o algoritmo para quando encontrar um indivíduo com aptidão menor ou igual àquela; ou Número de gerações, que gera a quantidade de gerações informada e então para a execução.</li>
<li><b>Valor para parada:</b> o valor de Aptidão ou Número de gerações, conforme informado no parâmetro anterior.</li>
<li><b>Tipo de seleção:</b> critério de seleção dos indivíduos. Pode ser Torneio ou Aptidão (roleta).</li>
<li><b>Taxa de mutação:</b> valor de 0 a 100 representando a porcentagem de mutação nos indivíduos.</li>
<li><b>Taxa de crossover:</b> valor de 0 a 100 representando a porcentagem de crossover na geração dos filhos.</li>
<li><b>Qtd. pontos de crossover:</b> número de pontos a cortar nos indivíduos para mesclar os materiais genéticos</li>
<li><b>Tamanho do caminho:</b> quantidade de direções nos caminhos da primeira geração.</li>
</ul>

An auto-solving labyrinth exit problem implemented with genetic algorithm techniques.
Requires <a href="http://www.pyside.org/" target="_blank">PySide</a> to run.

Simply hit ./gui.py to run the simulator.
