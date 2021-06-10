# SAD
<p> Trabalho da materia Sistemas de apoio à decisão.</p>
<p> Foi construido um Sistema para aumentar a efitividade da distribuição de salas de uma universidade.</p>

<h2> Como executar o projeto </h2>
<ul>
  <li>Crie o banco de dados usando os arquivos de configuração na pasta "arquivos de configuração do banco"</li>
  <li>Altere o aquivo "src/Model/BancoDeDados/banco.py" para fazer a conexão com o seu banco de dados</li>
  <li>Instale as bibliotecas necessarias para execução do projeto, que são sqlalchemy e o pandas</li>
  <li>Após isso basta executar o arquivo "controller.py" que fica dentro do diretorio "src" </li>
</ul>

<h2>Como começar a otimização</h2>
<p>O Sistema recebe como entrada 2 arquivos CSV, que contem a configuração de salas e turmas.</p>
<p>Alem disso recebe:</p>
<ul>
    <li>Pesos: são 3 numeros separados por virgula, representando o peso para cada das taxas de qualidade</li>
    <li>Temperatura: Um unico numero maior que 2, preferencialmente um numero proximo de 1000</li>
    <li>Fator de resfriamento: Um numero entre 0 e 1 que representa a fator de redução da tempuratura </li>
    <li>Numero maximo de iterações por temperatura: um numero inteiro qualquer</li>
</ul>

<h2>Alterando a solução</h2>
<p>Após utilizar a otimização é exibida uma tabela com uma solução inicial, com as colunas: ID sala, dia da semana, horario, codigo da turma e ID da turma. A partir disso o Usuario pode fazer buscas de salas e turmas para buscar informações completas a respeito das turmas ou salas e a partir dessas informações é possivel realizar a troca de salas entre duas turmas. Para todas essas trocas são calculadas novas taxas de qualidade que são exibidas na barra lateral.</p>
<p>Por fim, o usuario pode salvar ou carregar uma solução no banco de dados, para persistir seus dados, ou reverter todas alterações e voltar ao estado inicial. 
