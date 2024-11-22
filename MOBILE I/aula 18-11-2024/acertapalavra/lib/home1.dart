import 'package:flutter/material.dart';
import 'dart:math';

class Home1 extends StatefulWidget {
  const Home1({Key? key}) : super(key: key);

  @override
  State<Home1> createState() => _Home1State();
}

class _Home1State extends State<Home1> {
  static const palavras = {
    "Dia": "Noite",
    "Alegre": "Triste",
    "Vivo": "Morto",
  };

  late String palavraSorteada;
  final TextEditingController _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    sortearPalavra();
  }

  void sortearPalavra() {
    final random = Random();
    final chaves = palavras.keys.toList();
    setState(() {
      palavraSorteada = chaves[random.nextInt(chaves.length)];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tela Home1'),
        centerTitle: true,
        foregroundColor: Colors.white,
        backgroundColor: Colors.blue,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Dica: ${palavras[palavraSorteada]}"),
            const SizedBox(height: 32),
            TextFormField(
              controller: _controller,
              decoration: const InputDecoration(
                border: UnderlineInputBorder(),
                labelText: 'Coloque a palavra aqui',
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              style: TextButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: Colors.blue,
              ),
              onPressed: () {
                String userInput = _controller.text.trim();

                if (userInput == palavraSorteada) {
                  Navigator.pushNamed(context, '/home2');
                } else {
                  Navigator.pushNamed(context, '/home3');
                }
              },
              child: const Text('Verificar a palavra'),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              style: TextButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: Colors.green,
              ),
              onPressed: sortearPalavra,
              child: const Text('Sortear outra palavra'),
            ),
          ],
        ),
      ),
    );
  }
}
