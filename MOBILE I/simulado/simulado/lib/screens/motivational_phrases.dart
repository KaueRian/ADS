import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';
import 'dart:math';
import 'package:adaptive_dialog/adaptive_dialog.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final List<String> frases = [];
  String frase = '';

  Future<void> adicionarFrase(BuildContext context) async {
    final resultado = await showTextInputDialog(
      context: context,
      message: 'Digite aqui a sua frase motivadora para adicinar à lista:',
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

  int sorteioIndex() {
    Random random = Random();
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
            child: const Padding(
              padding: EdgeInsets.all(8),
              child: Icon(Icons.add_box_sharp),
            ),
          )
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
            verticalDirection: VerticalDirection.down,
            children: [
              const Text("Frase motivacional de hoje:"),
              const SizedBox(
                height: 32,
              ),
              Text(
                frase,
                style: const TextStyle(
                  fontSize: 32,
                ),
              ),
              const SizedBox(
                height: 32,
              ),
              ElevatedButton(
                  onPressed: () {
                    setState(() {
                      var sorteio = sorteioIndex();
                      frase = frases[sorteio];
                    });
                  },
                  child: const Text('Sortear frase'))
            ],
          ),
        ),
      ),
    );
  }
}