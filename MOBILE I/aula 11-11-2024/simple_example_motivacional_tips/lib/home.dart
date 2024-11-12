import 'dart:math';
import 'package:flutter/material.dart';
import 'package:adaptive_dialog/adaptive_dialog.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  List<String> frases = [''];
  String frase = '';

  Future<void> adicionarFrase(BuildContext context) async {
    final resultado = await showTextInputDialog(
      context: context,
      message: 'Digite aqui a sua frase motivadora para adicinar à lista:',
      textFields: [
        DialogTextField(
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

  int sorteioIndex() {
    Random random = new Random();
    int resultado = random.nextInt(frases.length);
    return resultado;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          GestureDetector(
            onTap: () {
              adicionarFrase(context);
            },
            child: Padding(
              padding: EdgeInsets.all(8),
              child: Icon(Icons.add_box_sharp),
            ),
          )
        ],
        centerTitle: true,
        title: Text('Frase Motivacional de Hoje'),
        backgroundColor: Colors.red,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: EdgeInsets.all(8),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            verticalDirection: VerticalDirection.down,
            children: [
              Text("Frase motivacional de hoje:"),
              Text(frase),
              ElevatedButton(
                  onPressed: () {
                    setState(() {
                      var sorteio = sorteioIndex();
                      frase = frases[sorteio];
                    });
                  },
                  child: Text('Sortear frase'))
            ],
          ),
        ),
      ),
    );
  }
}
