import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        primaryColor: Colors.deepOrange,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.deepOrange,
          foregroundColor: Colors.white,
          centerTitle: true,
        ),
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
        ),
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Jogo do Pedra, Papel e Tesoura'),
        ),
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextWidget(texto: 'Escolha da Máquina'),
              IconeWidget(textoIcone: '👊'),
              TextWidget(texto: 'Escolha uma opção abaixo'),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  IconeWidget(textoIcone: '👊'),
                  IconeWidget(textoIcone: '🤚'),
                  IconeWidget(textoIcone: '✌️'),
                ],
              ),
              SizedBox(height: 20),
              TextWidget(texto: 'Você ganhou!'),
            ],
          ),
        ),
      ),
    );
  }
}

class TextWidget extends StatelessWidget {
  final String texto;

  const TextWidget({
    super.key,
    required this.texto,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: Text(
        texto,
        style: Theme.of(context).textTheme.bodyLarge,
      ),
    );
  }
}

class IconeWidget extends StatelessWidget {
  final String textoIcone;

  const IconeWidget({
    super.key,
    required this.textoIcone,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: Container(
        width: 120,
        height: 120,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: const Color(0xFFF1F1F1),
          border:
              Border.all(color: const Color.fromARGB(100, 0, 0, 0), width: 4),
        ),
        child: Text(
          textoIcone,
          style: const TextStyle(fontSize: 64),
        ),
      ),
    );
  }
}
