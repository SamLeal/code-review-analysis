# 📈 Caracterizando a atividade de code review no github 

## 1) Introdução
O presente relatório visa analisar as características sobre a prática de code review.
Essa prática consiste na interação entre desenvolvedores e revisores visando inspecionar o código produzido antes de integrá-lo à base principal. Assim, garante-se a qualidade do código integrado, evitando-se também a inclusão de defeitos.
No contexto de sistemas open source, mais especificamente dos desenvolvidos através do GitHub, as atividades de code review acontecem a partir da avaliação de contribuições submetidas por meio de Pull Requests (PR). Ou seja, para que se integre um código na branch principal, é necessário que seja realizada uma solicitação de pull, que será avaliada e discutida por um colaborador do projeto. Ao final, a solicitação de merge pode ser aprovada ou rejeitada pelo revisor. Em muitos casos, ferramentas de verificação estática realizam uma primeira análise, avaliando requisitos de estilo de programação ou padrões definidos pela organização.

Neste contexto, o objetivo deste laboratório é analisar a atividade de code review desenvolvida em repositórios populares do GitHub, identificando variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados

## 2) Metodologia:
Inicialmente, para extrair as informações foi utilizada a API GraphQL para realização das consultas. Foram realizadas duas querys: uma para extrair os dados dos repositórios populares (com no mínimo 100 estrelas e que continham os pullRequests com status 'MERGED' ou 'CLOSED') e outra para extrair as informações dos pullRequests com a restrição dos mesmos possuírem no mínimo uma hora de revisão. 

É válido ressaltar que na primeira versão do código utilizado para a extração dos dados, a API não funcionou corretamente retornando 'Rate limit remaining: 5000'. Esse erro indica que foi atingido o limite de requisições permitido pela API do GITHUB para o token de acesso. Sendo assim, foram executadas tentativas para solucionar esse problema como utilizar o 'time.sleep(10)' no qual aumenta o tempo de espera da requisição. Porém, mesmo com diversos testes não foi possível solucionar o problema o que colaborou para a refatoração completa do código.

Desse modo, após a refatoração realizada foi possível obter os dados dos pullRequets referentes aos repositórios analisados. Logo, os dados coletados foram salvos em arquivos CSV para compultar o dataset. Posteriormente, foram construídos os gráficos para as questões de pesquisa e realizada a análise para a conclusão das hipóteses estabelecidas baseando-se nos dados e métricas coletadas.


## 3) Resultados Obtidos 
Diante da base extraída, foi realizado um filtro no código de modo que printasse no console os nomes dos PR que foram skipados pelo fato de possuir menos de 1 hora. Foi extremamente notório que a grande maioria foi desconsiderada pelo fato de muitos PRs serem revisados de forma automática: utilizando ferramentas de CI/CD ou bots. Além disso, com o alto índice do uso da inteligência artificial nos últimos meses, indica que a automatização desse processo de análise pode ter sido impactada para colaborar que o tempo de análise seja menor que 1 hora. 


* **RQ 01. Qual a relação entre o tamanho dos PRs e o feedback final das revisões?**
       
    **Métrica:** 

    **Resultado:** 

    **Discussão do resultado:** 

* **RQ 02. Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?**
       
    **Métrica:** 

    **Resultado:** 
    **Discussão do resultado:** 

* **RQ 03. Qual a relação entre a descrição dos PRs e o feedback final das revisões?**
       
    **Métrica:** 

    **Resultado:**  
    
    **Discussão do resultado:**

* **RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?**
       
    **Métrica:** 

    **Resultado:** 

    **Discussão do resultado:** 
    
* **RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?**
       
    **Métrica:** 

    **Resultado:** 

    **Discussão do resultado:** 

* **RQ 05. Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?**
       
    **Métrica:** 

    **Resultado:** 

    **Discussão do resultado:** 

* **RQ 06. Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?**
       
    **Métrica:** 

    **Resultado:** 

    **Discussão do resultado:** 

* **RQ 07. Qual a relação entre a descrição dos PRs e o número de revisões realizadas?**
       
    **Métrica:** 

    **Resultado:** 

    **Discussão do resultado:** 

* **RQ 08. Qual a relação entre as interações nos PRs e o número de revisões realizadas?**
       
    **Métrica:** 

    **Resultado:** 

    **Discussão do resultado:** 

## 4) Discussão

Os resultados obtidos no relatório indicam 