import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: Text('Jogo do Pedra, Papel e Tesoura'),
          backgroundColor: Colors.deepOrange,
          foregroundColor: Color.fromARGB(255, 250, 250, 250),
        ),
        body: Center(
          child: Column(
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  TextWidget(texto: 'Escolha da Máquina'),
                  IconeWidget(textoIcone: '👊'),
                  TextWidget(texto: 'Escolha uma opção abaixo'),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  IconeWidget(textoIcone: '👊'),
                  IconeWidget(textoIcone: '🤚'),
                  IconeWidget(textoIcone: '✌️'),
                ],
              ),
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

  TextWidget({
    super.key,
    required this.texto,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(8),
      child: Text(
        texto,
        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
      ),
    );
  }
}

class IconeWidget extends StatelessWidget {
  final String textoIcone;

  IconeWidget({
    super.key,
    required this.textoIcone,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(8),
      child: Container(
        width: 120,
        height: 120,
        alignment: Alignment.center,
        decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Color.fromARGB(255, 241, 241, 241),
            border: Border.all(color: Color.fromARGB(100, 0, 0, 0), width: 4)),
        child: Text(
          textoIcone,
          style: TextStyle(fontSize: 64),
        ),
      ),
    );
  }
}
