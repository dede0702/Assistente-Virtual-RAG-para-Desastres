# Assistente Virtual com Arquitetura RAG para Orientação em Desastres Naturais

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://assistente-virtual-rag-para-desastres.streamlit.app/)

**Global Solution - Engenharia de Software | Turma 1ESPF - 2024**

## Integrantes

*   **Alan Maximiano** - RM557088
*   **André Rovai** - RM555848
*   **Leonardo Zago** - RM558691

## 🚀 Demonstração Online

Acesse o assistente virtual em funcionamento:
[https://assistente-virtual-rag-para-desastres.streamlit.app/](https://assistente-virtual-rag-para-desastres.streamlit.app/)

## 📜 Descrição do Projeto

Este projeto consiste no desenvolvimento de um assistente virtual inteligente, o **S.O.S. Assistente RAG**, capaz de fornecer respostas personalizadas, atualizadas e contextualizadas sobre desastres naturais e as melhores práticas de segurança e resposta.

O assistente foi desenvolvido utilizando a arquitetura **RAG (Retrieval-Augmented Generation)**, que combina:
1.  **Modelos de Linguagem da OpenAI (LLM):** Responsáveis pela geração das respostas em linguagem natural (ex: `gpt-4o-mini`).
2.  **Mecanismo de Recuperação de Informações (Retrieval):** Um sistema que busca informações relevantes de uma base de conhecimento para enriquecer o contexto fornecido ao LLM. Nesta versão, a recuperação é simulada com base em palavras-chave e perfil do usuário, mas a arquitetura permite a integração com bases de dados mais complexas e busca semântica.

O objetivo é oferecer suporte rápido e eficaz em momentos críticos, adaptando as orientações para diferentes perfis de usuários.

## 🎯 Perfis de Usuários Atendidos

O assistente é projetado para atender aos seguintes perfis:

1.  **Vítimas Diretamente Afetadas:** Fornece orientações imediatas de segurança, informações sobre resgate e primeiros socorros.
2.  **Moradores da Região em Risco ou Já Afetada:** Oferece alertas preventivos, como se preparar, onde buscar ajuda e informações sobre abrigos.
3.  **Familiares das Vítimas:** Auxilia com canais de contato, informações sobre localização (quando disponíveis e permitidas) e procedimentos de busca.

## ✨ Funcionalidades Principais

*   **Seleção de Perfil:** Permite ao usuário identificar seu perfil para receber orientações mais adequadas.
*   **Consulta em Linguagem Natural:** O usuário pode descrever sua situação ou dúvida.
*   **Recuperação de Contexto (Simulada):** O sistema identifica informações relevantes com base na consulta e no perfil.
*   **Geração de Respostas Aumentadas:** Utiliza a API da OpenAI para gerar respostas empáticas, claras e baseadas no contexto recuperado.
*   **Interface Web Intuitiva:** Desenvolvida com Streamlit para fácil acesso e utilização.
*   **Foco em Segurança e Empatia:** As respostas são projetadas para serem responsáveis e considerarem o estado emocional do usuário.

## 🏛️ Arquitetura RAG (Retrieval-Augmented Generation)

O sistema segue um fluxo RAG simplificado:

1.  **Entrada do Usuário:** O usuário seleciona seu perfil e insere sua consulta.
2.  **Recuperação (Retrieval):**
    *   Nesta implementação, a função `retrieve_information` simula a busca em uma base de conhecimento. Ela seleciona um bloco de texto relevante com base em palavras-chave na consulta do usuário (ex: "enchente", "incêndio") e o perfil selecionado.
    *   Em uma implementação completa, esta etapa envolveria busca semântica em um banco de dados vetorial (ex: FAISS, ChromaDB) contendo embeddings de documentos de fontes confiáveis (manuais da Defesa Civil, notícias, bases de abrigos).
3.  **Geração Aumentada (Augmented Generation):**
    *   A consulta original do usuário e o contexto recuperado são combinados em um prompt estruturado.
    *   Este prompt é enviado para um modelo de linguagem da OpenAI (ex: `gpt-4o-mini`).
    *   O modelo gera a resposta final, que é então exibida ao usuário.

Este processo garante que as respostas do LLM sejam mais fundamentadas, relevantes e menos propensas a "alucinações".

## 🛠️ Tecnologias Utilizadas

*   **Python:** Linguagem principal de desenvolvimento.
*   **OpenAI API:** Para acesso aos modelos de linguagem (LLM).
*   **Streamlit:** Para a criação da interface web interativa.
*   **Pandas:** Para manipulação de dados (utilizado nos logs de debug).
*   **Dotenv:** Para gerenciamento de variáveis de ambiente (API Key).

## ⚙️ Configuração e Execução Local (Streamlit App)

Siga os passos abaixo para executar o assistente em sua máquina local:

1.  **Pré-requisitos:**
    *   Python 3.8 ou superior.
    *   Conta na OpenAI e uma chave de API válida.

2.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/dede0702/Assistente-Virtual-RAG-para-Desastres.git
    cd Assistente-Virtual-RAG-para-Desastres
    ```

3.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Se não houver um `requirements.txt`, instale manualmente: `pip install streamlit openai pandas python-dotenv`)*

5.  **Configure a Chave da API da OpenAI:**
    *   Crie um arquivo chamado `.env` na raiz do projeto.
    *   Adicione sua chave da API da OpenAI ao arquivo `.env` da seguinte forma:
        ```
        OPENAI_API_KEY="sua_chave_secreta_da_openai_aqui"
        ```

6.  **Execute a Aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```
    O aplicativo deverá abrir automaticamente em seu navegador padrão.

## Notebook Google Colab

Uma versão adaptada do assistente também está disponível para execução em ambiente Google Colab. Esta versão utiliza `input()` para interação e `print()` para saídas, ideal para experimentação e testes rápidos sem a interface Streamlit.

Consulte o arquivo `Assistente_RAG_Desastres_Colab.ipynb` (ou similar) no repositório para instruções de como executá-lo. Será necessário fornecer sua chave da API da OpenAI quando solicitado.

## 💡 Reflexão Crítica e Ética

O desenvolvimento de assistentes virtuais para contextos críticos como desastres naturais traz consigo importantes responsabilidades:

*   **Risco de Informações Incorretas:** Embora a arquitetura RAG vise mitigar isso, a precisão das informações recuperadas e a interpretação do LLM são cruciais. É fundamental que o sistema sempre reforce a busca por canais oficiais e não substitua o julgamento humano ou as equipes de emergência.
*   **Atualização das Fontes:** A base de conhecimento deve ser constantemente atualizada e verificada para garantir a relevância e veracidade das informações.
*   **Linguagem Empática e Não Alarmista:** A comunicação deve ser cuidadosamente elaborada para ser empática, clara e evitar causar pânico desnecessário, ao mesmo tempo que alerta para riscos reais.
*   **Acessibilidade:** Considerar como diferentes populações podem acessar e se beneficiar da ferramenta.
*   **Disclaimer:** É vital que o assistente deixe claro que é uma ferramenta de apoio e não um substituto para os serviços de emergência (Defesa Civil, Bombeiros, SAMU).

Este projeto busca ser uma ferramenta de auxílio, priorizando a segurança e o bem-estar dos usuários, e serve como um ponto de partida para discussões e desenvolvimentos futuros na área de IA para gerenciamento de crises.

## 🔮 Possíveis Melhorias Futuras

*   **Integração com Bases de Dados Reais:** Conectar a fontes de dados dinâmicas e oficiais (APIs de alertas, bases de abrigos atualizadas).
*   **Mecanismo de Recuperação Avançado:** Implementar busca semântica com embeddings vetoriais (ex: Sentence Transformers + FAISS/ChromaDB).
*   **Geolocalização:** Utilizar a localização do usuário para fornecer informações mais específicas (rotas de evacuação, abrigos próximos).
*   **Suporte Multilíngue.**
*   **Manutenção de Histórico da Conversa:** Para um diálogo mais fluido e contextual.
*   **Avaliação Contínua da Qualidade das Respostas.**

---

*Este README foi gerado para o projeto da Global Solution - FIAP (2024).*
