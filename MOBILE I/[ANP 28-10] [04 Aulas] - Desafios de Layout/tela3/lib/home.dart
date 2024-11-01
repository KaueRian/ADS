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
          foregroundColor: Colors.white,
        ),
        body: Center(
          child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                TextWidget(texto: 'Escolha da Máquina')
              ]
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
    return Padding(padding: EdgeInsets.all(8),
      child: Text(texto, style: TextStyle(fontWeight: FontWeight.bold),),
    );
  }
}

class IconeWidget extends StateLessWidget {
  final 
}