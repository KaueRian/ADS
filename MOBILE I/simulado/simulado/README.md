### Estrutura do Projeto:
1. **Tela Inicial (Dashboard)**:
   - Apresenta uma visão geral com botões ou cards para acessar cada funcionalidade (Frases Motivacionais, Preços de Criptomoedas, Jogo de Adivinhação, e Consumo de API).

2. **Funcionalidades**:
   - **Frases Motivacionais**:
     - Permite adicionar frases à lista e sortear uma frase aleatória para exibição.
   - **Preços de Criptomoedas**:
     - Exibe uma lista de criptomoedas com seus preços e permite navegar para uma página de detalhes.
   - **Jogo de Adivinhação**:
     - Um jogo simples que exibe uma dica e permite ao usuário tentar adivinhar a palavra.
   - **Consumo de API**:
     - Um exemplo funcional que consome uma API pública (como ViaCEP) e exibe os dados na tela.

3. **Navegação**:
   - Use rotas nomeadas para transitar entre as telas.
   - A tela inicial servirá como ponto central para acessar as outras.

4. **Gerenciamento de Estado**:
   - Use `setState` para gerenciar estados simples em cada funcionalidade.
   - Para dados compartilhados entre páginas, considere usar o `Provider` ou o `InheritedWidget`.

---

### Exemplo de Estrutura de Diretórios:
```plaintext
lib/
├── main.dart
├── screens/
│   ├── dashboard.dart
│   ├── motivational_phrases.dart
│   ├── crypto_prices.dart
│   ├── guessing_game.dart
│   └── api_consumer.dart
├── widgets/
│   ├── crypto_card.dart
│   └── custom_button.dart
└── models/
    └── crypto.dart
```

---

### Passos para Desenvolvimento:
1. Crie a tela inicial (`dashboard.dart`) com botões para navegar para cada funcionalidade.
2. Implemente cada funcionalidade como uma tela separada.
3. Teste a navegação entre as telas.
4. Integre os widgets e lógica de cada funcionalidade.
5. Adicione estilos e ajustes finais.

Se quiser, posso detalhar o desenvolvimento de cada tela ou começar com o código básico. O que prefere? 😊
