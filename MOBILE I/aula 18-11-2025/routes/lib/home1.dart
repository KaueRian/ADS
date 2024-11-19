import 'package:flutter/material.dart';

class Home1 extends StatelessWidget {
  const Home1({super.key});

  static const palavras = {
    "Dia": "Noite",
    "Alegre": "Triste",
    "Vivo": "Morto",
  };



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Tela Home1'),
        centerTitle: true,
        foregroundColor: Colors.white,
        backgroundColor: Colors.blue,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Dica: ${palavras["Dia"]!}"),
            SizedBox(
              height: 32,
            ),
          var nome = TextFormField(
      decoration: const InputDecoration(
      border: UnderlineInputBorder(),
      labelText: 'Coloque a palavra aqui',

      ),

    );

            ElevatedButton(
                style: TextButton.styleFrom(
                    foregroundColor: Colors.white,
                    backgroundColor: Colors.blue),
                onPressed: () {
                  Navigator.pushNamed(context, '/home2');
                },
                child: Text('Ir para 2º tela'))
          ],
        ),
      ),
    );
  }
}
