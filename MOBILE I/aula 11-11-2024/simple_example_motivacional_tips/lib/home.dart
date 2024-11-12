import 'dart:math';
import 'package:flutter/material.dart';
import 'package:adaptive_dialog/adaptive_dialog.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final List<String> frases = []; // Usar final para listas imutáveis
  String frase = '';

  // Função para adicionar uma frase com input do usuário
  Future<void> adicionarFrase(BuildContext context) async {
    final resultado = await showTextInputDialog(
      context: context,
      message: 'Digite aqui a sua frase motivadora para adicionar à lista:',
      textFields: [
        const DialogTextField(
          hintText: 'Digite aqui a sua frase:',
        ),
      ],
    );

    if (resultado != null && resultado.isNotEmpty) {
      setState(() {
        frases.add(resultado[0]);
      });
    }
  }

  // Função para sortear índice de uma frase
  int sorteioIndex() => Random().nextInt(frases.length);

  // Função para sortear uma nova frase
  void sortearFrase() {
    if (frases.isNotEmpty) {
      setState(() {
        frase = frases[sorteioIndex()];
      });
    } else {
      setState(() {
        frase = 'Nenhuma frase adicionada!';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            icon: const Icon(Icons.add_box_sharp),
            onPressed: () => adicionarFrase(context),
          ),
        ],
        centerTitle: true,
        title: const Text('Frase Motivacional de Hoje'),
        backgroundColor: Colors.red,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(8),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("Frase motivacional de hoje:"),
              const SizedBox(height: 32),
              Text(
                frase,
                style: const TextStyle(fontSize: 32),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: sortearFrase,
                child: const Text('Sortear frase'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
